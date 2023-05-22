from dataclasses import dataclass

from openshift_ldap_operator.resources.base import (
    KubeLocalResourceRef,
    KubeResourceBase,
    PrintColumn,
    _field_schema,
)

# TODO: optionals

@dataclass
class LdapClusterAdminGroupSpec:
    group_ref: KubeLocalResourceRef = _field_schema(
        description="groupRef can only be a reference to an LdapGroup to give the referenced cluster role.",
    )
    role_ref: KubeLocalResourceRef = _field_schema(
        description="roleRef, if provided, can only reference a single ClusterRole.  Defaults to 'admin'.",
    )


@dataclass
class LdapClusterAdminGroupStatus:
    group_name: str = _field_schema(
        description="groupName refers to the short name of the group referenced in the associated LDAPGroup, and will only appear if spec.groupRef resolves.",
    )
    group_dn: str = _field_schema(
        description="groupDN refers to the full Distinguished Name of the group referenced in the associated LDAPGroup, and will only appear if spec.groupRef resolves and has been synchronized.",
    )
    cluster_role: KubeLocalResourceRef = _field_schema(
        description="if spec.roleRef is a valid reference to a ClusterRole, then we show it.",
    )
    cluster_role_binding: KubeLocalResourceRef = _field_schema(
        description='if the child rolebinding exists, we show the reference to it here',
    )


@dataclass
class LdapClusterAdminGroup(KubeResourceBase):
    spec: LdapClusterAdminGroupSpec = _field_schema(
        description="",  # TODO
    )
    status: LdapClusterAdminGroupStatus = _field_schema(
        description="",  # TODO
    )

    __group__ = "ldap.wopr.tech"
    __version__ = "v1alpha1"
    __scope__ = "cluster"
    __singular__ = "ldapclusteradmingroup"
    __plural__ = "ldapclusteradmingroups"
    __kind__ = "LDAPClusterAdminGroup"
    __short_names__ = ["lcag"]
    __print_columns__ = [
        PrintColumn(
            name="Group",
            type="string",
            json_path=".spec.groupRef.name",
        ),
        PrintColumn(
            name="Cluster Role",
            type="string",
            json_path=".status.clusterRole.name",
        ),
        PrintColumn(
            name="Cluster Role Binding",
            type="string",
            json_path=".status.clusterRoleBinding.name",
        ),
    ]
