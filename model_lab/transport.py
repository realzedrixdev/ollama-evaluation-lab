import json
import urllib.request


class OllamaTransport:
    def __init__(self, endpoint="http://localhost:11434/api/generate", timeout=180):
        self.endpoint, self.timeout = endpoint, timeout

    def generate(self, model: str, prompt: str, system: str = "") -> str:
        data = json.dumps({"model": model, "prompt": prompt, "system": system, "stream": False}).encode()
        request = urllib.request.Request(self.endpoint, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read())["response"]
