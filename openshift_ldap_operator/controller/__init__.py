import kopf

# Kopf doesn't require a main function or anything like that, so we just start
# with declaring handlers!


@kopf.on.login()  # type: ignore  # Apparently Pylance is gonna hate kopf...
def login_fn(**kwargs):
    return kopf.login_with_service_account(**kwargs)


