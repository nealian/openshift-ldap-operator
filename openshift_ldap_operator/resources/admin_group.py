from dataclasses import dataclass
from datetime import datetime

from openshift_ldap_operator.resources.base import (
    KubeLocalResourceRef,
    KubeResourceBase,
    KubeTypedResourceRef,
    PrintColumn,
    _field_schema,
)


@dataclass
class LdapAdminGroupSpec:
    group_ref: KubeLocalResourceRef = _field_schema(
        description="groupRef can only be a reference to an LdapGroup to give the referenced role in this namespace.",
    )
    role_ref: KubeTypedResourceRef = _field_schema(
        description="roleRef, if provided, can only reference a single Role or a single ClusterRole.  Defaults to ClusterRole 'admin'.",
    )


@dataclass
class LdapAdminGroupStatus:
    group_name: str = _field_schema(
        description="groupName refers to the short name of the group referenced in the associated LDAPGroup, and will only appear if spec.groupRef resolves.",
    )
    group_dn: str = _field_schema(
        description="groupDN refers to the full Distinguished Name of the group referenced in the associated LDAPGroup, and will only appear if spec.groupRef resolves and has been synchronized.",
    )
    role_ref: KubeTypedResourceRef = _field_schema(
        description="if spec.roleRef is a valid reference to a Role, then we show the good reference to it.",
    )
    cluster_role: str = _field_schema(
        description="if spec.roleRef is a valid reference to a ClusterRole, then we show the name for it.",
    )


@dataclass
class LdapAdminGroup(KubeResourceBase):
    spec: LdapAdminGroupSpec = _field_schema(
        description="",
    )
    status: LdapAdminGroupStatus = _field_schema(
        description="",
    )

    __group__ = "ldap.wopr.tech"
    __version__ = "v1alpha1"
    __scope__ = "namespaced"
    __singular__ = "ldapadmingroup"
    __plural__ = "ldapadmingroups"
    __kind__ = "LDAPAdminGroup"
    __short_names__ = ["lag"]
    __print_columns__ = [
        PrintColumn(
            name="Group",
            type="string",
            json_path=".spec.groupRef.name",
        ),
        PrintColumn(
            name="Cluster Role",
            type="string",
            json_path=".status.clusterRole",
        ),
        PrintColumn(
            name="Role",
            type="string",
            json_path=".status.roleRef.name",
        ),
    ]
