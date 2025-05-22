from telethon import TelegramClient
from telethon.tl.types import Message
import os
from dotenv import load_dotenv


class TelegramDownloader:
    def __init__(self, api_id: int, api_hash: str, session_name: str = 'anon'):
        """
        Initialize TelegramDownloader
        
        Args:
            api_id (int): Telegram API ID
            api_hash (str): Telegram API Hash
            session_name (str, optional): Name for the session file. Defaults to 'anon'.
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(session_name, self.api_id, self.api_hash)

    async def connect(self):
        """Connect to Telegram"""
        
        await self.client.connect()
        if not await self.client.is_user_authorized():
            raise Exception("Please run the script first to authenticate")

    async def get_message(self, channel_name: str, message_id: int) -> Message:
        """
        Get a specific message from a channel
        
        Args:
            channel_name (str): The username or channel ID
            message_id (int): The ID of the message to download
            
        Returns:
            Message: The downloaded message object
        """
        try:
            message = await self.client.get_messages(channel_name, ids=message_id)
            if message is None:
                raise Exception(f"Message {message_id} not found in channel {channel_name}")
            return message
        except Exception as e:
            raise Exception(f"Error downloading message: {str(e)}")

    async def close(self):
        """Close the Telegram client connection"""
        await self.client.disconnect() 