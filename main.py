import asyncio

from aiohttp import web

from core import voice_to_text

app = web.Application()


async def whisper_handler(request):
    data = request.json()
    return web.json_response(
        {
            'status': True,
            'answer': await voice_to_text(data['url'], data['key']),
            'execution_time': 0
        }
    )


async def routers():
    app.router.add_post('/', await whisper_handler)


asyncio.run(routers())

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=9999)
