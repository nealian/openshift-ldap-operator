from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from openshift_ldap_operator.resources.base import (
    KubeCondition,
    KubeLocalResourceRef,
    KubeResourceBase,
    _field_schema,
)

# TODO: find out what's optional


@dataclass
class LdapConfigPassword:
    value: Optional[str] = _field_schema(
        description="value is an optional static value for a password. Conflicts with 'secret'.",
    )
    secret: Optional[KubeLocalResourceRef] = _field_schema(
        description="secret is an optional reference to a value in a secret in the local namespace. Conflicts with 'value'.",
    )


@dataclass
class LdapConfigCfgMap:
    value: Optional[str] = _field_schema(
        description="value is an optional static (string) value for some config. Conflicts with 'configMap'.",
    )
    config_map: Optional[KubeLocalResourceRef] = _field_schema(
        description="configMap is an optional reference to a value in a configMap in the local namespace. Conflicts with 'value'.",
    )


class LdapConfigServerType(StrEnum):
    RFC2307 = "rfc2307"
    ActiveDirectory = "activeDirectory"
    AugmentedActiveDirectory = "augmentedActiveDirectory"


class LdapConfigScope(StrEnum):
    Sub = "sub"
    Base = "base"
    One = "one"


class LdapConfigDerefAliases(StrEnum):
    Never = "never"
    Search = "search"
    Base = "base"
    Always = "always"


@dataclass
class LdapConfigServerConfig:
    url: str = _field_schema(
        description="",
    )
    bind_dn: str = _field_schema(
        description="",
    )
    bind_password: LdapConfigPassword = _field_schema(
        description="",
    )
    insecure: bool = _field_schema(
        description="",
    )
    ca: LdapConfigCfgMap = _field_schema(
        description="",
    )
    baseDN: str = _field_schema(
        description="",
    )
    server_type: LdapConfigServerType = _field_schema(
        description="",
    )


@dataclass
class LdapConfigUserSearchAttributes:
    uid: str = _field_schema(
        description="",
    )
    name: list[str] = _field_schema(
        description="",
    )
    group_membership: list[str] = _field_schema(
        description="",
    )


@dataclass
class LdapConfigUserSearch:
    base_dn: str = _field_schema(
        description="",
    )
    scope: LdapConfigScope = _field_schema(
        description="",
    )
    deref_aliases: LdapConfigDerefAliases = _field_schema(
        description="",
    )
    timeout: int = _field_schema(
        description="",
    )
    filter: str = _field_schema(
        description="",
    )
    page_size: int = _field_schema(
        description="",
    )
    attributes: LdapConfigUserSearchAttributes = _field_schema(
        description="",
    )


@dataclass
class LdapConfigGroupSearchAttributes:
    uid: str = _field_schema(
        description="",
    )
    name: str = _field_schema(
        description="",
    )
    user_membership: list[str] = _field_schema(
        description="",
    )


@dataclass
class LdapConfigGroupSearch:
    base_dn: str = _field_schema(
        description="",
    )
    scope: LdapConfigScope = _field_schema(
        description="",
    )
    deref_aliases: LdapConfigDerefAliases = _field_schema(
        description="",
    )
    timeout: int = _field_schema(
        description="",
    )
    filter: str = _field_schema(
        description="",
    )
    page_size: int = _field_schema(
        description="",
    )
    attributes: LdapConfigGroupSearchAttributes = _field_schema(
        description="",
    )
    uid_name_mapping: dict[str, str] = _field_schema(
        description="",
    )


@dataclass
class LdapConfigSpec:
    server_config: LdapConfigServerConfig = _field_schema(
        description="",
    )
    user_search: LdapConfigUserSearch = _field_schema(
        description="",
    )
    group_search: LdapConfigGroupSearch = _field_schema(
        description="",
    )
    schedule: str = _field_schema(  # TODO: str?
        description="",
    )


@dataclass
class LdapConfigStatus:
    conditions: list[KubeCondition] = _field_schema(
        description="",
    )
    lastUpdatedTimestamp: datetime = _field_schema(
        description="",
    )


@dataclass
class LdapConfig(KubeResourceBase):
    __group__ = "ldap.wopr.tech"
    __version__ = "v1alpha1"

    spec: LdapConfigSpec = _field_schema(
        description="",
    )
    status: LdapConfigStatus = _field_schema(
        description="",
    )
