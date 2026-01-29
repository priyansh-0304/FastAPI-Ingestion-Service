from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.database import get_db
from app.models import Call
from app.schemas import CallPacket
from app.states import CallState
from app.services.ai_processor import process_call_ai
import asyncio

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/v1/call/stream/{call_id}", status_code=202)
async def stream_call(
    call_id: str,
    packet: CallPacket,
    db: AsyncSession = Depends(get_db)
):
    # Row-level lock to handle race conditions
    result = await db.execute(
        select(Call).where(Call.call_id == call_id).with_for_update()
    )
    call = result.scalar_one_or_none()

    if call is None:
        call = Call(call_id=call_id, state=CallState.IN_PROGRESS)
        db.add(call)
        try:
            await db.flush()
        except Exception:
            # Another concurrent request created the row first
            await db.rollback()
            result = await db.execute(
                select(Call)
                .where(Call.call_id == call_id)
                .with_for_update()
            )
            call = result.scalar_one()

    # Packet order validation
    if packet.sequence != call.last_sequence + 1:
        logger.warning(
            f"Missing packet for {call_id}: "
            f"expected {call.last_sequence + 1}, got {packet.sequence}"
        )

    call.last_sequence = packet.sequence

    # Simulate completion condition
    if packet.sequence >= 5:
        call.state = CallState.COMPLETED
        asyncio.create_task(process_call_ai(call_id))

    await db.commit()
    return {"status": "accepted"}