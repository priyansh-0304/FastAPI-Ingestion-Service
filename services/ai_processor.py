import asyncio
import random
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Call
from app.states import CallState

async def process_call_ai(call_id: str):
    retries = 5
    delay = 1

    for _ in range(retries):
        try:
            await asyncio.sleep(random.uniform(1, 3))

            # 25% failure rate
            if random.random() < 0.25:
                raise Exception("503 AI Service Unavailable")

            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(Call).where(Call.call_id == call_id)
                )
                call = result.scalar_one()

                call.state = CallState.PROCESSING_AI
                call.transcription = "Mock transcription"
                call.sentiment = "neutral"
                call.state = CallState.ARCHIVED

                await db.commit()
            return

        except Exception:
            await asyncio.sleep(delay)
            delay *= 2

    # Mark FAILED after retries
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Call).where(Call.call_id == call_id)
        )
        call = result.scalar_one()
        call.state = CallState.FAILED
        await db.commit()