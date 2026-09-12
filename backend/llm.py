import requests


OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

MODEL = "llama3.2"


def generate_answer(prompt):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "No answer generated."
        )

    except requests.exceptions.ConnectionError:

        return (
            "Unable to connect to Ollama. "
            "Make sure Ollama is running."
        )

    except Exception as e:

        return (
            f"LLM error: {str(e)}"
        )