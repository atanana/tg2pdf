from dotenv import load_dotenv
import os
import asyncio
from telegram_downloader import TelegramDownloader


async def main():
    # Load environment variables
    load_dotenv()
    api_id = int(os.getenv("TG_API_ID"))
    api_hash = os.getenv("TG_API_HASH")
    
    # Initialize the downloader with API credentials
    downloader = TelegramDownloader(api_id=api_id, api_hash=api_hash)
    
    try:
        # Connect to Telegram
        await downloader.connect()
        
        # Example: Download a message from a channel
        channel_name = "footballnovosty"  # Replace with actual channel username or ID
        message_id = 12921  # Replace with actual message ID
        
        message = await downloader.get_message(channel_name, message_id)
        print(f"Message text: {message.text}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Always close the connection
        await downloader.close()


if __name__ == "__main__":
    asyncio.run(main())
