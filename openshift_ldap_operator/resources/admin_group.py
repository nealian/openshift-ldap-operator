from dataclasses import dataclass
from datetime import datetime

from openshift_ldap_operator.resources.base import (
    KubeResourceBase,
    KubeTypedResourceRef,
    _field_schema,
)


@dataclass
class LdapAdminGroupSpec:
    group_name: str = _field_schema(
        description="",
    )
    role_ref: KubeTypedResourceRef = _field_schema(
        description="",
    )


@dataclass
class LdapAdminGroupStatus:
    group_name: str = _field_schema(
        description="",
    )
    group_dn: str = _field_schema(
        description="",
    )
    role_ref: KubeTypedResourceRef = _field_schema(
        description="",
    )


@dataclass
class LdapAdminGroup(KubeResourceBase):
    __group__ = "ldap.wopr.tech"
    __version__ = "v1alpha1"

    spec: LdapAdminGroupSpec = _field_schema(
        description="",
    )
    status: LdapAdminGroupStatus = _field_schema(
        description="",
    )
