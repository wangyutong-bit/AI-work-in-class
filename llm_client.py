import json
import os
from pathlib import Path
from urllib import error, request


def _load_env_file() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_env_file()

DEFAULT_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.siliconflow.cn/v1")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct")


def _get_api_key() -> str:
    api_key = (
        os.getenv("LLM_API_KEY")
        or os.getenv("SILICONFLOW_API_KEY")
        or os.getenv("DEEPSEEK_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if not api_key:
        raise RuntimeError(
            "未找到可用的 API Key。请在 .env 中配置 LLM_API_KEY、SILICONFLOW_API_KEY、DEEPSEEK_API_KEY 或 OPENAI_API_KEY。"
        )
    return api_key


def invoke_messages(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    temperature: float = 0,
    max_tokens: int | None = 1024,
) -> str:
    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    req = request.Request(
        url=f"{DEFAULT_BASE_URL.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"模型调用失败: HTTP {exc.code} - {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"模型调用失败: {exc.reason}") from exc

    return data["choices"][0]["message"]["content"]


def invoke_text(
    prompt: str,
    *,
    model: str | None = None,
    temperature: float = 0,
    max_tokens: int | None = 1024,
) -> str:
    return invoke_messages(
        [{"role": "user", "content": prompt}],
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
