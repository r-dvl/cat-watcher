import aiohttp


async def post_photo(url, headers, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            print(f'Response status: {response.status}')
            return await response.text()