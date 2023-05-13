from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID
from kubecrd import KubeResourceBase
from apischema import schema



@dataclass
class LdapConfigPassword:
    value: Optional[str]
    secret: Optional

@dataclass
class LdapConfigCfgMap:
    pass


@dataclass
class LdapConfigServerConfig:
    url: str
    bindDN: str
    bindPassword: LdapConfigPassword



@dataclass
class LdapConfig(KubeResourceBase):
    __group__ = 'ldap.wopr.tech'
    __version__ = 'v1alpha1'

    serverConfig: LdapConfigServerConfig