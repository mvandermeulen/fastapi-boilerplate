import datetime
import json
import math
from typing import Any
from typing import List
from typing import TypeVar

from elasticsearch.helpers import scan
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .base import CRUDBase
from app import schemas
from app.db.elastic_client import elasticsearch_client
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
ListResponseSchemaType = TypeVar("ListResponseSchemaType", bound=BaseModel)
es = elasticsearch_client()


class CRUDSyncBase(
    CRUDBase[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
        ResponseSchemaType,
        ListResponseSchemaType,
    ],
):
    def get_db_obj_by_id(
        self,
        db: Session,
        id: Any,
        include_deleted: bool = False,
    ) -> ModelType | None:
        db_obj = (
            db.query(self.model)
            .filter(self.model.id == id)
            .execution_options(include_deleted=include_deleted)
            .first()
        )
        return db_obj

    def get_db_obj_list(
        self,
        db: Session,
        where_clause: list[Any] | None = None,
        sort_query_in: schemas.SortQueryIn | None = None,
        include_deleted: bool = False,
    ) -> list[ModelType]:
        query = db.query(self.model)
        if where_clause is not None:
            query = query.filter(*where_clause)
        if sort_query_in:
            order_by_clause = self._get_order_by_clause(sort_query_in.sort_field)
            query = sort_query_in.apply_to_query(query, order_by_clause=order_by_clause)
        db_obj_list = query.execution_options(include_deleted=include_deleted).all()

        return db_obj_list

    def get_paged_list(
        self,
        db: Session,
        paging_query_in: schemas.PagingQueryIn,
        where_clause: list[Any] | None = None,
        sort_query_in: schemas.SortQueryIn | None = None,
        include_deleted: bool = False,
    ) -> ListResponseSchemaType:
        """Notes
        include_deleted=True include_deleted=True returns data with delete flag=True.
        """
        where_clause = where_clause if where_clause is not None else []
        total_count = db.query(self.model).filter(*where_clause).count()

        select_columns = self._get_select_columns()
        query = db.query(*select_columns).filter(*where_clause)
        if sort_query_in:
            order_by_clause = self._get_order_by_clause(sort_query_in.sort_field)
            query = sort_query_in.apply_to_query(query, order_by_clause=order_by_clause)
        query = paging_query_in.apply_to_query(query)
        query = query.execution_options(include_deleted=include_deleted)
        data = query.all()
        meta = schemas.PagingMeta(
            total_data_count=total_count,
            current_page=paging_query_in.page,
            total_page_count=int(math.ceil(total_count / paging_query_in.per_page)),
            per_page=paging_query_in.per_page,
        )
        list_response = self.list_response_class(data=data, meta=meta)

        return list_response

    def create(self, db: Session, create_schema: CreateSchemaType) -> ModelType:
        # by_by_alias=False else (CamenCase) will be used
        create_dict = jsonable_encoder(create_schema, by_alias=False)
        exists_create_dict = self._filter_model_exists_fields(create_dict)
        db_obj = self.model(**exists_create_dict)
        print(db_obj.__dict__)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)

        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        update_schema: UpdateSchemaType,
    ) -> ModelType:
        # Update obj_in schema for each model column
        db_obj_dict = jsonable_encoder(db_obj)
        update_dict = update_schema.model_dump(
            exclude_unset=True,
        )
        # Unset columns are not updated when exclude_unset=True is enabled.
        for field in db_obj_dict:
            if field in update_dict:
                setattr(db_obj, field, update_dict[field])

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> ModelType:
        if db_obj.deleted_at:
            # Raise an exception
            print("Raise an excepton")
        db_obj.deleted_at = datetime.datetime.now(tz=datetime.timezone.utc)
        print(db_obj)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def search_index(
        self,
        paging_query_in: schemas.PagingQueryIn,
        index_name: str,
        query_text: Any = None,
        filters: Any = None,
        fields: List[str] = [],
        sort_query_in: Any | None = None,
    ) -> Any:
        """
        => filters = [{"term": {"field_name": "value"}}]
        # Modify 'field_name' and 'value' to your specific filter

        # Modify 'field_to_search' to your specific field
        """
        body: Any = {
            "from": paging_query_in.get_offset(),
            "size": paging_query_in.per_page,
            "query": {"match_all": {}},
        }

        if query_text and len(fields) > 0:
            body["query"] = {
                "multi_match": {
                    "query": query_text,
                    "fields": fields,
                    "fuzziness": "AUTO",
                }
            }

        if sort_query_in is not None:
            sort = []
            sort.append(
                {sort_query_in["sortField"]: {"order": sort_query_in["direction"]}}
            )
            body["sort"] = json.loads(json.dumps(sort))
        else:
            body["sort"] = [
                {
                    "created_at": {
                        "order": "asc",
                        "missing": "_last",
                        "ignore_unmapped": True,
                    }
                }
            ]

        if filters:
            body["query"]["bool"]["filter"] = filters

        results = es.search(index=index_name, body=body)
        return results

    def paginate_results(
        self,
        paging_query_in: schemas.PagingQueryIn,
        index_name: str,
        query_text: Any = None,
        filters: Any = None,
        fields: List[str] = [],
        sort_query_in: Any | None = None,
    ) -> ListResponseSchemaType:
        results = self.search_index(
            query_text=query_text,
            index_name=index_name,
            filters=filters,
            paging_query_in=paging_query_in,
            fields=fields,
            sort_query_in=sort_query_in,
        )
        total_elmt = results["hits"]["total"]["value"]
        data = [hit["_source"] for hit in results["hits"]["hits"]]

        meta = schemas.PagingMeta(
            total_data_count=total_elmt,
            current_page=paging_query_in.page,
            total_page_count=int(math.ceil(total_elmt / paging_query_in.per_page)),
            per_page=paging_query_in.per_page,
        )

        list_response = self.list_response_class(data=data, meta=meta)

        return list_response

    def read_all(self, index_name):
        scanner = scan(es, index=index_name)
        return [result["_source"] for result in scanner]
