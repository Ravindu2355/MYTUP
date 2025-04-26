import json
import os
import asyncio
import aiofiles
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pyrogram import Client
from pyrogram.types import Message

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

async def get_login_url():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    auth_url, _ = flow.authorization_url(prompt="consent")
    return auth_url

async def save_auth_code(code):
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    flow.fetch_token(code=code)
    creds = flow.credentials
    async with aiofiles.open("token.json", "w") as f:
        await f.write(creds.to_json())
    return True

def get_credentials():
    if not os.path.exists("token.json"):
        return None
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(google.auth.transport.requests.Request())
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

async def upload_video(file_path, title, description):
    creds = get_credentials()
    if not creds:
        return {"success": False, "error": "You are not logged in. Use /login and /saveAuth first."}
    
    youtube = build("youtube", "v3", credentials=creds)
    
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["telegram", "upload"],
            "categoryId": "22"  # category 'People & Blogs'
        },
        "status": {
            "privacyStatus": "unlisted"
        }
    }

    media = googleapiclient.http.MediaFileUpload(file_path, resumable=True)

    upload_request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = upload_request.next_chunk()
        await asyncio.sleep(1)

    return {"success": True, "video_id": response.get("id")}
  
