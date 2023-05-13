from dataclasses import dataclass, field
from uuid import UUID
from typing import Optional
from kubecrd import KubeResourceBase # maybe try something else though because we can't add status to these
from apischema import schema


@dataclass
class K8sDataRef:
    name: str = field(
        metadata=schema(

        )
    )
    key: str = field(
        metadata=schema(

        )
    )


@dataclass
class LdapConfigPassword:
    value: Optional[str] = field(
        metadata=schema(
            
        )
    )
    secret: K8sDataRef = field(
        metadata=schema(

        ),
    )

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