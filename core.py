import os
import random
import aiohttp
import openai


async def download_audio_async(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, "wb") as file:
                    while True:
                        chunk = await response.content.read(128)
                        if not chunk:
                            break
                        file.write(chunk)


async def complete_openai(openai_api_key, file_path):
    async with openai.AsyncOpenAI(api_key=openai_api_key) as client:
        audio_file = open(file_path, "rb")
        transcript = await client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
    return transcript


async def voice_to_text(url, openai_api_key):
    file_path = f"{random.randint(1000000, 100000000)}.m4a"
    await download_audio_async(url, file_path)
    response = await complete_openai(openai_api_key, file_path)
    os.remove(file_path)
    return response
