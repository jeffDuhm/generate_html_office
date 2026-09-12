import re
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    name = Path(filename).stem # sin .docx

    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "-", name.strip())
    
    return name.lower()
    