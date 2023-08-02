from .. import loader, utils
from telethon import types, events
import io
from PIL import Image, ImageDraw
from PIL import ImageEnhance
from PIL import ImageOps
from PIL import ImageOps as IO
from telethon.errors.rpcerrorlist import YouBlockedUserError
import string
import random
import asyncio

@loader.tds
class stickersMod(loader.Module):
	"""by @Vsakoe0 | модуль, который создаст стикерпак из фото"""
	strings = {'name':'создатель стикерпаков'}
	async def createpackcmd(self, message):
	    """Создать новый стикерпак с изображением (реплай) 
	    \n .createpack (эмодзи) (название)
	    ============================"""
	    reply = await message.get_reply_message()
	    if not reply:
	        await message.edit("Нужен реплай с фоткой")
	        return
	    
	    args = utils.get_args_raw(message)
	    splitargs = args.split()
	    if not args or len(args) <= 1:
	        await message.edit("Название стикерпака не указано")
	        return
	    await message.edit('Идет создание стикерпака')
	    chat = "@Stickers"
	    name = "".join(
                random.choice(list(string.ascii_lowercase + string.ascii_uppercase + '1' + '2' + '3' + '4' + '5' + '6' + '7' +'8' + '9' + '0' + '_'))
            for _ in range(8)
        )
	    image = io.BytesIO()
	    await message.client.download_file(reply, image)
	    image = Image.open(image)
	    image = image.resize((512,512))
	    f = open('output.png', 'w')
	    f.close()
	    image.save('output.png')
	    async with message.client.conversation(chat) as conv:
	           emoji = splitargs[0]
	           try:
	               x = await message.client.send_message(chat, "/cancel")
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               x = await message.client.send_message(chat, "/newpack")
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               x = await message.client.send_message(chat, ' '.join(splitargs[1:]))
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               image.name = name + ".png"
	               image.seek(0)
	               x = await message.client.send_file(chat, 'output.png', force_document=True)
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               x = await message.client.send_message(chat, emoji)
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               x = await message.client.send_message(chat, '/publish')
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               x = await message.client.send_message(chat, '/skip')
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               x = await message.client.send_message(chat, name)
	               ending = await conv.wait_event(
	               events.NewMessage(incoming=True, from_users=chat))
	               await x.delete()
	               await ending.delete()
	               for part in ending.raw_text.split():
	                       if part.startswith("https://t.me/"):
	                           break
	               with open('packs.txt', 'w') as file:
	                   file.write(f"{' '.join(splitargs[1:])}||{name}||")
	               await message.edit('Ссылка на стикерпак отправлена в <b>Избраннное</b>')
	               await message.client.send_message('me', "Стикерпак создан\n" + part)
	           except YouBlockedUserError:
	               await message.edit("@Stickers заблокирован")
	               return
	               
	               
	async def packscmd(self, message):
	    """Выводит список ваших стикерпаков
	    ============================"""
	    try:
	        with open('packs.txt', 'r') as rpack:
	            lines = rpack.readlines()
	            names = [l.split('||')[0] for l in lines]
	            urls = [l.split('||')[1] for l in lines]
	        mes = ' '
	        for num, nm in enumerate(names):
	            mes = mes + f'\n{num}. {nm}'
	        await message.edit(mes)
	    except:
	        await message.edit('Нет созданных стикерпаков')
	        return
	    
	    
	async def addstickcmd(self, message):
	    """Добавить стикер в стикерпак реплай 
	    \n .addstick (название) (эмодзи)
	    ============================"""
	    args = utils.get_args_raw(message)
	    splitargs = args.split(' ')
	    if not args or len(args) <= 1:
	        await message.edit("Название стикерпака не указано")
	        return
	    reply = await message.get_reply_message()
	    if not reply:
	        await message.edit("Нужен реплай с фоткой")
	        return
	    dict_packs = {}
	    with open('packs.txt', 'r') as rpack:
	        lines = rpack.readlines()
	        names = [l.split('||')[0] for l in lines]
	        urls = [l.split('||')[1] for l in lines]
	    for num, nm in enumerate(names):
	        dict_packs[nm] = int(num)
	    if splitargs[0] not in list(dict_packs.keys()):
	        await message.edit('Стикерпак не найден')
	        return
	    image = io.BytesIO()
	    await message.client.download_file(reply, image)
	    image = Image.open(image)
	    image = image.resize((512,512))
	    f = open('add.png', 'w')
	    f.close()
	    image.save('add.png')
	    chat = '@Stickers'
	    emoji = splitargs[1]
	    pack_for_edit = urls[int(dict_packs[splitargs[0]])]
	    await message.edit('Публикую...')
	    async with message.client.conversation(chat) as conv:
	           try:
	               x = await message.client.send_message(chat, "/cancel")
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               x = await message.client.send_message(chat, "/addsticker")
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               x = await message.client.send_message(chat, pack_for_edit)
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               x = await message.client.send_file(chat, 'add.png', force_document=True)
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               x = await message.client.send_message(chat, emoji)
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await x.delete()
	               x = await message.client.send_message(chat, '/done')
	               await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
	               await message.edit('Стикер успешно добавлен, переустановите стикерпак. (Ссылка на стикерпак отправлена в Избранное)')
	               await message.client.send_message('me', 'https://t.me/addstickers/'+str(pack_for_edit))
	           except YouBlockedUserError:
	               await message.edit("@Stickers заблокирован")
	               return
	        	               