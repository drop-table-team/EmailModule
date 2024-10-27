import json
import os
import aiohttp
from aiohttp import FormData

BACKEND_BASE_URL = os.getenv('BACKEND_BASE_URL')
backend_url = f'{BACKEND_BASE_URL}/modules/input'

async def store_backend(entry, html):
    if entry is None:
        return
    async with aiohttp.ClientSession() as session:
        form = FormData()
        form.add_field(
            "json", json.dumps(entry)
        )
        form.add_field("file", html, filename=f"{entry.title}.html", content_type="text/html")
        async with session.post(backend_url, data=form) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
