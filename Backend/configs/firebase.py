import firebase_admin
from firebase_admin import credentials
import os


def initialize_firebase():

    if firebase_admin._apps:
        return firebase_admin.get_app()

    credential_path = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH"
    )

    if not credential_path:
        raise RuntimeError(
            "FIREBASE_SERVICE_ACCOUNT_PATH is not configured."
        )

    cred = credentials.Certificate(
        credential_path
    )

    return firebase_admin.initialize_app(
        cred
    )