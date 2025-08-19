import requests

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

            if not data.get("choices") or not data["choices"][0].get("message"):
                raise ValueError("Unexpected response format from vLLM.")

            return data["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                f"Could not connect to vLLM server at {self.base_url}. "
                "Make sure vLLM is running: e.g., `vllm serve ...` or check your VLLM_URL."
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("Request to vLLM timed out. Check server and connectivity.")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP error from vLLM: {e}. Response text: {getattr(e.response, 'text', 'N/A')}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while calling vLLM: {e}")

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
            response = requests.post(url, json=payload, headers=headers, timeout=100)
            response.raise_for_status()
            data = response.json()

            if not data.get("choices") or not data["choices"][0].get("text"):
                raise ValueError("Unexpected response format from vLLM.")

            return data["choices"][0]["text"]

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                f"Could not connect to vLLM server at {self.base_url}. "
                "Make sure vLLM is running: e.g., `vllm serve ...` or check your VLLM_URL."
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("Request to vLLM timed out. Check server and connectivity.")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP error from vLLM: {e}. Response text: {getattr(e.response, 'text', 'N/A')}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while calling vLLM: {e}")


# Example usage with error handling
if __name__ == "__main__":
    client = VLLMClient()
    try:
        output = client.chat([
            {"role": "system", "content": "You are a friendly assistant."},
            {"role": "user", "content": "Hello, vLLM! How are you today?"}
        ])
        print("Chat response:", output)
    except RuntimeError as e:
        print("[FATAL] Chat failed:", e)

    try:
        legacy_output = client.complete("The capital of France is")
        print("Completion response:", legacy_output)
    except RuntimeError as e:
        print("[FATAL] Completion failed:", e)
