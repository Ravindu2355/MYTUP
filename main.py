import asyncio
from pyrogram import Client, filters
from config import Config
from yt_uploader import get_login_url, save_auth_code, upload_video

app = Client(
    "UploaderBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# /login command
@app.on_message(filters.command("login") & filters.user(Config.OWNER_ID))
async def login_handler(client, message):
    url = await get_login_url()
    await message.reply(f"🔐 **Login URL:**\n[Click here to login]({url})\n\nAfter login, copy the code and use /saveAuth <code>", disable_web_page_preview=True)

# /saveAuth command
@app.on_message(filters.command("saveAuth") & filters.user(Config.OWNER_ID))
async def save_auth_handler(client, message):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.reply("⚠️ Usage: `/saveAuth <authorization_code>`", quote=True)
    code = parts[1]
    success = await save_auth_code(code)
    if success:
        await message.reply("✅ Successfully saved authentication!")
    else:
        await message.reply("❌ Failed to save authentication.")



@app.on_message(filters.command("saveclient") & filters.reply)
async def save_client_secret(client: Client, message: Message):
    reply = message.reply_to_message

    # Check if the replied message has a document
    if not reply.document:
        return await message.reply("❌ Please reply to a `.json` file!")

    # Check if the file is a JSON
    if not reply.document.file_name.endswith(".json"):
        return await message.reply("❌ The file must be a `.json`!")

    # Download the file
    try:
        save_path = "./client_secret.json"
        await message.reply("⬇️ Downloading client secret...")
        await reply.download(file_name=save_path)
        await message.reply("✅ Client secret saved successfully!")
    except Exception as e:
        await message.reply(f"❌ Failed to save: `{str(e)}`")



# /yt command
@app.on_message(filters.command("yt") & filters.reply & filters.user(Config.OWNER_ID))
async def yt_upload_handler(client, message):
    media = message.reply_to_message
    if not (media.video or media.document):
        return await message.reply("⚠️ Reply to a video or document to upload to YouTube.")
    
    file_name = media.file_name or "video.mp4"
    msg = await message.reply(f"⬇️ Downloading `{file_name}`...", quote=True)
    path = await media.download()
    
    await msg.edit("⬆️ Uploading to YouTube...")

    title = file_name
    description = "Uploaded using my Telegram Bot."

    res = await upload_video(path, title, description)
    if res["success"]:
        await msg.edit(f"✅ Uploaded Successfully!\n\n🔗 [Watch Video](https://youtu.be/{res['video_id']})", disable_web_page_preview=True)
    else:
        await msg.edit(f"❌ Upload failed: `{res['error']}`")
    
    try:
        os.remove(path)
    except:
        pass

app.run()
