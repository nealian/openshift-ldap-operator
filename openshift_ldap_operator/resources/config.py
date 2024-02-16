from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from openshift_ldap_operator.resources.base import (
    KubeCondition,
    KubeLocalResourceRef,
    KubeResourceBase,
    PrintColumn,
    _field_schema,
    dataclassloader,
)

# TODO: find out what's optional


@dataclassloader
@dataclass
class LdapConfigPassword:
    value: Optional[str] = _field_schema(
        description="value is an optional static value for a password. If set, will create or override the secret 'ldap-operator-bindpass' within the 'openshift-config' namespace. Conflicts with 'secret'.",
    )
    secret: Optional[KubeLocalResourceRef] = _field_schema(
        description="secret is an optional reference to a value in a secret in the 'openshift-config' namespace. Conflicts with 'value'.",
    )


@dataclassloader
@dataclass
class LdapConfigCfgMap:
    value: Optional[str] = _field_schema(
        description="value is an optional static (string) value for some config. Conflicts with 'configMap'.",
    )
    config_map: Optional[KubeLocalResourceRef] = _field_schema(
        description="configMap is an optional reference to a value in a configMap in the 'openshift-config' namespace. Conflicts with 'value'.",
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


@dataclassloader
@dataclass
class LdapConfigServerConfig:
    url: str = _field_schema(
        description="url is the scheme, host, and port of the LDAP server to connect to, like 'scheme://host[:port]'.",
    )
    bind_dn: str = _field_schema(
        description="bindDN is the optional DN to bind with.",
    )
    bind_password: LdapConfigPassword = _field_schema(
        description="bindPassword is optional, and either the value of the password or a reference to that value with which to bind to the LDAP server.",
    )
    insecure: bool = _field_schema(
        description="insecure indicates not to use StartTLS on connections with 'ldap://' urls.  The use of 'insecure: true' with 'ldaps://' urls is invalid.",
    )
    ca: LdapConfigCfgMap = _field_schema(
        description="ca is optional, and either the value of or a reference to the trusted roots for TLS connections with the LDAP server.  If not provided, the upstream container (OpenShift official CLI container image) default trust store is used.",
    )
    base_dn: str = _field_schema(
        description="baseDN is an optional global base from which the users and groups base DNs are derived.",
    )
    server_type: LdapConfigServerType = _field_schema(
        description="serverType is the type of server; valid values are 'rfc2307', 'activeDirectory', and 'augmentedActiveDirectory'.  See OpenShift documentation for v1.LDAPSyncConfig for more details.",
    )


@dataclassloader
@dataclass
class LdapConfigUserSearchAttributes:
    uid: str = _field_schema(
        description="uid defines which attribute determines the unique user id; if using dynamic groups, the value format of this attribute must match that of one of the group membership attributes.",
    )
    name: list[str] = _field_schema(
        description="name defines which attribute determines the value for the user's username within OpenShift.  The first attribute with a non-empty value will be used.  Values must be unique.",
    )
    display_name: list[str] = _field_schema(
        description="displayName defines which attribute determines the value for the user's display name.  Optional.  If unspecified, no display name is set for the identity.  The first attribute with a non-empty value will be used.",
        default_factory=list,
    )
    email: list[str] = _field_schema(
        description="email defines which attribute determines the value for the user's email.  The first attribute with a non-empty value will be used.  Values must be unique.  Optional.",
        default_factory=list,
    )
    group_membership: list[str] = _field_schema(
        description="groupMembership defines which attribute determines which groups a user is a member of; only used in ActiveDirectory contexts.  Uses the value of the first non-empty attribute in the list.",
    )


@dataclassloader
@dataclass
class LdapConfigUserSearch:
    base_dn: str = _field_schema(
        description="baseDN is the optional DN (relative to server base DN, if configured) under which to search for users.  May only be omitted if server baseDN is defined.",
    )
    scope: LdapConfigScope = _field_schema(
        description="scope is the optional scope of the search; valid values are 'base', 'one', and 'sub'.  Defaults to 'sub' if not set.",
    )
    deref_aliases: LdapConfigDerefAliases = _field_schema(
        description="derefAliases is the optional behavior of the search with regards to aliases; valid values are 'never', 'search', 'base', and 'always'.  Defaults to 'always' if not set.",
    )
    timeout: int = _field_schema(
        description="timeout determines the limit in seconds for any requests to the server to remain outstanding before giving up.  If 0, no client-side limit is imposed.",
    )
    filter: str = _field_schema(
        description="filter defines the user search criteria to get all valid users within the base DN.",
    )
    page_size: int = _field_schema(
        description="pageSize is the maximum preferred page size for requests against the server, measured in number of LDAP entries.  A page size of 0 indicates no paging.",
    )
    attributes: LdapConfigUserSearchAttributes = _field_schema(
        description="attributes is a mapping  of specific user elements to their matching LDAP attributes.",
    )


@dataclassloader
@dataclass
class LdapConfigGroupSearchAttributes:
    uid: str = _field_schema(
        description="uid defines which attribute determines the unique group id.",
    )
    name: str = _field_schema(
        description="name defines which attribute to use for the group name within OpenShift; optional if uidNameMapping is set.",
    )
    user_membership: list[str] = _field_schema(
        description="userMembership defines which attribute determines which users are members of the group.  The first non-empty attribute in this list will be used.",
    )


@dataclassloader
@dataclass
class LdapConfigGroupSearch:
    base_dn: str = _field_schema(
        description="baseDN is the optional DN (relative to server base DN, if configured) under which to search for groups.  May be omitted if the server base DN is defined or if group membership is determined by the user's LDAP object.",
    )
    scope: LdapConfigScope = _field_schema(
        description="scope is the optional scope of the search; valid values are 'base', 'one', and 'sub'.  Defaults to 'sub' if not set.  May also be omitted if group membership is determined by the user's LDAP object.",
    )
    deref_aliases: LdapConfigDerefAliases = _field_schema(
        description="derefAliases is the optional behavior of the search with regards to aliases; valid values are 'never', 'search', 'base', and 'always'.  Defaults to 'always' if not set.  May also be omitted if group membership is determined by the user's LDAP object.",
    )
    timeout: int = _field_schema(
        description="timeout determines the limit in seconds for any requests to the server to remain outstanding before giving up.  If 0, no client-side limit is imposed.  May be omitted only if group membership is determined by the user's LDAP object.",
    )
    filter: str = _field_schema(
        description="filter defines the search criteria to get all valid groups within the base DN.  May be omitted only if group membership is determined by the user's LDAP object.",
    )
    page_size: int = _field_schema(
        description="pageSize is the maximum preferred page size for requests against the server, measured in number of LDAP entries.  A page size of 0 indicates no paging.  May be omitted only if group membership is determined by the user's LDAP object.",
    )
    attributes: LdapConfigGroupSearchAttributes = _field_schema(
        description="attributes is the mapping of specific group elements to their matching LDAP attributes.  May be omitted only if group membership is determined by the user's LDAP object.",
    )
    uid_name_mapping: dict[str, str] = _field_schema(
        description="uidNameMapping is an optional direct map of LDAP group UIDs to OpenShift group names.",
    )


@dataclassloader
@dataclass
class LdapConfigSpec:
    server_config: LdapConfigServerConfig = _field_schema(
        description="serverConfig defines information about the LDAP server(s) to connect to, as well as bind options.",
    )
    user_search: LdapConfigUserSearch = _field_schema(
        description="userSearch defines information about finding and filtering individual users, and mapping their information into OpenShift.",
    )
    group_search: LdapConfigGroupSearch = _field_schema(
        description="groupSearch defines information about finding and filtering groups, and mapping their information into OpenShift.  Unused in non-Augmented ActiveDirectory contexts.",
    )
    schedule: str = _field_schema(
        description="schedule defines the LDAP synchronization schedule, defaults to 'daily'.",
    )


@dataclassloader
@dataclass
class LdapConfigStatus:
    conditions: list[KubeCondition] = _field_schema(
        description="conditions is a list of conditions and their statuses relevant to LDAPConfig objects.",
    )
    lastUpdatedTimestamp: datetime = _field_schema(
        description="lastUpdatedTime represents the last time synchronization completed successfully.",
    )


@dataclassloader
@dataclass
class LdapConfig(KubeResourceBase):
    spec: LdapConfigSpec = _field_schema(
        description="spec defines the desired state of LDAPConfig.",
    )
    status: LdapConfigStatus = _field_schema(
        description="status defines the observed state of LDAPConfig.",
    )

    __group__ = "ldap.wopr.tech"
    __version__ = "v1alpha1"
    __scope__ = "cluster"
    __singular__ = "ldapconfig"
    __plural__ = "ldapconfigs"
    __kind__ = "LDAPConfig"
    __allowed_names__ = ["cluster"]
