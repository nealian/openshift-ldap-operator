from inspect import get_annotations
from typing import Optional

from kubernetes import config
from kubernetes.dynamic.exceptions import NotFoundError
from openshift.dynamic import DynamicClient
from openshift.dynamic.exceptions import DynamicApiError

__all__ = [
    "V1",
    "BatchV1",
    "K8ApiExtensionsV1",
    "OSAuthzV1",
    "OSConfigV1",
    "OSImageV1",
    "OSUserV1",
]

# k8s_client = config.new_client_from_config()
k8s_client = config.load_incluster_config()
ocp_client = DynamicClient(client=k8s_client)


class AnnotatedDynamicClient:
    def __init__(self, api_version: str, kind: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__client = ocp_client.resources.get(api_version=api_version, kind=kind)

    def get(
        self,
        *,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        body: Optional[dict] = None,
        **kwargs,
    ):
        try:
            if name is not None or label_selector is not None or field_selector is not None:
                if body is not None:
                    raise DynamicApiError(
                        "Invalid API request; body cannot be defined at the same time as name, label_selector, or field_selector."
                    )
                return self.__client.get(
                    name=name,
                    namespace=namespace,
                    label_selector=label_selector,
                    field_selector=field_selector,
                    **kwargs,
                )
            elif body is not None:
                return self.__client.get(
                    body=body,
                    namespace=namespace,
                    **kwargs,
                )
            else:
                return self.__client.get(namespace=namespace, **kwargs)
        except NotFoundError:
            return None


    def create(
        self,
        *,
        body: dict,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        return self.__client.create(body=body, namespace=namespace, **kwargs)

    def delete(
        self,
        *,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        body: Optional[dict] = None,
        **kwargs,
    ):
        if name is not None or label_selector is not None or field_selector is not None:
            if body is not None:
                raise DynamicApiError(
                    "Invalid API request; body cannot be defined at the same time as name, label_selector, or field_selector."
                )
            return self.__client.delete(
                name=name,
                namespace=namespace,
                label_selector=label_selector,
                field_selector=field_selector,
                **kwargs,
            )
        elif body is not None:
            return self.__client.delete(
                body=body,
                namespace=namespace,
                **kwargs,
            )

    def patch(
        self,
        *,
        body: Optional[dict] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        return self.__client.patch(body=body, namespace=namespace, **kwargs)

    def replace(
        self,
        *,
        body: Optional[dict] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        return self.__client.replace(body=body, namespace=namespace, **kwargs)

    def watch(
        self,
        *,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        resource_version: Optional[str] = None,
        timeout: Optional[int | str] = None,
        **kwargs,
    ):
        return self.__client.watch(
            name=name,
            namespace=namespace,
            label_selector=label_selector,
            field_selector=field_selector,
            resource_version=resource_version,
            timeout=timeout,
            **kwargs,
        )


class AnnotatedDynamicClientParent:
    def __init_subclass__(cls) -> None:
        vers: str = getattr(cls, "__api_version__")
        for k, v in get_annotations(cls).items():
            if v == AnnotatedDynamicClient and getattr(cls, k, None) is None:
                client = AnnotatedDynamicClient(api_version=vers, kind=k)
                setattr(cls, k, client)


# Now we specialize into every kind of resource we are interested in:
# v1 namespace configmap secret pod
# batch/v1 cronjob job
# apiextensions.k8s.io/v1 customresourcedefinition
# authorization.openshift.io/v1 clusterrole clusterrolebinding role rolebinding
# config.openshift.io/v1 oauth
# image.openshift.io/v1 imagestream imagestreamtag
# user.openshift.io/v1 group user


class V1(AnnotatedDynamicClientParent):
    __api_version__ = "v1"
    Namespace: AnnotatedDynamicClient
    ConfigMap: AnnotatedDynamicClient
    Secret: AnnotatedDynamicClient
    Pod: AnnotatedDynamicClient


class BatchV1(AnnotatedDynamicClientParent):
    __api_version__ = "batch/v1"
    CronJob: AnnotatedDynamicClient
    Job: AnnotatedDynamicClient


class K8ApiExtensionsV1(AnnotatedDynamicClientParent):
    __api_version__ = "apiextensions.k8s.io/v1"
    CustomResourceDefinition: AnnotatedDynamicClient


class OSAuthzV1(AnnotatedDynamicClientParent):
    __api_version__ = "authorization.openshift.io/v1"
    ClusterRole: AnnotatedDynamicClient
    ClusterRoleBinding: AnnotatedDynamicClient
    Role: AnnotatedDynamicClient
    RoleBinding: AnnotatedDynamicClient


class OSConfigV1(AnnotatedDynamicClientParent):
    __api_version__ = "config.openshift.io/v1"
    OAuth: AnnotatedDynamicClient


class OSImageV1(AnnotatedDynamicClientParent):
    __api_version__ = "image.openshift.io/v1"
    ImageStream: AnnotatedDynamicClient
    ImageStreamTag: AnnotatedDynamicClient


class OSUserV1(AnnotatedDynamicClientParent):
    __api_version__ = "user.openshift.io/v1"
    Group: AnnotatedDynamicClient
    User: AnnotatedDynamicClient
