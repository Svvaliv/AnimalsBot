import os
import random

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
# from september_3 import images


class AnimalsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)
        self.remove_command('help')

    async def on_message(self, message):
        channel = message.channel
        if (
                message.author != self.user and
                channel.name != 'команды-для-ботов' and
                message.content[1:] in self.all_commands
        ):
            embed = discord.Embed(description='😭 Команды боту можно отправлять только в канале "команды-для-ботов"')
            return await message.channel.send(embed=embed)

        await self.process_commands(message)


bot = AnimalsBot()


def get_value(nested_dicts: dict, key: hash) -> hash:
    if key in nested_dicts and 'official-artwork' in nested_dicts[key]:
        return nested_dicts[key]
    for k, v in nested_dicts.items():
        if isinstance(v, dict):
            value = get_value(v, key)
            if value is not None:
                return value


@bot.command(name='help')
async def help(ctx):
    TEXT = '''
$bird — случайное изображение птички
$cat — случайное изображение котика
$capybara — случайное изображение капибары
$dog — случайное изображение собаки
$fox — случайное изображение лисицы
$kangaroo — случайное изображение кенгуру
$koala — случайное изображение коалы
$panda — случайное изображение панды
$pikachu — случайное изображение Пикачу
$pokemon — случайное изображение покемона
$red_panda — случайное изображение красной панды

Так же есть возможность получить сразу несколько изображений некоторых животных:

$cats <n> — где n — число от 1 до 3, количество изображений кошек
$dogs <n> — где n — число от 1 до 3, количество изображений собак
    '''
    embed = discord.Embed(title='Справка по командам бота', description=TEXT)
    await ctx.send(embed=embed)


@bot.command(name='cat')
async def cat(ctx):
    url = 'https://api.thecatapi.com/v1/images/search'
    get_cat_image = requests.get(url).json()
    await ctx.send(get_cat_image[0]['url'])


@bot.command(name='cats')
async def cats(ctx, n=None):
    url = 'https://api.thecatapi.com/v1/images/search?limit=10'
    cats_list = requests.get(url).json()
    if n is None or int(n) > 3:
        n = 3
    for i in range(int(n)):
        await ctx.send(cats_list[i]['url'])


@bot.command(name='dog')
async def dog(ctx):
    url = 'https://dog.ceo/api/breeds/image/random'
    dog_js = requests.get(url).json()
    await ctx.send(dog_js['message'])


@bot.command(name='dogs')
async def dogs(ctx, n=None):
    url = 'https://dog.ceo/api/breeds/image/random'
    if n is None or int(n) > 3:
        n = 3
    dogs_list = [requests.get(url).json() for _ in range(int(n))]
    for dog in dogs_list:
        await ctx.send(dog['message'])


@bot.command(name='pokemon')
async def pokemon(ctx):
    identifier = random.randint(1, 1008)
    url = f'https://pokeapi.co/api/v2/pokemon/{identifier}'
    content = requests.get(url=url).json()
    pok = get_value(content, 'front_shiny')
    await ctx.send(pok)


@bot.command(name='capybara')
async def capybara(ctx):
    url = 'https://api.capy.lol/v1/capybara?json=true'
    capibara_js = requests.get(url).json()
    await ctx.send(capibara_js['data']['url'])


@bot.command(name='koala')
async def koala(ctx):
    url = 'https://some-random-api.com/animal/koala'
    koala_js = requests.get(url).json()
    await ctx.send(koala_js['image'])


# @bot.command(name='raccoon')
# async def raccoon(ctx):
#     url = 'https://some-random-api.com/animal/raccoon'
#     raccoon_js = requests.get(url).json()
#     await ctx.send(raccoon_js['image'])


@bot.command(name='bird')
async def bird(ctx):
    url = 'https://some-random-api.com/animal/bird'
    bird_js = requests.get(url).json()
    await ctx.send(bird_js['image'])


@bot.command(name='panda')
async def panda(ctx):
    url = 'https://some-random-api.com/animal/panda'
    panda_js = requests.get(url).json()
    await ctx.send(panda_js['image'])


@bot.command(name='fox')
async def fox(ctx):
    url = 'https://some-random-api.com/animal/fox'
    fox_js = requests.get(url).json()
    await ctx.send(fox_js['image'])


@bot.command(name='kangaroo')
async def kangaroo(ctx):
    url = 'https://some-random-api.com/animal/kangaroo'
    kangaroo_js = requests.get(url).json()
    await ctx.send(kangaroo_js['image'])


@bot.command(name='red_panda')
async def red_panda(ctx):
    url = 'https://some-random-api.com/animal/red_panda'
    red_panda_js = requests.get(url).json()
    await ctx.send(red_panda_js['image'])


@bot.command(name='pikachu')
async def pikachu(ctx):
    url = 'https://some-random-api.com/img/pikachu'
    pikachu_js = requests.get(url).json()
    await ctx.send(pikachu_js['link'])

# @bot.command(name='shufik')
# async def shufik(ctx):
#     img = random.choice(images)
#     await ctx.send(img)


if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('TOKEN'))
