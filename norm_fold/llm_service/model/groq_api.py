import os, json, time, requests
from .prompts import SYSTEM_PROMPT, FEW_SHOT_MESSAGES, build_user_prompt
from . import config  # ensure .env loaded
from .normalize import _extract_json_block

def call_groq(user_text: str, hints: dict, *, model: str | None = None, max_tokens: int = 1200) -> dict:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Не найден GROQ_API_KEY в окружении")

    model = model or os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *FEW_SHOT_MESSAGES,
        {"role": "user", "content": build_user_prompt(user_text, hints)},
    ]

    def _post(json_mode: bool):
        payload = {
            "model": model,
            "temperature": 0.35,  # чуть смелее для разнообразия, но без потери строгости формата
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        t0 = time.time()
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        _ = int((time.time()-t0)*1000)
        return r

    # Пробуем JSON-mode, при 400 — без него
    r = _post(True)
    if r.status_code == 400:
        r = _post(False)

    if r.status_code != 200:
        raise RuntimeError(f"Groq API error {r.status_code}: {r.text}")

    try:
        resp = r.json()
        content = resp["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Ошибка парсинга ответа от Groq: {e}")

    try:
        data = json.loads(content)
    except Exception:
        data = _extract_json_block(content)

    # meta удалён по требованию
    return data
