import aiohttp
import time
import asyncio
import requests

# Synchronous block for making requests with requests library
def sync_requests():
    URL = "http://127.0.0.1:8000"
    start = time.time()
    results = []
    for i in range(1000):
        results.append(requests.post(URL).content)
    print(f"Sync Time: {time.time() - start}")

# Asynchronous block for making requests with aiohttp library
async def test(URL):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL) as resp:
            return await resp.text()

async def async_requests():
    URLS = ["http://127.0.0.1:8000" for _ in range(1000)]
    start = time.time()
    results = await asyncio.gather(*(test(URL) for URL in URLS), return_exceptions=True)
    print(f"Async Time: {time.time() - start}")

# Main block to run both synchronous and asynchronous parts
if __name__ == '__main__':
    sync_requests()  # Execute synchronous requests
    asyncio.run(async_requests())  # Execute asynchronous requests
