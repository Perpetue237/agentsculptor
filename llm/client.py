import requests
import json

class VLLMClient:
    def __init__(self, base_url="http://localhost:8008", model="openai/gpt-oss-120b"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def chat(self, messages, max_tokens=512, temperature=0):
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        headers = {"Content-Type": "application/json"}

        print("\n[DEBUG] Sending chat request to:", url)
        #print("[DEBUG] Payload:\n", json.dumps(payload, indent=2))

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            #print("[DEBUG] Raw response:\n", json.dumps(data, indent=2))
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            print("[ERROR] HTTPError:", e)
            print("[ERROR] Response text:\n", response.text)
            raise
        except Exception as e:
            print("[ERROR] Unexpected error:", e)
            raise

    def complete(self, prompt, max_tokens=1024, temperature=0):
        url = f"{self.base_url}/v1/completions"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        headers = {"Content-Type": "application/json"}

        print("\n[DEBUG] Sending completion request to:", url)
        print("[DEBUG] Payload:\n", json.dumps(payload, indent=2))

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            print("[DEBUG] Raw response:\n", json.dumps(data, indent=2))
            return data["choices"][0]["text"]
        except requests.exceptions.HTTPError as e:
            print("[ERROR] HTTPError:", e)
            print("[ERROR] Response text:\n", response.text)
            raise
        except Exception as e:
            print("[ERROR] Unexpected error:", e)
            raise

# Simple test usage
if __name__ == "__main__":
    client = VLLMClient()

    # Chat mode test
    try:
        output = client.chat([
            {"role": "system", "content": "You are a friendly assistant."},
            {"role": "user", "content": "Hello, vLLM! How are you today?"}
        ])
        print("Chat response:", output)
    except Exception:
        print("[TEST] Chat failed.")

    # Legacy completion test
    try:
        legacy_output = client.complete("The capital of France is")
        print("Completion response:", legacy_output)
    except Exception:
        print("[TEST] Completion failed.")
