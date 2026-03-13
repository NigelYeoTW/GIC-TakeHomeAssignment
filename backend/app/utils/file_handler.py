import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import get_settings

settings = get_settings()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def save_logo(file: UploadFile) -> str:
    """Validates and saves a logo file. Returns the stored file path."""
    _validate_logo(file)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "png"
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)

    total = 0
    chunks = []
    chunk_size = 64 * 1024  # 64KB
    while chunk := file.file.read(chunk_size):
        total += len(chunk)
        if total > settings.MAX_LOGO_SIZE_BYTES:
            raise HTTPException(status_code=400, detail="Logo must be under 2MB")
        chunks.append(chunk)

    with open(file_path, "wb") as f:
        for chunk in chunks:
            f.write(chunk)

    return file_path


def delete_logo(file_path: str) -> None:
    """Deletes a logo file from disk. Silently ignores missing files."""
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass


def _validate_logo(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_CONTENT_TYPES)}",
        )
