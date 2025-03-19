from typing import Optional
from src.edgecloud.core.edgecloud_interface import EdgeCloudManagementInterface
from typing import Dict, List, Optional
from .common import I2EdgeError, i2edge_delete, i2edge_get, i2edge_post, i2edge_post_multiform_data

class EdgeApplicationManager(EdgeCloudManagementInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_edge_cloud_zones(self) -> list[dict]:
        url = "{}/zones/list".format(self.base_url)
        try:
            response = i2edge_get(url, params=None)
            return response
        except I2EdgeError as e:
            raise e

    def onboard_app(self, app_manifest: Dict) -> Dict:
        print(f"Submitting application: {app_manifest}")
        return {"appId": "1234-5678"}

    def get_all_onboarded_apps(self) -> List[Dict]:
        return [{"appId": "1234-5678", "name": "TestApp"}]

    def get_onboarded_app(self, app_id: str) -> Dict:
        return {"appId": app_id, "name": "TestApp"}

    def delete_onboarded_app(self, app_id: str) -> None:
        print(f"Deleting application: {app_id}")

    def deploy_app(self, app_id: str, app_zones: List[Dict]) -> Dict:
        return {"appInstanceId": "abcd-efgh"}

    def get_all_deployed_apps(self, app_id: Optional[str] = None, app_instance_id: Optional[str] = None, region: Optional[str] = None) -> List[Dict]:
        return [{"appInstanceId": "abcd-efgh", "status": "ready"}]

    def undeploy_app(self, app_instance_id: str) -> None:
        print(f"Deleting app instance: {app_instance_id}")
