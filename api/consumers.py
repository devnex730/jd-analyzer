from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from google import genai
import traceback
import os
client = genai.Client(api_key=os.environ.get("GOOGLE_GEMMA_API"))



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        from api.ml import train_once
        await train_once()


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            msg = ("""
                Answer in only plain text.
                You are helper chatbot.
                Give SHORT, CRISP answers.
                Use bullet points.
                No long theory explanations.
                """
                   +data.get("message"))
            res = await sync_to_async(client.models.generate_content)(
                model = "gemma-3-27b-it",
                contents = msg)
            await self.send(json.dumps({"reply": res.text}))

        except Exception as e:
            traceback.print_exc()
            await self.send(json.dumps({
                "reply": "Internal error. Check server logs."
            }))
