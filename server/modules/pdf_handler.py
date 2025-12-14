import os
import shutil
import tempfile
from fastapi import UploadFile
from pathlib import Path

UPLOAD_DIR = "./uploaded_docs"

def save_uploaded_file(files: list[UploadFile]) -> list[str]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_paths = []

    for file in files:
        if not file.filename:
            raise ValueError("Invalid filename")

        safe_name = Path(file.filename).name
        temp_path = os.path.join(UPLOAD_DIR, safe_name)

        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        file_paths.append(temp_path)

    return file_paths
