# task_3/api/controllers/audio_submission_controller.py

import re

from fastapi import HTTPException, UploadFile

from api.utils.supabase import supabase
import cloudinary.uploader

from api.services.audio_analysis import analyze_audio


def get_last_10_digits(phone: str) -> str:
    """
    Extract the last 10 digits from any phone format.

    Examples:
        9000000273
        +919000000273
        919000000273
        +91-9000000273
        +91 9000000273

    All become:

        9000000273
    """

    digits = re.sub(r"\D", "", phone)

    if len(digits) < 10:
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number"
        )

    last_10 = digits[-10:]

    # Indian mobile numbers should start with 6, 7, 8 or 9
    if last_10[0] not in "6789":
        raise HTTPException(
            status_code=400,
            detail="Invalid Indian mobile number"
        )

    return last_10


def create_audio_submission(
    name: str,
    phone: str,
    audio: UploadFile
):
    # -----------------------------------------
    # 1. Validate name
    # -----------------------------------------

    name = name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    # -----------------------------------------
    # 2. Validate audio
    # -----------------------------------------

    if not audio.filename:
        raise HTTPException(
            status_code=400,
            detail="Audio file is required"
        )

    metrics = analyze_audio(audio)

    # -----------------------------------------
    # 3. Get last 10 digits from incoming phone
    # -----------------------------------------

    incoming_phone = get_last_10_digits(phone)

    # -----------------------------------------
    # 4. Get all people from Supabase
    # -----------------------------------------

    try:
        people_response = (
            supabase
            .table("people")
            .select("person_id, names, phones")
            .execute()
        )

        people = people_response.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch people: {str(e)}"
        )

    # -----------------------------------------
    # 5. Find matching person
    # -----------------------------------------

    person = None

    for existing_person in people:

        db_phone = existing_person.get("phones")

        if not db_phone:
            continue

        # Extract last 10 digits from DB phone
        db_phone_last_10 = get_last_10_digits(db_phone)

        if db_phone_last_10 == incoming_phone:
            person = existing_person
            break

    # -----------------------------------------
    # 6. Create person if not found
    # -----------------------------------------

    if person is None:

        stored_phone = f"+91-{incoming_phone}"

        try:
            person_response = (
                supabase
                .table("people")
                .insert({
                    "names": name,
                    "phones": stored_phone
                })
                .execute()
            )

            if not person_response.data:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create person"
                )

            person = person_response.data[0]

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create person: {str(e)}"
            )

    person_id = person["person_id"]

    # -----------------------------------------
    # 7. Upload audio to Cloudinary
    # -----------------------------------------

    cloudinary_public_id = None

    try:

        audio.file.seek(0)

        upload_result = cloudinary.uploader.upload(
            audio.file,
            resource_type="video",
            folder="consultbae/audio"
        )

        audio_url = upload_result["secure_url"]

        cloudinary_public_id = upload_result["public_id"]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload audio: {str(e)}"
        )

    # -----------------------------------------
    # 8. Store audio information in Supabase
    # -----------------------------------------

    try:

        submission_response = (
            supabase
            .table("audio_submissions")
            .insert({
                "person_id": person_id,
                "audio_url": audio_url,
                "cloudinary_public_id": cloudinary_public_id,

                "duration_seconds": metrics["duration_seconds"],
                "sample_rate_khz": metrics["sample_rate_khz"],
                "bitrate_kbps": metrics["bitrate_kbps"],
                "loudness_db": metrics["loudness_db"]
            })
            .execute()
        )

        if not submission_response.data:

            # DB insert failed, remove Cloudinary file
            try:
                cloudinary.uploader.destroy(
                    cloudinary_public_id,
                    resource_type="video"
                )
            except Exception:
                pass

            raise HTTPException(
                status_code=500,
                detail="Failed to create audio submission"
            )

        submission = submission_response.data[0]

    except HTTPException:
        raise

    except Exception as e:

        # DB insert failed, remove Cloudinary file
        if cloudinary_public_id:

            try:
                cloudinary.uploader.destroy(
                    cloudinary_public_id,
                    resource_type="video"
                )
            except Exception:
                pass

        raise HTTPException(
            status_code=500,
            detail=f"Failed to store audio submission: {str(e)}"
        )

    # -----------------------------------------
    # 9. Return response
    # -----------------------------------------

    return {
        "message": "Audio submission created successfully",

        "person": {
            "person_id": person["person_id"],
            "name": person["names"],
            "phone": person["phones"]
        },

        "submission": {
            "submission_id": submission["submission_id"],
            "audio_url": submission["audio_url"],
            "cloudinary_public_id": submission[
                "cloudinary_public_id"
            ],

            "duration_seconds": submission["duration_seconds"],
            "sample_rate_khz": submission["sample_rate_khz"],
            "bitrate_kbps": submission["bitrate_kbps"],
            "loudness_db": submission["loudness_db"],

            "created_at": submission.get("created_at")
        }
    }