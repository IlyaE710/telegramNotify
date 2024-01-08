import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from telegram import Bot

app = FastAPI()

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("Telegram token is not found in environment variables")

bot = Bot(token=TELEGRAM_TOKEN)


class Notification(BaseModel):
    message: str
    chat_id: str = None


@app.post("/notification")
async def notification(notification_request: Notification = Body(...)):
    if not notification_request.chat_id:
        raise ValueError("Chat ID is required")

    await bot.send_message(
        chat_id=notification_request.chat_id, text=notification_request.message
    )
    return {"message": "Notification sent"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
