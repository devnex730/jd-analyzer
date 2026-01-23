from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import google.generativeai as genai
import traceback
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    "gemini-2.5-flash-lite",
    system_instruction="""
    Answer in only plain text.
    You are JD Analyzer chatbot.
    Give SHORT, CRISP answers.
    Use bullet points.
    No long theory explanations.
    """
)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.chat = model.start_chat(history=[])

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            msg = data.get("message")
            res = await sync_to_async(self.chat.send_message)(msg)
            await self.send(json.dumps({"reply": res.text}))

        except Exception as e:
            traceback.print_exc()
            await self.send(json.dumps({
                "reply": "Internal error. Check server logs."
            }))
