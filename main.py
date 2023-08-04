import os
import random

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


def get_value(nested_dicts: dict, key: hash) -> hash:
    if key in nested_dicts and 'official-artwork' in nested_dicts[key]:
        return nested_dicts[key]
    for k, v in nested_dicts.items():
        if isinstance(v, dict):
            value = get_value(v, key)
            if value is not None:
                return value

@bot.command(name='need_help')
async def need_help(ctx):
    TEXT = '''
Небольшая справка по командам бота:

$cat — случайное изображение котика
$capybara — случайное изображение капибары
$dog — случайное изображение собаки
$pokemon — случайное изображение покемона

Так же есть возможность получить сразу несколько изображений некоторых животных:

$cats <n> — где n — число от 1 до 10, количество изображений кошек
$dogs <n> — где n — число от 1 до 10, количество изображений собак
    '''
    await ctx.send(TEXT)

@bot.command(name='cat')
async def cat(ctx):
    url = 'https://api.thecatapi.com/v1/images/search'
    get_cat_image = requests.get(url).json()
    await ctx.send(get_cat_image[0]['url'])


@bot.command(name='cats')
async def cats(ctx, n=None):
    url = 'https://api.thecatapi.com/v1/images/search?limit=10'
    cats_list = requests.get(url).json()
    if n is None or int(n) > 10:
        n = 10
    for i in range(int(n)):
        await ctx.send(cats_list[i]['url'])


@bot.command(name='dog')
async def dog(ctx):
    url = 'https://dog.ceo/api/breeds/image/random'
    dog_js = requests.get(url).json()
    await ctx.send(dog_js['message'])


@bot.command(name='dogs')
async def cats(ctx, n=None):
    url = 'https://dog.ceo/api/breeds/image/random'
    if n is None or int(n) > 10:
        n = 10
    dogs_list = [requests.get(url).json() for _ in range(int(n))]
    for dog in dogs_list:
        await ctx.send(dog['message'])


@bot.command(name='pokemon')
async def pokemon(ctx):
    identifier = random.randint(1, 500)
    url = f'https://pokeapi.co/api/v2/pokemon/{identifier}'
    content = requests.get(url=url).json()
    pok = get_value(content, 'front_shiny')
    await ctx.send(pok)


@bot.command(name='capybara')
async def capybara(ctx):
    url = 'https://api.capy.lol/v1/capybara?json=true'
    capibara_js = requests.get(url).json()
    await ctx.send(capibara_js['data']['url'])


if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('TOKEN'))
