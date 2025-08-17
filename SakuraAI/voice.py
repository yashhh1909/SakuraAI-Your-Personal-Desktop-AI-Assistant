import asyncio
import edge_tts
import os

async def main():
    path = os.path.expanduser("~\\Desktop\\test.mp3")  # Save on Desktop
    communicate = edge_tts.Communicate(text="Hello! This is Aria speaking in English.", voice="en-US-AriaNeural")
    await communicate.save(path)
    print("Saved to:", path)

asyncio.run(main())
