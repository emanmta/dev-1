from fastapi import APIRouter, Request
from app.models.waha import WahaWebhook

router = APIRouter(tags=["Actions"])

@router.post("/webhook/waha", name="waha_webhook")
async def waha_webhook(
    request: Request,
    payload: WahaWebhook
):
    """
    Webhook endpoint to receive callbacks from WAHA service.
    """
    # For now, we'll just acknowledge receipt of the webhook
    print(f"Received webhook for session: {payload.session}")
    return {"status": "ok", "message": "Webhook received"}