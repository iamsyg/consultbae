from fastapi import HTTPException

from api.utils.supabase import supabase


def get_all_submissions():

    try:
        response = (
            supabase
            .table("audio_submissions")
            .select(
                """
                submission_id,
                audio_url,
                duration_seconds,
                sample_rate_khz,
                bitrate_kbps,
                loudness_db,
                created_at,
                people (
                    person_id,
                    names,
                    phones
                )
                """
            )
            .order("created_at", desc=True)
            .execute()
        )

        submissions = response.data or []

        result = []

        for submission in submissions:

            person = submission.get("people") or {}

            result.append({
                "submission_id": submission["submission_id"],

                "name": person.get("names"),
                "phone": person.get("phones")[0] if person.get("phones") else None,

                "audio_url": submission["audio_url"],

                "duration_seconds": submission[
                    "duration_seconds"
                ],

                "sample_rate_khz": submission[
                    "sample_rate_khz"
                ],

                "bitrate_kbps": submission[
                    "bitrate_kbps"
                ],

                "loudness_db": submission[
                    "loudness_db"
                ],

                "created_at": submission["created_at"]
            })

        return {
            "count": len(result),
            "submissions": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch submissions: {str(e)}"
        )