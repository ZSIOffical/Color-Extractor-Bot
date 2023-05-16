
import discord  
import requests
import shutil
from PIL import Image,ImageDraw
from collections import Counter
from discord.ext import commands


Bot = discord.Client(intents=discord.Intents.all())

def get_color_palette(image_path, palette_image_path="palette.jpg"):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((100, 100))
    colors = image.getcolors(10000)
    color_counts = Counter([color[1] for color in colors])
    palette = color_counts.most_common(5)
    palette_image = Image.new("RGB", (5 * 100, 100))
    draw = ImageDraw.Draw(palette_image)
    
    for i, (color, count) in enumerate(palette):
        draw.rectangle([i * 100, 0, (i + 1) * 100 - 1, 99], fill=color)
    
    palette_image.save(palette_image_path)
    
    return [color[0] for color in palette]

@Bot.event
async def on_ready():
    print(f"{Bot.user} is now online!")

@Bot.event
async def on_message(message):
    attachment = message.attachments[0].url
    if attachment and message.author != Bot.user:
        if message.content.startswith(".palette"):
            request = requests.get(attachment,stream=True)
            if request.status_code == 200:
                try:
                    embed_setup = discord.Embed(title="Color Palette",description="This is the color palette of your image",color=discord.Color.random())
                    with open(f"{message.author.id}.jpg","wb") as file:
                        shutil.copyfileobj(request.raw,file)
                        palette = get_color_palette(file.name, palette_image_path="palette.jpg")
                        embed_setup.add_field(name="First Color",value=palette[0],inline=True)
                        embed_setup.add_field(name="Second Color",value=palette[1],inline=True)
                        embed_setup.add_field(name="Third Color",value=palette[2],inline=True)
                        embed_setup.add_field(name="Fourth Color",value=palette[3],inline=True)
                        embed_setup.add_field(name="Fith Color",value=palette[4],inline=True)

                        await message.channel.send(embed=embed_setup,file=discord.File("palette.jpg"))
                    return
                except:
                    await message.channel.send(content="Something went wrong")


Bot.run("Super secret token here!")
