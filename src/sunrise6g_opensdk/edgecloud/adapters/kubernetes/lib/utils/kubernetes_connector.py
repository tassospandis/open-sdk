from __future__ import (
    print_function,
)
import requests

from kubernetes import (
    client,
)
from kubernetes.client.rest import (
    ApiException,
)
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.utils import (
    auxiliary_functions,
)
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.utils.connector_db import (
    ConnectorDB,
)

configuration = client.Configuration()


class KubernetesConnector:
    def __init__(self, ip, port, token, username):
        master_node_ip = ip
        master_node_port = port
        username = username
        self.token_k8s = token
        self.host = "https://" + master_node_ip + ":" + master_node_port
        configuration.api_key["authorization"] = self.token_k8s
        configuration.api_key_prefix["authorization"] = "Bearer"

        configuration.host = self.host

        configuration.username = username
        configuration.verify_ssl = False
        self.v1 = client.CoreV1Api(client.ApiClient(configuration))

        # config.lod
        # client.Configuration.set_default(configuration)
        # Defining host is optional and default to http://localhost
        # Enter a context with an instance of the API kubernetes.client
        with client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            self.api_instance = client.AdmissionregistrationApi(api_client)
            self.api_instance_appsv1 = client.AppsV1Api(api_client)
            self.api_instance_apiregv1 = client.ApiregistrationV1Api(api_client)
            self.api_instance_v1autoscale = client.AutoscalingV1Api(api_client)
            self.api_instance_v2beta1autoscale = client.AutoscalingV2Api(
                api_client
            )
            self.api_instance_v2beta2autoscale = client.AutoscalingV2Api(
                api_client
            )
            self.api_instance_corev1api = client.CoreV1Api(api_client)
            self.api_instance_storagev1api = client.StorageV1Api(api_client)
            self.api_instance_batchv1 = client.BatchV1Api(api_client)

            self.api_custom = client.CustomObjectsApi(api_client)
            try:
                self.api_instance.get_api_group()
            except ApiException as e:
                print(
                    "Exception when calling AdmissionregistrationApi->get_api_group: %s\n"
                    % e
                )

    def get_node_details(self, nodeName):
        try:
            url = self.host + "/api/v1/nodes/" + nodeName
            headers = {"Authorization": "Bearer " + self.token_k8s}
            x = requests.get(url, headers=headers, verify=False)
            node_details = x.json()
            return node_details
        except requests.exceptions.HTTPError as e:
            # logging.error(traceback.format_exc())
            return "Exception when calling Kubernetes API:" + e.args

    def get_PoP_statistics(self, nodeName):

        # x1 = v1.list_node().to_dict()

        try:
            url = self.host + "/api/v1/nodes"
            headers = {"Authorization": "Bearer " + self.token_k8s}
            x = requests.get(url, headers=headers, verify=False)
            x1 = x.json()
        except requests.exceptions.HTTPError as e:
            # logging.error(traceback.format_exc())
            return (
                "Exception when calling CoreV1Api->/api/v1/namespaces/sunrise6g/persistentvolumeclaims: %s\n"
                % e
            )
        k8s_nodes = self.api_custom.list_cluster_custom_object(
            "metrics.k8s.io", "v1beta1", "nodes"
        )
        pop_output = {}
        for pop in x1["items"]:

            name = pop["metadata"]["name"]
            if name == nodeName:
                pop_output["nodeName"] = name
                pop_output["nodeId"] = pop["metadata"]["uid"]
                pop_output["nodeLocation"] = pop["metadata"]["labels"]["location"]

                node_addresses = {}
                node_addresses["nodeHostName"] = pop["status"]["addresses"][1][
                    "address"
                ]
                node_addresses["nodeExternalIP"] = pop["status"]["addresses"][0][
                    "address"
                ]
                node_addresses["nodeInternalIP"] = pop["metadata"]["annotations"][
                    "projectcalico.org/IPv4VXLANTunnelAddr"
                ]
                pop_output["nodeAddresses"] = node_addresses

                node_conditions = {}
                for condition in pop["status"]["conditions"]:
                    type = condition["type"]
                    node_type = "node" + type
                    node_conditions[node_type] = condition["status"]
                pop_output["nodeConditions"] = node_conditions

                node_capacity = {}
                node_capacity["nodeCPUCap"] = pop["status"]["capacity"]["cpu"]
                memory = pop["status"]["capacity"]["memory"]
                memory_size = len(memory)
                node_capacity["nodeMemoryCap"] = memory[: memory_size - 2]
                node_capacity["nodeMemoryCapMU"] = memory[-2:]
                storage = pop["status"]["capacity"]["ephemeral-storage"]
                storage_size = len(storage)
                node_capacity["nodeStorageCap"] = storage[: storage_size - 2]
                node_capacity["nodeStorageCapMU"] = storage[-2:]
                node_capacity["nodeMaxNoofPods"] = pop["status"]["capacity"]["pods"]
                pop_output["nodeCapacity"] = node_capacity

                node_allocatable_resources = {}
                node_allocatable_resources["nodeCPUCap"] = pop["status"]["allocatable"][
                    "cpu"
                ]
                memory = pop["status"]["allocatable"]["memory"]
                memory_size = len(memory)
                node_allocatable_resources["nodeMemoryCap"] = memory[: memory_size - 2]
                node_allocatable_resources["nodeMemoryCapMU"] = memory[-2:]
                storage = pop["status"]["allocatable"]["ephemeral-storage"]
                storage_size = len(storage)
                node_allocatable_resources["nodeStorageCap"] = storage[
                    : storage_size - 2
                ]
                node_allocatable_resources["nodeStorageCapMU"] = storage[-2:]
                # node_allocatable_resources["nodeMaxNoofPods"] = pop['status']['allocatable']['pods']
                pop_output["nodeAllocatableResources"] = node_allocatable_resources

                # calculate usage
                for stats in k8s_nodes["items"]:
                    if stats["metadata"]["name"] == nodeName:
                        node_usage = {}
                        cpu = stats["usage"]["cpu"]
                        cpu_size = len(cpu)
                        memory = stats["usage"]["memory"]
                        memory_size = len(memory)

                        node_usage["nodeMemoryInUse"] = memory[: memory_size - 2]
                        node_usage["nodeMemoryInUseMU"] = memory[-2:]
                        node_usage["nodeMemoryUsage"] = int(
                            node_usage["nodeMemoryInUse"]
                        ) / int(node_capacity["nodeMemoryCap"])
                        node_usage["nodeCPUInUse"] = cpu[: cpu_size - 1]
                        node_usage["nodeCPUInUseMU"] = cpu[-1:]
                        node_usage["nodeCPUUsage"] = int(node_usage["nodeCPUInUse"]) / (
                            int(node_capacity["nodeCPUCap"]) * 1000
                        )
                        pop_output["nodeUsage"] = node_usage

                node_general_info = {}
                node_general_info["nodeOS"] = pop["status"]["nodeInfo"]["osImage"]
                node_general_info["nodeKubernetesVersion"] = pop["status"]["nodeInfo"][
                    "kernelVersion"
                ]
                node_general_info["nodecontainerRuntimeVersion"] = pop["status"][
                    "nodeInfo"
                ]["containerRuntimeVersion"]
                node_general_info["nodeKernelVersion"] = pop["status"]["nodeInfo"][
                    "kernelVersion"
                ]
                node_general_info["nodeArchitecture"] = pop["status"]["nodeInfo"][
                    "architecture"
                ]
                pop_output["nodeGeneralInfo"] = node_general_info

        return pop_output

    def delete_service_function(self, connector_db: ConnectorDB, service_function_name):

        self.api_instance_appsv1.delete_namespaced_deployment(
            name=service_function_name, namespace="sunrise6g"
        )

        self.v1.delete_namespaced_service(
            name=service_function_name, namespace="sunrise6g"
        )

        hpa_list = (
            self.api_instance_v1autoscale.list_namespaced_horizontal_pod_autoscaler(
                "sunrise6g"
            )
        )

        # hpas=hpa_list["items"]

        for hpa in hpa_list.items:
            if hpa.metadata.name == service_function_name:
                self.api_instance_v1autoscale.delete_namespaced_horizontal_pod_autoscaler(
                    name=service_function_name, namespace="sunrise6g"
                )
                break
        # deletevolume
        volume_list = self.v1.list_namespaced_persistent_volume_claim("sunrise6g")
        for volume in volume_list.items:
            name_v = service_function_name + str("-")
            if name_v in volume.metadata.name:
                self.v1.delete_persistent_volume(
                    name=volume.spec.volume_name
                )

                self.v1.delete_namespaced_persistent_volume_claim(
                    name=volume.metadata.name, namespace="sunrise6g"
                )

        doc = {}
        doc["instance_name"] = service_function_name
        connector_db.delete_document_deployed_service_functions(document=doc)

    def deploy_service_function(self, descriptor_service_function):
        # deploys a Deployment yaml file, a service, a pvc and a hpa
        # logging.info('DESCRIPTOR: '+descriptor_service_function)
        # logging.info(descriptor_service_function)
        if "volumes" in descriptor_service_function:
            for volume in descriptor_service_function["volumes"]:
                # first solution (python k8s client raises error without reason!)
                # body_volume = create_pvc(descriptor_service_function["name"], volume)
                # api_response_pvc = v1.create_namespaced_persistent_volume_claim("sunrise6g", body_volume)

                # #deploy pv
                # print("deploy pv")
                # try:
                #     url = host + "/api/v1/persistentvolumes"
                #     body_volume = create_pv_dict(descriptor_service_function["name"], volume)
                #
                #
                #     headers = {"Authorization": "Bearer " + token_k8s}
                #     x = requests.post(url, headers=headers, json=body_volume, verify=False)
                #     print (x.status_code)
                # except requests.exceptions.HTTPError as e:
                #     # logging.error(traceback.format_exc())
                #     return ("Exception when calling CoreV1Api->/api/v1/persistentvolumes: %s\n" % e)

                # deploy pvc

                if volume.get("hostpath") is None:
                    try:
                        url = (
                            self.host
                            + "/api/v1/namespaces/sunrise6g/persistentvolumeclaims"
                        )
                        body_volume = self.create_pvc_dict(
                            descriptor_service_function["name"], volume
                        )
                        headers = {"Authorization": "Bearer " + self.token_k8s}
                        requests.post(
                            url, headers=headers, json=body_volume, verify=False
                        )
                    except requests.exceptions.HTTPError as e:
                        # logging.error(traceback.format_exc())
                        return (
                            "Exception when calling CoreV1Api->/api/v1/namespaces/sunrise6g/persistentvolumeclaims: %s\n"
                            % e
                        )

            # api_response_pvc = api_instance_corev1api.create_namespaced_persistent_volume_claim
        body_deployment = self.create_deployment(descriptor_service_function)
        body_service = self.create_service(descriptor_service_function)

        try:
            api_response_deployment = (
                self.api_instance_appsv1.create_namespaced_deployment(
                    "sunrise6g", body_deployment
                )
            )
            # api_response_service = api_instance_apiregv1.create_api_service(body_service)
            self.v1.create_namespaced_service(
                "sunrise6g", body_service
            )
            if "autoscaling_policies" in descriptor_service_function:
                # V1 AUTOSCALER
                body_hpa = self.create_hpa(descriptor_service_function)
                self.api_instance_v1autoscale.create_namespaced_horizontal_pod_autoscaler(
                    "sunrise6g", body_hpa
                )
            # V2beta1 AUTOSCALER
            # body_hpa = create_hpa(descriptor_paas)
            # api_instance_v2beta1autoscale.create_namespaced_horizontal_pod_autoscaler("sunrise6g",body_hpa)
            # body_r = (
            #     "Service "
            #     + descriptor_service_function["name"]
            #     + " deployed successfully"
            # )
            return api_response_deployment
        except ApiException as e:
            # logging.error(traceback.format_exc())
            return (
                "Exception when calling AppsV1Api->create_namespaced_deployment or ApiregistrationV1Api->create_api_service: %s\n"
                % e
            )
   
    def create_deployment(self, descriptor_service_function):

        metadata = client.V1ObjectMeta(name=descriptor_service_function["name"])
        # selector
        dict_label = {}
        dict_label["sunrise6g"] = descriptor_service_function["name"]
        selector = client.V1LabelSelector(match_labels=dict_label)

        # create spec

        # spec.selector=selector
        # replicas
        # spec.replicas=descriptor_paas("count-min")
        # template

        metadata_spec = client.V1ObjectMeta(labels=dict_label)

        # template spec
        containers = []
        for container in descriptor_service_function["containers"]:
            # privileged
            if "privileged" in container:
                security_context = client.V1SecurityContext(
                    privileged=container["privileged"]
                )
            else:
                security_context = None
            ports = []
            for port_id in container["application_ports"]:
                port_ = client.V1ContainerPort(container_port=port_id)
                ports.append(port_)

            # check env_parameters
            envs = []

            if "env_parameters" in descriptor_service_function:
                if descriptor_service_function["env_parameters"] is not None:

                    for env in descriptor_service_function["env_parameters"]:
                        if "value" in env:
                            env_ = client.V1EnvVar(name=env["name"], value=env["value"])
                        elif "value_ref" in env:
                            # env_name_ should based on paas_instance_name
                            if "paas_name" in descriptor_service_function:
                                # check if value is something like:  http://edgex-core-data:48080

                                env_split = env["value_ref"].split(":")

                                if (
                                    "@" not in env["value_ref"]
                                ):  # meaning  that it is reffering to a running paas!!!!!

                                    if (
                                        len(env_split) > 2
                                    ):  # case http://edgex-core-data:48080
                                        prefix = env_split[0]  # http
                                        final_env = env_split[
                                            1
                                        ]  # //edgex-core-data or edgex-core-data
                                        split2 = final_env.split("//")
                                        if len(split2) >= 2:
                                            final_env = split2[1]
                                        port_env = env_split[2]  # 48080
                                        env_ = auxiliary_functions.prepare_name_for_k8s(
                                            str(
                                                descriptor_service_function["paas_name"]
                                                + str("-")
                                                + final_env
                                            )
                                        )

                                        env_name_ = (
                                            prefix + ":" + "//" + env_ + ":" + port_env
                                        )

                                    elif (
                                        len(env_split) > 1
                                    ):  # case edgex-core-data:48080
                                        final_env = env_split[0]
                                        port_env = env_split[1]
                                        env_ = auxiliary_functions.prepare_name_for_k8s(
                                            str(
                                                descriptor_service_function["paas_name"]
                                                + str("-")
                                                + final_env
                                            )
                                        )
                                        env_name_ = env_ + ":" + port_env
                                    else:  # case edgex-core-data
                                        final_env = env_split[0]
                                        env_name_ = (
                                            auxiliary_functions.prepare_name_for_k8s(
                                                str(
                                                    descriptor_service_function[
                                                        "paas_name"
                                                    ]
                                                    + str("-")
                                                    + final_env
                                                )
                                            )
                                        )
                                    env_ = client.V1EnvVar(
                                        name=env["name"], value=env_name_
                                    )

                        envs.append(env_)

            # create volumes
            volumes = []
            volume_mounts = []
            if "volumes" in descriptor_service_function:
                if descriptor_service_function["volumes"] is not None:

                    for volume in descriptor_service_function["volumes"]:

                        if volume.get("hostpath") is None:

                            pvc = client.V1PersistentVolumeClaimVolumeSource(
                                claim_name=str(
                                    descriptor_service_function["name"]
                                    + str("-")
                                    + volume["name"]
                                )
                            )
                            # volume_=client.V1Volume(name=volume["name"], persistent_volume_claim=pvc)
                            volume_ = client.V1Volume(
                                name=str(
                                    descriptor_service_function["name"]
                                    + str("-")
                                    + volume["name"]
                                ),
                                persistent_volume_claim=pvc,
                            )

                            volumes.append(volume_)

                        else:
                            hostpath = client.V1HostPathVolumeSource(
                                path=volume["hostpath"]
                            )
                            volume_ = client.V1Volume(
                                name=str(
                                    descriptor_service_function["name"]
                                    + str("-")
                                    + volume["name"]
                                ),
                                host_path=hostpath,
                            )
                            volumes.append(volume_)

                        volume_mount = client.V1VolumeMount(
                            name=str(
                                descriptor_service_function["name"]
                                + str("-")
                                + volume["name"]
                            ),
                            mount_path=volume["path"],
                        )
                        volume_mounts.append(volume_mount)

            if "autoscaling_policies" in descriptor_service_function:
                limits_dict = {}
                request_dict = {}
                for auto_scale_policy in descriptor_service_function[
                    "autoscaling_policies"
                ]:
                    limits_dict[auto_scale_policy["metric"]] = auto_scale_policy[
                        "limit"
                    ]
                    request_dict[auto_scale_policy["metric"]] = auto_scale_policy[
                        "request"
                    ]

                resources = client.V1ResourceRequirements(
                    limits=limits_dict, requests=request_dict
                )
                if not envs:
                    con = client.V1Container(
                        name=descriptor_service_function["name"],
                        image=container["image"],
                        ports=ports,
                        image_pull_policy="Always",
                        resources=resources,
                        volume_mounts=volume_mounts if volume_mounts else None,
                        security_context=security_context,
                    )
                else:
                    con = client.V1Container(
                        name=descriptor_service_function["name"],
                        image=container["image"],
                        ports=ports,
                        image_pull_policy="Always",
                        resources=resources,
                        env=envs,
                        volume_mounts=volume_mounts if volume_mounts else None,
                        security_context=security_context,
                    )
            else:
                if not envs:
                    con = client.V1Container(
                        name=descriptor_service_function["name"],
                        image=container["image"],
                        ports=ports,
                        image_pull_policy="Always",
                        volume_mounts=volume_mounts if volume_mounts else None,
                        security_context=security_context,
                    )
                else:
                    con = client.V1Container(
                        name=descriptor_service_function["name"],
                        image=container["image"],
                        image_pull_policy="Always",
                        ports=ports,
                        env=envs,
                        volume_mounts=volume_mounts if volume_mounts else None,
                        security_context=security_context,
                    )

            containers.append(con)

        pod_spec_args = {
            "containers": containers,
            "hostname": descriptor_service_function["name"],
            "restart_policy": "Always",
            "volumes": None if not volumes else volumes,
        }

        location = descriptor_service_function.get("location")
        if location:
            pod_spec_args["node_selector"] = {"location": location}

        template_spec_ = client.V1PodSpec(**pod_spec_args)

        template = client.V1PodTemplateSpec(metadata=metadata_spec, spec=template_spec_)

        spec = client.V1DeploymentSpec(
            selector=selector,
            template=template,
            replicas=descriptor_service_function.get("count-min", 1),
        )

        body = client.V1Deployment(
            api_version="apps/v1", kind="Deployment", metadata=metadata, spec=spec
        )
        return body
 
    
    def get_deployed_service_functions(self, connector_db: ConnectorDB):
        # label_selector = {}
        # deployed_hpas=get_deployed_hpas()
        #

        # SHOULD UNCOMMENT IT IF WE WOULD LIKE LIVE UPDATE OF A RUNNING PAAS SERVICE
        # if deployed_hpas:
        #     check_for_update_hpas(deployed_hpas)
        ##########
        api_response = self.api_instance_appsv1.list_namespaced_deployment("sunrise6g")

        api_response_service = self.v1.list_namespaced_service("sunrise6g")
        api_response_pvc = self.v1.list_namespaced_persistent_volume_claim("sunrise6g")

        #
        # hpa_list = api_instance_v1autoscale.list_namespaced_horizontal_pod_autoscaler("sunrise6g")
        # api_response_pod = v1.list_namespaced_pod("sunrise6g")
        #
        apps = []
        for app in api_response.items:
            metadata = app.metadata
            spec = app.spec
            status = app.status
            app_ = {}
            apps_col = connector_db.get_documents_from_collection(
                collection_input="service_functions"
            )
            deployed_apps_col = connector_db.get_documents_from_collection(
                collection_input="deployed_service_functions"
            )
            actual_name = None
            for app_col in deployed_apps_col:
                if metadata.name == app_col["instance_name"]:
                    app_["service_function_instance_name"] = app_col["instance_name"]
                    app_["uid"] = metadata.uid
                    actual_name = app_col["name"]
                    # app_["appid"] = app_col["_id"]
                    
                    break
            for app_col in apps_col:
                if actual_name == app_col["name"]:
                    app_["service_function_catalogue_name"] = app_col["name"]
                    app_['id'] = app_col.get('_id')
                    app_['appProvider'] = app_col.get('appProvider')
                    # app_["appid"] = app_col["_id"]
                    break
            
            if app_:  # if app_ is not empty

                if (status.available_replicas is not None) and (
                    status.ready_replicas is not None
                ):
                    if status.available_replicas >= 1 and status.ready_replicas >= 1:
                        app_["status"] = "running"
                        app_["replicas"] = status.ready_replicas
                    else:
                        app_["status"] = "not_running"
                        app_["replicas"] = 0
                else:
                    app_["status"] = "not_running"
                    app_["replicas"] = 0

                # we need to find the compute node
                if (
                    spec.template.spec.node_selector is not None
                ):  # giati kati mporei na min exei node selector
                    if "location" in spec.template.spec.node_selector.keys():
                        location = spec.template.spec.node_selector["location"]
                        nodes = connector_db.get_documents_from_collection(
                            collection_input="points_of_presence"
                        )
                        for node in nodes:
                            if location == node["location"]:
                                app_["node_name"] = node["name"]
                                app_["node_id"] = node["_id"]
                                app_["location"] = node["location"]
                                break

                for app_service in api_response_service.items:
                    metadata_svc = app_service.metadata
                    spec_svc = app_service.spec
                    svc_ports = []
                    if metadata_svc.name == app_["service_function_instance_name"]:

                        for port in spec_svc.ports:
                            port_ = {}
                            if port.node_port is not None:

                                port_["exposed_port"] = port.node_port
                                port_["protocol"] = port.protocol
                                port_["application_port"] = port.port
                                svc_ports.append(port_)
                            else:
                                port_["protocol"] = port.protocol
                                port_["application_port"] = port.port
                                svc_ports.append(port_)
                        app_["ports"] = svc_ports
                        break

                apps.append(app_)

        return apps

    def create_service(self, descriptor_service_function):
        dict_label = {}
        dict_label["sunrise6g"] = descriptor_service_function["name"]
        metadata = client.V1ObjectMeta(
            name=descriptor_service_function["name"], labels=dict_label
        )

        #  spec

        if (
            "exposed_ports" in descriptor_service_function["containers"][0]
        ):  # create NodePort svc object
            ports = []
            hepler = 0
            for port_id in descriptor_service_function["containers"][0][
                "exposed_ports"
            ]:

                ports_ = client.V1ServicePort(
                    port=port_id, target_port=port_id, name=str(port_id)
                )
                ports.append(ports_)
                hepler = hepler + 1
            spec = client.V1ServiceSpec(
                selector=dict_label, ports=ports, type="NodePort"
            )
        # body = client.V1Service(api_version="v1", kind="Service", metadata=metadata, spec=spec)
        else:  # create ClusterIP svc object
            ports = []
            for port_id in descriptor_service_function["containers"][0][
                "application_ports"
            ]:
                ports_ = client.V1ServicePort(
                    port=port_id, target_port=port_id, name=str(port_id)
                )
                ports.append(ports_)
            spec = client.V1ServiceSpec(
                selector=dict_label, ports=ports, type="ClusterIP"
            )
        body = client.V1Service(
            api_version="v1", kind="Service", metadata=metadata, spec=spec
        )

        return body

    def get_PoPs(self):

        try:
            pops_ = []
            x1 = self.v1.list_node()
            for node in x1.items:
                pop_ = {}
                pop_["name"] = node.metadata.name
                pop_["uid"] = node.metadata.uid
                pop_["location"] = node.metadata.labels.get("location")
                pop_["serial"] = node.status.addresses[0].address
                pop_["node_type"] = node.metadata.labels.get("node_type")
                pop_["status"] = (
                    "active"
                    if node.status.conditions[-1].status == "True"
                    else "inactive"
                )
                # pop_= NodesResponse(id=uid,name=name,location=location,serial=address, node_type=node_type, status=ready_status)
                pops_.append(pop_)
            return pops_
        # url = host + "/api/v1/nodes"
        # headers = {"Authorization": "Bearer " + token_k8s}
        # x=requests.get(url, headers=headers, verify=False)
        # x1 = x.json()
        except requests.exceptions.HTTPError as e:
            # logging.error(traceback.format_exc())
            return (
                "Exception when calling CoreV1Api->/api/v1/namespaces/sunrise6g/persistentvolumeclaims: %s\n"
                % e
            )


def create_pvc(name, volumes):
    dict_label = {}
    name_vol = name + str("-") + volumes["name"]
    dict_label["sunrise6g"] = name_vol
    # metadata = client.V1ObjectMeta(name=name_vol)
    metadata = client.V1ObjectMeta(name=name_vol, labels=dict_label)
    # api_version = ("v1",)
    kind = ("PersistentVolumeClaim",)
    spec = client.V1PersistentVolumeClaimSpec(
        access_modes=["ReadWriteMany"],
        resources=client.V1ResourceRequirements(
            requests={"storage": volumes["storage"]}
        ),
    )
    body = client.V1PersistentVolumeClaim(
        api_version="v1", kind=kind, metadata=metadata, spec=spec
    )

    return body


def create_pvc_dict(name, volumes, storage_class="microk8s-hostpath", volume_name=None):
    name_vol = name + str("-") + volumes["name"]
    # body={}
    # body["api_version"]="v1"
    # body["kind"]="PersistentVolumeClaim"
    # metadata={}
    # labels={}
    body = {
        "api_version": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {"labels": {"sunrise6g": name_vol}, "name": name_vol},
        "spec": {
            "accessModes": ["ReadWriteOnce"],
            "resources": {"requests": {"storage": volumes["storage"]}},
            "storageClassName": storage_class,
        },
    }

    if volume_name is not None:
        body["spec"]["volume_name"] = volume_name

    return body


def create_pv_dict(name, volumes, storage_class, node=None):
    name_vol = name + "-" + volumes["name"]

    body = {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
            "name": name_vol,
            "labels": {
                "sunrise6g": name_vol,
            },
        },
        "spec": {
            "capacity": {"storage": volumes["storage"]},
            "volumeMode": "Filesystem",
            "accessModes": ["ReadWriteOnce"],
            "persistentVolumeReclaimPolicy": "Delete",
            "storageClassName": storage_class,
            "hostPath": {"path": "/mnt/" + name_vol, "type": "DirectoryOrCreate"},
        },
    }

    if node is not None:
        body["spec"]["nodeAffinity"] = {
            "required": {
                "nodeSelectorTerms": [
                    {
                        "matchExpressions": [
                            {
                                "key": "kubernetes.io/hostname",
                                "operator": "In",
                                "values": [node],
                            }
                        ]
                    }
                ]
            }
        }

    return body

def create_hpa(descriptor_service_function):

    # V1!!!!!!!

    dict_label = {}
    dict_label["name"] = descriptor_service_function["name"]
    client.V1ObjectMeta(
        name=descriptor_service_function["name"], labels=dict_label
    )

    #  spec

    scale_target = client.V1CrossVersionObjectReference(
        api_version="apps/v1",
        kind="Deployment",
        name=descriptor_service_function["name"],
    )

    # todo!!!! check 0 gt an exoume kai cpu k ram auto dn tha einai auto to version!
    client.V1HorizontalPodAutoscalerSpec(
        max_replicas=descriptor_service_function["count-max"],
        min_replicas=descriptor_service_function["count-min"],
        target_cpu_utilization_percentage=int(
            descriptor_service_function["autoscaling_policies"][0]["util_percent"]
        ),
        scale_target_ref=scale_target,
    )
    # body = client.V1HorizontalPodAutoscaler(
    #     api_version="autoscaling/v1",
    #     kind="HorizontalPodAutoscaler",
    #     metadata=metadata,
    #     spec=spec,
    # )
