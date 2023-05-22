from typing import Optional

import kopf

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


@kopf.on.create("ldap.wopr.tech", "LDAPConfig")  # type: ignore
async def create_ldapconfig(body: kopf.Body, **kwargs):
    kopf.info(body, reason="Created", message="Got a new cluster LDAP config!")

    
