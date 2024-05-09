import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram import Client, filters
import httpx

api_url_chat5 = "https://nandha-api.onrender.com/ai/gpt"

def fetch_data(api_url: str, query: str) -> tuple:
    try:
        response = requests.get(f"{api_url}/{query}")
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 2:
            return data.get("content", "No response from the API."), None
        else:
            return None, f"API error: {data.get('message', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {e}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

@Client.on_message(filters.command(["gpt","bard","llama","palm"]))
async def chatgpt5(_: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give An Input!!")

    query = " ".join(message.command[1:])    
    txt = await message.reply_text("Wait patiently")
    await txt.edit("💭")
    api_response, error_message = fetch_data(api_url_chat5, query)
    await txt.edit(api_response or error_message)
