from dotenv import load_dotenv
import os
import asyncio
import re
from telegram_downloader import TelegramDownloader


def parse_telegram_link(link: str) -> tuple[str, int]:
    """
    Parse a Telegram channel link to extract channel name and message ID
    
    Args:
        link (str): Telegram channel link (e.g., "https://t.me/prometa/3251")
        
    Returns:
        tuple[str, int]: Channel name and message ID
        
    Raises:
        ValueError: If the link format is invalid
    """
    # Regular expression to match t.me links
    pattern = r'https?://t\.me/([^/]+)/(\d+)'
    match = re.match(pattern, link)
    
    if not match:
        raise ValueError("Invalid Telegram link format. Expected format: https://t.me/channel_name/message_id")
    
    channel_name = match.group(1)
    message_id = int(match.group(2))
    
    return channel_name, message_id


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
        
        # Example: Parse a Telegram link
        telegram_link = "https://t.me/prometa/3251"
        channel_name, message_id = parse_telegram_link(telegram_link)
        
        # Download the message
        message = await downloader.get_message(channel_name, message_id)
        print(f"Message text: {message.text}")
        
    except ValueError as e:
        print(f"Invalid link format: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Always close the connection
        await downloader.close()


if __name__ == "__main__":
    asyncio.run(main())
