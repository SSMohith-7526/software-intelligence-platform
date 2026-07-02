import os
import zipfile
import io
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from config import settings
from utils.logger import logger

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_repository_payload(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Ingests a zipped repository from the React UI, unzips it in memory, 
    and returns a structured file dictionary ready for the LangGraph state bus.
    """
    if not file.filename.endswith('.zip'):
        logger.error(f"Invalid file upload attempt: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
            detail="The AI OS strictly requires a .zip archive of the repository."
        )

    # Read the file bytes into memory (avoiding slow disk I/O)
    file_bytes = await file.read()
    
    # Enforce size limits to protect the system memory
    if len(file_bytes) > (settings.MAX_FILE_SIZE_MB * 1024 * 1024):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload exceeds {settings.MAX_FILE_SIZE_MB}MB limit."
        )

    extracted_files = {}
    
    try:
        # Process the zip file entirely in RAM
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            for zip_info in z.infolist():
                # Skip directories and hidden git files
                if zip_info.is_dir() or '__MACOSX' in zip_info.filename or '.git' in zip_info.filename:
                    continue
                    
                # Read specific file content
                try:
                    with z.open(zip_info) as f:
                        content = f.read().decode('utf-8')
                        extracted_files[zip_info.filename] = content
                except UnicodeDecodeError:
                    # Silently skip binary files (images, compiled objects)
                    pass
                    
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is corrupted and cannot be unzipped."
        )

    logger.info(f"Successfully ingested UI payload. Extracted {len(extracted_files)} readable files.")

    # Return the payload formatted exactly as the Repository Agent expects it
    return {
        "status": "success",
        "file_count": len(extracted_files),
        "payload": {
            "repository_path": file.filename,
            "files": extracted_files
        }
    }