import requests
from app.prompts import build_rag_prompt

def model_exists():
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def clean_model_output(raw_output):
    if "ANSWER_START" in raw_output:
        cleaned = raw_output.split("ANSWER_START", 1)[-1].strip()
    else:
        cleaned = raw_output.strip()

    if "[ Prompt:" in cleaned:
        cleaned = cleaned.split("[ Prompt:", 1)[0].strip()

    return cleaned

def call_model(question, runbook):
    prompt = build_rag_prompt(question, runbook)

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a Kubernetes expert."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.6,
        "max_tokens": 200,
        "stream": False,
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8080/v1/chat/completions",
            json=payload,
            timeout=60,
        )

        if response.status_code != 200:
            return f"Model API failed with status {response.status_code}:\n{response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.RequestException as error:
        return f"Model API request failed:\n{error}"

    except KeyError:
        return f"Unexpected model API response:\n{response.text}"



### command to run llama-server for local testing
# llama-server -m /Users/gd06tf/Downloads/personal/models/tinyllama-1.1b-chat-v1.0.Q2_K.gguf --host 127.0.0.1 --port 8080

## curl command to test llama-server health endpoint
#curl http://127.0.0.1:8080/health