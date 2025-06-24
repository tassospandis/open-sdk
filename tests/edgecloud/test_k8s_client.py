import unittest
from typing import Any, Dict
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.client import EdgeApplicationManager
import os

# class TestK8sEdgeApplicationManager(unittest.TestCase):

    # def setUp(self):
    #     kwargs={
    #             'PLATFORM_PROVIDER': 'ICOM',
    #             'KUBERNETES_MASTER_TOKEN': 'T3FRNnNVK25FY3I5ZHlNYmxrSEFpd2VPcW5WTlliTnRVNVo3bitNY1B3az0K',
    #             'KUBERNETES_MASTER_PORT': '16443',
    #             'EMP_STORAGE_URI': 'mongodb://mongopiedge:27017',
    #             'KUBERNETES_USERNAME': 'user'
    # }
    #     self.manager = EdgeApplicationManager(
    #         base_url= '146.124.106.200',
    #         **kwargs
    #     )


class TestK8sEdgeApplicationManager(unittest.TestCase):

    def setUp(self):
        
        IP_ADDRESS = "192.168.49.2" 

        TOKEN = os.environ.get("NEW_TOKEN")  # Use environment variable if set, else None

        if TOKEN is not None:
            TOKEN = os.environ["NEW_TOKEN"]  # Ensure this environment variable is set
            print(TOKEN)
        else:
            print("Environment variable 'NEW_TOKEN' is not set. Using TOKEN set in test_k8s_client.py")
            TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6InV4Z1VsMGFWd2JfMkxITFF6WGZkNkJLbkVaNWZFY0ZKWlVJVHZtR2ZFMVUifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzUwNjk3NDIyLCJpYXQiOjE3NTA2OTM4MjIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNDRlMjg2NjAtMzRjOC00OGJjLTg5N2MtNjE0NWZkYTA4NWYyIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJzdW5yaXNlNmciLCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoic2RrLXVzZXIiLCJ1aWQiOiI0MjU2ZDM3Yi03MjEzLTQwMDItYmI0Ny1lNjBhZWM4NGEzN2QifX0sIm5iZiI6MTc1MDY5MzgyMiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OnN1bnJpc2U2ZzpzZGstdXNlciJ9.hH4W_JIp6D_kgY988qSA30jESF1csVqYQzT9hqGV_DzcNE4vEfYo8SAz219cCdfv9P9LN8CRfBx9N5JUNuHvpi0Utc4__oRa5uhADgK6BUv6m1XKp-QJXFxDUEqzMK1EMEkevz7TPyAiJI63DDF6YY7ciPgPj8u8gWp-mBrsLUgikK0FbR9VPDT4MT5hYZcu-DiPCBeuOHWDcEzV_dekOk3xCgvACKZa0kUyvK04ZcoqElBe08sl8kZQxWmo4ooYmcUvUMRTyaFpjGMGYu86-OZ-KQIDlb3fQ07vHSg3Sdjx5NKc82i3Lc7rPpqThLl1G6OEVtiUL7Afn5Js_jiIfA"

        # --------------------------------------------------

        kwargs = {
                'PLATFORM_PROVIDER': 'MinikubeTest',
                'KUBERNETES_MASTER_TOKEN': TOKEN,
                'KUBERNETES_MASTER_PORT': '8443',
                'EMP_STORAGE_URI': 'mongodb://localhost:27017',
                'KUBERNETES_USERNAME': 'sdk-user'
        }
        self.manager = EdgeApplicationManager(
            base_url= IP_ADDRESS,
            **kwargs
        )

    def test_edge_cloud_zones_retrieval(self):        
        edge_cloud_zones = self.manager.get_edge_cloud_zones()
        print("Retrieved Zones:", edge_cloud_zones)
        self.assertTrue(edge_cloud_zones)
        self.assertIsInstance(edge_cloud_zones, list)



    def test_02_onboard_deploy(self):
        """
        Test 2: A complete integration test that performs all steps in order:
        1. Onboards an app to the database.
        2. Deploys the app to Kubernetes.
        """
        print("\n--- Running Test 2: Full Onboard, Deploy, and Verify Workflow ---")
        
        # --- ARRANGE ---
        deploymentlocation = "PATRAS"  # This should match the name of your Minikube zone
        app_name = "apacheiiboooioo1opatrastest"
        
        # APACHE MANIFEST
        camara_manifest = {
            "name": app_name,
            "packageType": "Container",
            "appRepo": {
                "imagePath": "httpd:2.4" 
            },
            "componentSpec": [
                {
                    "componentName": "apache-web-server",
                    "networkInterfaces": [
                        {"protocol": "TCP", "port": 80}
                    ]
                }
            ],
        }

        # # REDIS MANIFEST
        # camara_manifest = {
        #     "name": "my-redis-cache",
        #     "packageType": "Container",
        #     "appRepo": {
        #         "imagePath": "redis:7.0"  # Use a specific, stable version of Redis
        #     },
        #     "componentSpec": [
        #         {
        #             "componentName": "redis-server-container",
        #             # Redis listens on port 6379 by default
        #             "networkInterfaces": [
        #                 {"protocol": "TCP", "port": 6379}
        #             ]
        #         }
        #     ]
        # }

        # ENVIRONMENT VARIABLES MANIFEST
        # camara_manifest = {
        #     "name": "my-demo-app-with-env",
        #     "packageType": "Container",
        #     "appRepo": {
        #         # A special image from Google that displays app info and environment variables
        #         "imagePath": "gcr.io/google-samples/kubernetes-bootcamp:v1"
        #     },
        #     "componentSpec": [
        #         {
        #             "componentName": "demo-app-container",
        #             "networkInterfaces": [
        #                 {"protocol": "TCP", "port": 8080}
        #             ],
        #             # This is the new section we are testing
        #             "required_env_parameters": [
        #                 {"name": "MESSAGE"},
        #                 {"name": "APP_VERSION"}
        #             ]
        #         }
        #     ]
        # }

        # POSTGRES MANIFEST (testing persistency, networking, and environment variables) !not staying up, volume not created
        # camara_manifest = {
        #     "name": "postgres-db-app",
        #     "packageType": "Container",
        #     "appRepo": {
        #         "imagePath": "postgres:15"
        #     },
        #     "componentSpec": [
        #         {
        #             "componentName": "postgres-db-container",

        #             "networkInterfaces": [
        #                 {"protocol": "TCP", "port": 5432}
        #             ],

        #             "required_env_parameters": [
        #                 {
        #                     "name": "POSTGRES_PASSWORD",
        #                     "value": "password" 
        #                 }
        #             ],

        #             "required_volumes": [
        #                 {
        #                     "name": "postgres-data-storage",
        #                     "path": "/var/lib/postgresql/data" 
        #                 }
        #             ]
        #         }
        #     ]
        # }

        print("--> Step 1: Onboarding application...")
        onboard_response = self.manager.onboard_app(app_manifest=camara_manifest)
        app_id = onboard_response.get('appId')
        self.assertIsNotNone(app_id, "Onboarding failed, did not return an appId.")
        print(f"--> Onboarding successful. AppID: {app_id}")

        #!!!!!!
        #if the onboarding happens with the same name then onboarding will fail
        
        deployment_zones = [{"EdgeCloudZone": {"edgeCloudZoneName": deploymentlocation}}] #Set the deployment zone
        print(f"--> Step 2: Deploying app '{app_name}' to zone 'minikube'...")
        deploy_response = self.manager.deploy_app(app_id=app_id, app_zones=deployment_zones)
        self.assertIsNotNone(deploy_response, "Deploy command did not return a response.")
        print(f"--> Deployment command issued. Response: {deploy_response}")
        