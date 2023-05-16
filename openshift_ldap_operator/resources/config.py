from dataclasses import dataclass, field
from uuid import UUID
from typing import List, Optional
from .base import KubeResourceBase, KubeLocalResourceRef, KubeCondition, _field_schema
from apischema import schema
from datetime import datetime


@dataclass
class LdapConfigPassword:
    value: Optional[str] = _field_schema(
        description="value is an optional static value for a password",
    )
    secret: KubeLocalResourceRef = _field_schema(
        description="secret is an optional reference to a secret in the local namespace",
    )


@dataclass
class LdapConfigCfgMap:
    value: Optional[str] = _field_schema(
        description="",
    )
    configMap: KubeLocalResourceRef = _field_schema(
        description="",
    )


@dataclass
class LdapConfigServerConfig:
    url: str
    bindDN: str
    bindPassword: LdapConfigPassword


@dataclass
class LdapConfigSpec:
    serverConfig: LdapConfigServerConfig


@dataclass
class LdapConfigStatus:
    conditions: List[KubeCondition]
    lastUpdatedTimestamp: datetime


@dataclass
class LdapConfig(KubeResourceBase):
    __group__ = "ldap.wopr.tech"
    __version__ = "v1alpha1"

    spec: LdapConfigSpec
    status: LdapConfigStatus
