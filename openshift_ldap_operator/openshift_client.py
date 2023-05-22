from kubernetes import client, config
from openshift.dynamic import DynamicClient

k8s_client = config.new_client_from_config()
ocp_client = DynamicClient(client=k8s_client)

# Now we specialize into every kind of resource we are interested in:
# v1 namespace configmap secret pod
# batch/v1 cronjob job
# apiextensions.k8s.io/v1 customresourcedefinition
# authorization.openshift.io/v1 clusterrole clusterrolebinding role rolebinding
# config.openshift.io/v1 oath
# image.openshift.io/v1 imagestream imagestreamtag
# user.openshift.io/v1 group user

class V1:
    Namespace: object  # TODO
    ConfigMap: object  # TODO
    Secret: object  # TODO
    Pod: object  # TODO


class BatchV1:
    CronJob: object  # TODO
    Job: object  # TODO


class K8ApiExtensionsV1:
    CustomResourceDefinition: object  # TODO


class OSAuthzV1:
    ClusterRole: object  # TODO
    ClusterRoleBinding: object  # TODO
    Role: object  # TODO
    RoleBinding: object  # TODO


class OSConfigV1:
    Oauth: object  # TODO


class OSImageV1:
    ImageStream: object  # TODO
    ImageStreamTag: object  # TODO


class OSUserV1:
    Group: object  # TODO
    User: object  # TODO
