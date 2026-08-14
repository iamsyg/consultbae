# task_3/api/routes/audio_submission.py

from fastapi import APIRouter, File, Form, UploadFile

from api.controllers.audio_submission_controller import create_audio_submission


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