from dataclasses import dataclass
from datetime import datetime

from openshift_ldap_operator.resources.base import KubeResourceBase, _field_schema


@dataclass
class LdapGroupSpec:
    group_name: str = _field_schema(
        description="",
    )


@dataclass
class LdapGroupStatus:
    group_dn: str = _field_schema(
        description="",
    )
    cluster_group_name: str = _field_schema(
        description="",
    )
    last_updated_timestamp: datetime = _field_schema(
        description="",
    )


@dataclass
class LdapGroup(KubeResourceBase):
    __group__ = "ldap.wopr.tech"
    __version__ = "v1alpha1"

    spec: LdapGroupSpec = _field_schema(
        description="",
    )
    status: LdapGroupStatus = _field_schema(
        description="",
    )
