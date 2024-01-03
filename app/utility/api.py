import aiohttp


async def post_photo(url, headers, data):
    """
    Asynchronously sends a POST request to a specified URL with the provided headers and data.
    
    Args:
        url (str): The URL to send the POST request to.
        headers (dict): The headers to include in the POST request.
        data (dict): The data to include in the body of the POST request.
        
    Returns:
        str: The text of the response from the POST request.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            print(f'Response status: {response.status}')
            return await response.text()
