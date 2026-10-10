from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, UploadFile

from app.dependencies.auth_dependencies import require_role
from app.entities.user_entity import UserRole
from app.exceptions.exceptions import ForbiddenError, NotFoundError

data_router = APIRouter()

UPLOAD_DIR = Path("uploaded_data")
UPLOAD_DIR.mkdir(exist_ok=True)
file_dirs = [dir.name for dir in UPLOAD_DIR.iterdir() if dir.is_dir()]
file_extentions = ["pdf", "docx", "txt"]


@data_router.post("/upload_data")
async def upload_data(
    file: UploadFile,
    data_engineer_id: int = Depends(require_role(UserRole.DATA_ENGINEER)),
):
    if not file.filename:
        raise ForbiddenError("Файл должен иметь верно структурированное название")

    file_ext = file.filename.split(".")[-1]
    if file_ext not in file_extentions:
        raise NotFoundError("Такой тип расширения не поддерживается")
    ext_position = file_extentions.index(file_ext)
    file_path = UPLOAD_DIR / file_dirs[ext_position] / file.filename

    async with aiofiles.open(file_path, mode="wb") as f:
        content = await file.read()
        await f.write(content)
    return {"filename": file.filename, "size": len(content)}
