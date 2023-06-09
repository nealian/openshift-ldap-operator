

"""
v1alpha1

LdapAdminGroup
  spec
    groupRef
    roleRef
  status
    groupName
    groupDN
    roleRef
LdapConfig
  spec
    serverConfig
      url
      bindDN
      bindPassword
        value, or
        secret
          name
          key
      insecure
      ca
        value, or
        configmap
          name
          key
      baseDN
      serverType
        rfc2307
        activeDirectory
        augmentedActiveDirectory
    userSearch
      baseDN
      scope
        sub
        base
        one
      derefAliases
        never
        search
        base
        always
      timeout
      filter
      pageSize
      attributes
        uid
        name[]
        groupMembership[]
    groupSearch
      baseDN
      scope
      derefAliases
      timeout
      filter
      pageSize
      attributes
        uid
        name
        userMembership[]
      uidNameMapping{}
    schedule
  status
    conditions
    lastUpdatedTimestamp
LdapGroup
  spec
    groupName
  status
    groupDN
    clusterGroupName
    lastUpdatedTimestamp
"""

from openshift_ldap_operator.resources.admin_group import LdapAdminGroup
from openshift_ldap_operator.resources.cluster_admin_group import LdapClusterAdminGroup
from openshift_ldap_operator.resources.config import LdapConfig
from openshift_ldap_operator.resources.group import LdapGroup

__all__ = [
    'LdapAdminGroup',
    'LdapClusterAdminGroup',
    'LdapConfig',
    'LdapGroup',
]