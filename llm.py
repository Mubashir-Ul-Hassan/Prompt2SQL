import requests
from typing import List, Dict, Optional

class LLMError(Exception):
    pass

def _messages_from_prompt(system_prompt: str, user_prompt: str) -> list:
    msgs = []
    if system_prompt:
        msgs.append({"role": "system", "content": system_prompt})
    msgs.append({"role": "user", "content": user_prompt})
    return msgs

def chat_ollama(model: str, messages: List[Dict], base_url: str = "http://localhost:11434", temperature: float = 0.2, json_mode: bool=False, timeout: int = 120) -> str:
    """
    Calls Ollama's chat endpoint. Requires Ollama running locally.
    """
    url = f"{base_url.rstrip('/')}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature}
    }
    if json_mode:
        payload["format"] = "json"
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
    except requests.RequestException as e:
        raise LLMError(f"Ollama connection error: {e}")
    if resp.status_code != 200:
        raise LLMError(f"Ollama error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    # Ollama returns: {"message": {"role": "...","content":"..."}, ...}
    msg = data.get("message", {}).get("content", "")
    if not msg:
        # some models may return "response"
        msg = data.get("response", "")
    return msg

def chat_openai_compatible(base_url: str, api_key: str, model: str, messages: List[Dict], temperature: float = 0.2, json_mode: bool=False, timeout: int = 120) -> str:
    """
    Calls an OpenAI-compatible /v1/chat/completions endpoint.
    Works with OpenAI, DeepSeek, Groq (when compatible), etc. Provide proper base_url and key.
    """
    url = f"{base_url.rstrip('/')}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": messages,
         # don't stream; we'll keep it simple
        "temperature": temperature,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except requests.RequestException as e:
        raise LLMError(f"API connection error: {e}")
    if resp.status_code != 200:
        raise LLMError(f"API error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise LLMError(f"Unexpected API response: {str(data)[:400]}")

def chat(provider: str,
         model: str,
         system_prompt: str,
         user_prompt: str,
         temperature: float = 0.2,
         base_url: Optional[str] = None,
         api_key: Optional[str] = None,
         json_mode: bool=False) -> str:
    """
    Unified interface. provider in {"ollama","api"}.
    """
    messages = _messages_from_prompt(system_prompt, user_prompt)
    if provider == "ollama":
        return chat_ollama(model=model, messages=messages, base_url=base_url or "http://localhost:11434", temperature=temperature, json_mode=json_mode)
    elif provider == "api":
        if not base_url or not api_key:
            raise LLMError("For provider='api', both base_url and api_key are required.")
        return chat_openai_compatible(base_url=base_url, api_key=api_key, model=model, messages=messages, temperature=temperature, json_mode=json_mode)
    else:
        raise LLMError(f"Unknown provider: {provider}")

