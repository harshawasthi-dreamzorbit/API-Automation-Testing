from config import ENDPOINT

class TrialAPIPage:

    def __init__(self, api_context):
        self.api_context = api_context
        self.endpoint = ENDPOINT

    def start_trial(self, payload):
        """
        Send POST request to Trial Start API.
        """
        response = self.api_context.post(
            self.endpoint,
            data=payload
        )

        print("\n" + "=" * 60)
        print("API REQUEST")
        print("=" * 60)
        print("Request Fingerprint:", payload.get("fingerprint"))
        print("Request Email:", payload.get("email"))
        print("Request Payload:", payload)
        print("\nSTATUS CODE:", response.status)
        print("\nAPI RESPONSE:")
        print(response.text())
        print("=" * 60)

        return response