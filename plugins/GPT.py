import requests
from pyrogram import filters, Client
from pyrogram.types import Message, InputMediaPhoto
from pyrogram import *
from pyrogram.errors import MediaCaptionTooLong

api_url_bard = "https://nandha-api.onrender.com/ai/bard"

def fetch_data(api_url: str, query: str) -> tuple:
    try:
        response = requests.get(f"{api_url}/{query}")
        response.raise_for_status()
        data = response.json()
        return data.get("content", "No response from the API."), data.get("images", False)
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {e}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"


@Client.on_message(filters.command(["gpt","bard","llama", "palm","google"]))
async def bard(app, message):
    chat_id = message.chat.id
    message_id = message.id
    
    if len(message.command) < 2:
        return await message.reply_text("Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ǫᴜᴇʀʏ.")

    query = " ".join(message.command[1:])
    txt = await message.reply_text("Wᴀɪᴛ ᴘᴀᴛɪᴇɴᴛʟʏ")
    await txt.edit("💭")
    
    api_response, images = fetch_data(api_url_bard, query)

    medias = []
    bard = str(api_response)
    try:
       photo_url = images[-1]
    except:
        pass
    
    
    if images:
        if len(images) > 1:
            for url in images:
                medias.append(InputMediaPhoto(media=url, caption=None))
                        
            medias[-1] = InputMediaPhoto(media=photo_url, caption=bard)
            
            try:
                await app.send_media_group(chat_id=chat_id, media=medias, reply_to_message_id=message_id)
                return await txt.delete()
            except Exception as e:
                return await txt.edit(str(e))
        elif len(images) < 2:
            image_url = images[0]
            try:
                await message.reply_photo(photo=image_url, caption=bard)
                return await txt.delete()
            except MediaCaptionTooLong:
                return await txt.edit(bard)
            except Exception as e:
                return await txt.edit(str(e))
        else:
            return await txt.edit('Somthing went wrong')
    else:
        try:
            return await txt.edit(bard)
        except Exception as e:
            return await txt.edit(str(e))
