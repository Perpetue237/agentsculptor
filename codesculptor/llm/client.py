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

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=100)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.ConnectionError:
            print("[ERROR] Could not connect to vLLM server at", self.base_url)
            print("Please make sure vLLM is running and reachable.")
            return None
        except requests.exceptions.Timeout:
            print("[ERROR] Request to vLLM timed out. Try increasing the server timeout or check connectivity.")
            return None
        except requests.exceptions.HTTPError as e:
            print("[ERROR] HTTP error from vLLM:", e)
            print("Response text:", getattr(e.response, "text", "N/A"))
            return None
        except Exception as e:
            print("[ERROR] Unexpected error while calling vLLM:", e)
            return None

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

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"]
        except requests.exceptions.ConnectionError:
            print("[ERROR] Could not connect to vLLM server at", self.base_url)
            return None
        except requests.exceptions.Timeout:
            print("[ERROR] Request to vLLM timed out.")
            return None
        except requests.exceptions.HTTPError as e:
            print("[ERROR] HTTP error from vLLM:", e)
            print("Response text:", getattr(e.response, "text", "N/A"))
            return None
        except Exception as e:
            print("[ERROR] Unexpected error while calling vLLM:", e)
            return None


# Simple test usage
if __name__ == "__main__":
    client = VLLMClient()

    # Chat mode test
    output = client.chat([
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": "Hello, vLLM! How are you today?"}
    ])
    if output:
        print("Chat response:", output)
    else:
        print("[TEST] Chat failed due to vLLM issues.")

    # Legacy completion test
    legacy_output = client.complete("The capital of France is")
    if legacy_output:
        print("Completion response:", legacy_output)
    else:
        print("[TEST] Completion failed due to vLLM issues.")
