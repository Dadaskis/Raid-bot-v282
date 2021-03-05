# Needs telethon library
# pip install telethon
#
# Dont forget to change api_id and api_hash
#
# Commands are readable by bot only in "saved messages" channel.

from telethon import TelegramClient, sync, events
import random
import sched, time
import asyncio

api_id = 0 # paste your own from https://my.telegram.org/apps
api_hash = '---'

def multiline_text(*args):
	result = ""
	for text in args:
		result += text + "\n"
	return result

help_text = multiline_text(
    "Raid bot v282",
    "/ping - ping pong command",
    "/remember_stickers - enables "remember stickers" mode. After writing this command you will need to send stickers which will be used during the raid. To disable this mode write /stop_remember_stickers.",
    "/remember_text - enables "remember text" mode which is means that bot will remember some text to send during the raid. Write to disable: /stop_remember_text",
    "/remember_media - remembers multimedia content such as images or GIFs. For disabling: /stop_remember_media",
    "/test_raid - test raid with 50 messages, its nice to raid yourself",
    "/raid [chat_name] - raids some selected chat, instead of [chat_name] you need to paste name of the chat ACCURATELY. You can stop the raid using /stop_raid",
)

client = TelegramClient('session_name', api_id, api_hash)
client.start()

async def answer_myself(text):
	await client.send_message("me", text)
	
def get_random_item(array):
	return array[random.randint(0, len(array) - 1)]

remembering_stickers = False
remembered_stickers = []
remembering_text = False
remembered_text = []
remembering_media = False
remembered_media = []
stop_raid = False

raid_target = "me"
async def send_raid_message():
	try:
		global remembered_stickers
		global remembered_text
		global remembered_media
		global raid_target
		
		random.seed(random.randint(-100, 100) * 123)
		
		variant = random.randint(1, 3)
		
		if variant == 1:
			await client.send_file(raid_target, get_random_item(remembered_stickers))
		elif variant == 2:
			await client.send_message(raid_target, get_random_item(remembered_text))
		elif variant == 3:
			await client.send_file(raid_target, get_random_item(remembered_media))
	except:
		await send_raid_message()
	

@client.on(events.NewMessage(chats = "me"))
async def handler(event):
	global remembering_stickers
	global remembered_stickers
	global remembering_text
	global remembered_text
	global remembering_media
	global remembered_media
	global raid_target
	global stop_raid 
	
	if remembering_stickers:
		if "/stop_remember_stickers" in event.text:
			remembering_stickers = False
			await answer_myself("Stickers remember mode is disabled")
		else:
			remembered_stickers.append(event.sticker)
			await answer_myself("Saved this sticker")
			return
	
	if remembering_text:
		if "/stop_remember_text" in event.text:
			remembering_text = False
			await answer_myself("Text remember mode is disabled")
		else:
			remembered_text.append(event.text)
			await answer_myself("Saved this text")
			return
	
	if remembering_media:
			if "/stop_remember_media" in event.text:
				remembering_media = False
				await answer_myself("Media remember mode is disabled")
			else:
				remembered_media.append(event.media)
				await answer_myself("Saved this media")
				return
			
	
	if "/ping" in event.text:
		await answer_myself("pong")
	
	if "/help" in event.text:
		await answer_myself(help_text)
	
	if "/remember_stickers" in event.text:
		await answer_myself("Send some stickers")
		remembering_stickers = True
		return
	
	if "/remember_text" in event.text:
		await answer_myself("Send some text")
		remembering_text = True
		return
	
	if "/remember_media" in event.text:
		await answer_myself("Send some GIFs or images")
		remembering_media = True
		return
	
	if "/test_raid" in event.text:
		raid_target = "me"
		for counter in range(1, 50):
			await asyncio.sleep(random.uniform(0.02, 0.15))
			await send_raid_message()
	
	if "/raid" in event.text:
		target_chat_name = event.text
		target_chat_name = target_chat_name.replace("/raid", "").strip()
		my_private_channel_id = None
		my_private_channel = None
		
		async for dialog in client.iter_dialogs():
		    if dialog.name == target_chat_name:
		        my_private_channel = dialog
		        my_private_channel_id = dialog.id
		        break
		
		if my_private_channel_id:
			try:
				await answer_myself("Chat is detected, starting the raid")
				raid_target = my_private_channel_id
				while True:
					if stop_raid:
						break
					await asyncio.sleep(random.uniform(0.02, 0.15))
					await send_raid_message()
			except:
				pass
		else:
			await answer_myself("Chat is not detected")
	
	if "/stop_raid" in event.text:
		stop_raid = True
		await answer_myself("Stopping the raid")

print("Raid bot v282 starts")
client.run_until_disconnected()
