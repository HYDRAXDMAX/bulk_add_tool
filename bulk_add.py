from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
import asyncio

# Your API credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'  # Your Telegram phone number

async def bulk_add_members():
    async with TelegramClient(phone, api_id, api_hash) as client:
        print("Welcome to the Telegram Bulk Adder Tool!")
        
        # Get group details from the user
        source_group = input("Enter the Source Group ID or Username: ").strip()
        target_group = input("Enter the Target Group ID or Username: ").strip()
        
        print("Fetching members from the source group...")
        try:
            source_group_entity = await client.get_entity(source_group)
            members = await client.get_participants(source_group_entity)
            print(f"Found {len(members)} members in the source group.")
        except Exception as e:
            print(f"Error fetching members from source group: {e}")
            return

        try:
            target_group_entity = await client.get_entity(target_group)
        except Exception as e:
            print(f"Error accessing target group: {e}")
            return

        # Adding members to the target group
        for member in members:
            try:
                user = InputPeerUser(member.id, member.access_hash)
                await client(InviteToChannelRequest(target_group_entity, [user]))
                print(f"Added {member.username or member.id} to the target group.")
                await asyncio.sleep(5)  # Respect Telegram's rate limits
            except Exception as e:
                print(f"Failed to add {member.username or member.id}: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(bulk_add_members())
