from fastapi import APIRouter

router = APIRouter()


@router.get("/auth/login")
def login() -> dict:
    return {"status": "redirect_to_portal_oauth"}


@router.get("/auth/callback")
def callback() -> dict:
    return {"status": "oauth_callback_received"}


@router.post("/auth/logout")
def logout() -> dict:
    return {"status": "logged_out"}
