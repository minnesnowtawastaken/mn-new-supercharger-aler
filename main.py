from bs4 import BeautifulSoup
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import os

response = requests.request("GET", "https://www.tesla.com/findus/list/superchargers/United+States")

soup = BeautifulSoup(response.text, 'html.parser')

divTag = soup.find_all("div", {"class": "state"})

new_locations = []
existing_locations = []

with open('current_mn_sites', 'r') as f:
    lines = f.readlines()
    for item in lines:
        existing_locations.append(item.strip())

for tag in divTag:
    tdTags = tag.find_all("h2")
    for tag2 in tdTags:
        if tag2.text == "Minnesota":
            aTag = tag.find_all("a")
            for location in aTag:
                if location.text.strip() not in existing_locations:
                    new_locations.append(location.text.strip())
                    with open('current_mn_sites', 'a') as f:
                        f.write("{}\n".format(location.text.strip()))
if new_locations:
    webhook = DiscordWebhook(
        url=os.environ.get('DISCORD_WEBHOOK_URL'),
        content='@here')
    embed = DiscordEmbed(title='New MN Superchargers found', color=242424)
    for item in new_locations:
        embed.add_embed_field(name="Site:", value='{}'.format(item), inline=False)
    embed.add_embed_field(name="Supercharge.info", value="https://supercharge.info/changes", inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()
