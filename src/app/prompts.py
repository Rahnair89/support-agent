import os
import pathlib


def load_prompt(name: str) -> str:
    version = os.environ.get("PROMPT_VERSION", "v1")
    path = pathlib.Path(f"prompts/{name}.{version}.md")
    if not path.exists():
        path = pathlib.Path(f"prompts/{name}.v1.md")
    return path.read_text()
