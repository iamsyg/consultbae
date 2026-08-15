# task_3/api/routes/audio_submission.py

from fastapi import APIRouter, File, Form, UploadFile

from api.controllers.audio_submission_controller import create_audio_submission
from api.controllers.get_all_submissions import get_all_submissions


router = APIRouter(
    prefix="/api/audio",
    tags=["Audio Submissions"]
)


@router.post("/submissions")
def submit_audio(
    name: str = Form(...),
    phone: str = Form(...),
    audio: UploadFile = File(...)
):
    return create_audio_submission(
        name=name,
        phone=phone,
        audio=audio
    )



@router.get("")
def list_submissions():

    return get_all_submissions()