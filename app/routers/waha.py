import logging
from fastapi import APIRouter, Request
from app.models.waha import WahaWebhook

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Actions"])

@router.post("/webhook/waha", name="waha_webhook")
async def waha_webhook(
    request: Request,
    payload: WahaWebhook
):
    """
    Webhook endpoint to receive callbacks from WAHA service.
    """
    # Log the received webhook payload
    logger.info(f"Recieved webhook from waha for session:{payload.session}, event:{payload.event}")
    # For now, we'll just acknowledge receipt of the webhook
    print(f"Received webhook for session: {payload.session}")
    return {"status": "ok", "message": "Webhook received"}