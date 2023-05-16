

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

from .config import LdapConfig
