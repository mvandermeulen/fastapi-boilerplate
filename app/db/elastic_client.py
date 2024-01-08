from elasticsearch import Elasticsearch

from app.core.config import settings


def elasticsearch_client():
    client = Elasticsearch(
        hosts=[settings.ELASTIC_HOST],
        http_auth=(settings.ELASTIC_CLUSTER_NAME, settings.ELASTIC_PASSWORD),
    )

    return client
