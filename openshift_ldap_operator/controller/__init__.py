from typing import Optional

import kopf

from .. import openshift_client
from ..resources import *

# Kopf doesn't require a main function or anything like that, so we just start
# with declaring handlers!


@kopf.on.startup()  # type: ignore  # Apparently Pylance is gonna hate kopf...
def configure(settings: kopf.OperatorSettings, **kwargs):
    settings.persistence.finalizer = "ldap.wopr.tech/kopf-finalizer"
    settings.persistence.progress_storage = kopf.AnnotationsProgressStorage(
        prefix="ldap.wopr.tech",
        v1=False,
    )
    settings.persistence.diffbase_storage = kopf.AnnotationsDiffBaseStorage(
        prefix="ldap.wopr.tech",
        v1=False,
    )


@kopf.on.login()  # type: ignore
def login(**kwargs):
    return kopf.login_with_service_account(**kwargs)


@kopf.on.validate("ldap.wopr.tech", "LDAPConfig")  # type: ignore
def validate_ldapconfig_name(name: str, **kwargs):
    if name != "cluster":
        raise kopf.AdmissionError('Only allowed name is "cluster".', code=400)

@kopf.on.validate("ldap.wopr.tech", "LDAPConfig")  # type: ignore
def validate_ldapconfig_required(spec: dict, **kwargs):
    # TODO: all
    pass

@kopf.on.validate("ldap.wopr.tech", "LDAPConfig")  # type: ignore
def validate_ldapconfig_conflicts(spec: dict, **kwargs):
    # TODO: all
    pass

@kopf.on.create("ldap.wopr.tech", "LDAPConfig")  # type: ignore
async def create_ldapconfig(body: kopf.Body, **kwargs):
    kopf.info(body, reason="Created", message="Got a new cluster LDAP config!")

    conf: LdapConfig = LdapConfig._load(body)  # type: ignore

    ns = openshift_client.V1.Namespace.get(name="ldap-operator")
    if ns is None:
        openshift_client.V1.Namespace.create(
            body={
                "metadata": {
                    "name": "ldap-operator",
                    "ownerReferences": [
                        {
                            "apiVersion": conf.api_version,
                            "kind": conf.kind,
                            "name": "cluster",
                            "uid": conf.metadata['uid'],
                        }
                    ],
                },
            }
        )

    oauth = openshift_client.OSConfigV1.OAuth.get(name="cluster")
    if oauth is not None:
        oauthProviders = oauth.spec.identityProviders
        ldapProvider = None
        for prov in oauthProviders:
            if prov.type == "ldap" and prov.name == "ldap-operator":
                ldapProvider = prov
                break
        
        serverConfig = conf.spec.server_config
        userAttributes = conf.spec.user_search.attributes

        bindPass = serverConfig.bind_password.secret
        if serverConfig.bind_password.value is not None:
            bindPass = {
                "apiVersion": "v1",
                "kind": "Secret",
                "name": "ldap-operator-bindpass",
            }
            bindPassBody = {
                "metadata": {
                    "name": "ldap-operator-bindpass",
                    "ownerReferences": [
                        {
                            "apiVersion": conf.api_version,
                            "kind": conf.kind,
                            "name": "cluster",
                            "uid": conf.metadata['uid'],
                        }
                    ],
                },
                "type": "Opaque",
                "stringData": {
                    "bindPassword": serverConfig.bind_password.value,
                }
            }
            bindPassObj = openshift_client.V1.Secret.get(namespace="openshift-config", name="ldap-operator-bindpass")
            if bindPassObj is None:
                openshift_client.V1.Secret.create(namespace='openshift-config', body=bindPassBody)
            else:
                openshift_client.V1.Secret.replace(namespace='openshift-config', body=bindPassBody)

        provBody = {  # TODO: finish body
            "name": "ldap-operator",
            "type": "ldap",
            "ldap": {
                "attributes": {
                    "email": userAttributes.email,
                    "id": userAttributes.uid,
                    "name": userAttributes.display_name,
                    "preferredUsername": userAttributes.name,
                },
                "url": serverConfig.url,
                "insecure": serverConfig.insecure,
                "bindDN": serverConfig.bind_dn,
                "bindPassword": bindPass,
            },
        }
        
        if prov is None:
            pass # patch in new provider
        else:
            pass # patch in updated provider
        
    # TODO: handle all the others :upside_down_face:
