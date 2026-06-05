import requests
import json

class FordefiBridge:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.fordefi.com/api/v1"

    def mint_tokens(self, vault_id: str, to_address: str, quantity: int):
        url = f"{self.base_url}/transactions"
        payload = {
            "vault_id": vault_id,
            "type": "evm_transaction",
            "details": {
                "type": "evm_raw_transaction",
                "chain": "ethereum_mainnet",
                "gas": {"type": "priority", "priority_level": "medium"},
                "to": to_address,
                "data": {"method_name": "mintPublic", "method_arguments": [f"quantity:{quantity}"]}
            }
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()

if __name__ == "__main__":
    pass
