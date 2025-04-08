from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
import os
from models import ResponseSignal
from helpers.config import get_settings,Settings
from controllers import datacontroler,ProjectController
from fastapi.responses import JSONResponse
import aiofiles

data_router = APIRouter(
    prefix='/api/v1/data',
    tags=['api_v1',"data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,app_settings: Settings = Depends(get_settings)):
    #validation des fichiers
    is_valid = datacontroler().validation_upload(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result_signal
            }
        )
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = os.path.join(
        project_dir_path,
        file.filename
    )
    async with aiofiles.open(file_path,"wb")as f:
        while chunk :=await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)

    return JSONResponse(
            content={
                "signal":ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )      