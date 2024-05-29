import requests
import discord
from discord.ext import commands
import aiohttp
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

api_key = ""
api_uuid = ""
api_url = "https://api.hypixel.net/skyblock/profiles?key={key}&uuid={uuid}".format(key=api_key, uuid=api_uuid)


@client.event
async def on_ready():
    print("Bot Online")


# @client.command(aliases=['p'])
# async def ping(ctx):
#     await ctx.send("pong")


@client.command(aliases=['b'])
async def get_bazaar(ctx, *item):
    join_text = ' '.join(item)
    processed_text = join_text.upper().replace(" ", "_").strip()

    bazaar_link = "https://api.hypixel.net/v2/skyblock/bazaar"
    bazaar_response = requests.get(bazaar_link)
    try:
        listing = bazaar_response.json().get("products").get(processed_text).get("quick_status")
        product_id = listing.get("productId")
        sell_price = round(listing.get("sellPrice"), 2)
        buy_price = round(listing.get("buyPrice"), 2)
        format_text = f"Item: {product_id} \nSell Price: {sell_price} \nBuy Price: {buy_price}"
        await ctx.send(format_text)
    except AttributeError as e:
        await ctx.send("COULDN'T FIND ITEM")


async def getting_auctions(session, url):
    async with session.get(url) as resp:
        auctions = await resp.json()
        items = ""
        for auction in auctions.get("auctions"):
            if "Giant Mender Fedora" in auction.get("item_name"):
                global counter
                name = auction.get("item_name")
                highest_bid = str(auction.get("highest_bid_amount"))
                starting_bid = str(auction.get("starting_bid"))
                if items != "":
                    items += "\n"
                items += ("Item: " + name + "\nStarting bid: " + starting_bid + "\nHighest Bid: " + highest_bid + "\n")
        return items


@client.command(aliases=['ah'])
async def get_auctions(ctx):
    ah_link = "https://api.hypixel.net/v2/skyblock/auctions"
    ah_response = requests.get(ah_link)
    listing = ah_response.json()
    pages = listing.get("totalPages")

    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(pages):
            ah_link = f"https://api.hypixel.net/v2/skyblock/auctions?page={i}"
            tasks.append(asyncio.ensure_future(getting_auctions(session, ah_link)))

        original = await asyncio.gather(*tasks)
        for item in original:
            if item != "":
                print(item)


# @client.command(aliases=['c'])
# async def get_collection(ctx):
#     response = requests.get(api_url)
#     profiles = (response.json()).get("profiles")
#     collection = sorted(profiles[0].get('members').get(api_uuid).get("unlocked_coll_tiers"))
#     await ctx.send(collection)


# https://api.mojang.com/users/profiles/minecraft/{username}?
client.run("")
