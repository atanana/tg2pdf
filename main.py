from dotenv import load_dotenv
import os
import asyncio
import re
import argparse
from datetime import datetime
from exporter import export_markdown_to_pdf
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


def generate_output_filename() -> str:
    """
    Generate output filename with current datetime
    
    Returns:
        str: Generated filename
    """
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"outputs/{current_time}.pdf"


async def process_links(downloader: TelegramDownloader, links: list[str]) -> list[tuple[str, str]]:
    """
    Process multiple Telegram links and collect their messages
    
    Args:
        downloader (TelegramDownloader): Initialized Telegram downloader
        links (list[str]): List of Telegram channel links
        
    Returns:
        list[tuple[str, str]]: List of tuples containing channel name and message text
    """
    messages = []
    
    for link in links:
        try:
            channel_name, message_id = parse_telegram_link(link)
            message = await downloader.get_message(channel_name, message_id)
            
            # Add channel name as a header to the message
            formatted_message = f"# {channel_name}\n\n{message.text}\n\n---\n\n"
            messages.append((channel_name, formatted_message))
            print(f"Successfully processed: {link}")
            
        except ValueError as e:
            print(f"Invalid link format: {str(e)}")
        except Exception as e:
            print(f"Error processing link {link}: {str(e)}")
    
    return messages


async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download Telegram messages and convert to PDF')
    parser.add_argument('links', nargs='+', help='Telegram channel links to process')
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    api_id = int(os.getenv("TG_API_ID"))
    api_hash = os.getenv("TG_API_HASH")
    
    # Initialize the downloader with API credentials
    downloader = TelegramDownloader(api_id=api_id, api_hash=api_hash)
    
    try:
        # Connect to Telegram
        await downloader.connect()
        
        # Process all links and collect messages
        messages = await process_links(downloader, args.links)
        
        if messages:
            # Combine all messages into one text
            combined_text = "".join(msg[1] for msg in messages)
            
            # Generate output filename and export to PDF
            output_file = generate_output_filename()
            export_markdown_to_pdf(combined_text, output_file)
            print(f"\nAll messages exported to: {output_file}")
        else:
            print("No messages were successfully processed.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Always close the connection
        await downloader.close()


if __name__ == "__main__":
    asyncio.run(main())
