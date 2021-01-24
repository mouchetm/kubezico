import time

from flask import Flask, jsonify, request

from kubernetes import client, config

app = Flask(__name__)

RESOURCE_CLIENT = {
    "pod": "base",
    "event": "base",
    "config_map": "base",
    "secret": "base",
    "resource_quota": "base",
    "ingress": "base",
    "service": "base",
    "node": "base",
    "deployment": "apps",
    "job": "batch"

}

OBJECT_TO_CLIENT = {
    "base": "CoreV1Api",
    "extension": "ExtensionsV1beta1Api",
    "custom": "CustomObjectsApi",
    "batch": "BatchV1Api",
    "apps": "AppsV1Api"
}

KUBECONFIG_PATH = "/Users/mmouchet/.kube/config"

def __get_kube_client(object_type="base", kube_config="/Users/mmouchet/.kube/config"):
    config.load_kube_config(kube_config)
    api_client = client.ApiClient()
    client_name = OBJECT_TO_CLIENT[object_type]
    get_client_method = getattr(client, client_name)
    kube_client = get_client_method(api_client)
    return kube_client

def get_pod_logs(pod_name, pod_namespace, container):
    client = __get_kube_client("base", KUBECONFIG_PATH)
    api_response = client.read_namespaced_pod_log(name=pod_name, namespace=pod_namespace, container=container)
    return api_response.split("\n")


def get_resource(resource_type=None, namespace=None, name=None, container=None):
    if not resource_type:
        return []
    if resource_type == "log":
        return get_pod_logs(name, namespace, container)
    client = __get_kube_client(RESOURCE_CLIENT[resource_type], KUBECONFIG_PATH)
    if namespace:
        method_name = f"list_namespaced_{resource_type}"
        get_resources_method = getattr(client, method_name)
        resources = get_resources_method(namespace=namespace)
    else:
        method_name = f"list_{resource_type}_for_all_namespaces"
        get_resources_method = getattr(client, method_name)
        resources = get_resources_method()

    return [item.to_dict() for item in resources.items]
    

@app.route('/api/')
def api():
    resource_type = request.args.get('resource-type')
    name = request.args.get('name')
    namespace = request.args.get('namespace')
    container = request.args.get('container')
    resp = jsonify(get_resource(resource_type=resource_type, namespace=namespace, name=name, container=container))
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


if __name__ == "__main__":
    # Use create app factory with pyinstaller?
    app.run()