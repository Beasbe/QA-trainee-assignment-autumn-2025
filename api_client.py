import requests
from settings import BASE_URL


class ApiClient:
    def __init__(self):
        self.base_url = BASE_URL

    def create_ad(self, data):
        return requests.post(f"{self.base_url}/api/1/item", json=data)

    def get_ad_by_id(self, ad_id):
        return requests.get(f"{self.base_url}/api/1/item/{ad_id}")

    def get_ads_by_seller(self, seller_id):
        return requests.get(f"{self.base_url}/api/1/{seller_id}/item")

    def get_statistics_v1(self, ad_id):
        return requests.get(f"{self.base_url}/api/1/statistic/{ad_id}")

    def delete_ad(self, ad_id):
        return requests.delete(f"{self.base_url}/api/2/item/{ad_id}")

    def get_statistics_v2(self, ad_id):
        return requests.get(f"{self.base_url}/api/2/statistic/{ad_id}")

    def extract_ad_id(self, response_data):
        if isinstance(response_data, dict) and "status" in response_data:
            status_text = response_data["status"]
            if " - " in status_text:
                return status_text.split(" - ")[-1]
        return None