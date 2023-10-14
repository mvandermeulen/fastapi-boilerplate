import os
from typing import Any

import casbin
import casbin_sqlalchemy_adapter

from app.core.config import settings


path_name = os.path.dirname(os.path.abspath(__file__))
adapter = casbin_sqlalchemy_adapter.Adapter(settings.get_database_url())
enforcer = casbin.Enforcer(f"{path_name}/auth_model.conf", adapter)


def add_policy(role: str, sub: str, act: str) -> (Any | bool):
    return enforcer.add_policy(role, sub, act)


def get_policies():
    return enforcer.get_policy()


def delete_policy(role: str, sub: str, act: str) -> (Any | bool):
    return enforcer.remove_policy(role, sub, act)


def update_policie(old_rule: Any, new_rule: Any) -> (Any | bool):
    return enforcer.update_policy(old_rule=old_rule, new_rule=new_rule)
