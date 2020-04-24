import asyncio
import json
import aiohttp

import datetime
from datetime import datetime

import base64
from base64 import b64decode

class Server:
    def __init__(self, serverip: str):
        self.serverip = serverip
        self.serverinfo = {}
        self.serverinfo_vars = {}
        self.serverplayers = {}
        asyncio.get_running_loop(self.getServer())

    async def getServer(self):

        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"http://{self.serverip}/info.json") as r:
                    re = json.loads(await r.text())
                    self.serverinfo = re
                    self.serverinfo_vars = re["vars"]
                    # self.serverip = serverIp

            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"http://{self.serverip}/players.json") as r:
                    re = json.loads(await r.text())
                    self.serverplayers = re

        except:
            return f"[{datetime.now().strftime('%H:%M:%S')}] Incorrect IP or server is not responding."


    #def stringToBase64(s):
    #    return base64.b64encode(s.encode('utf-8'))

    #def base64ToString(b):
    #    return base64.b64decode(b).decode('utf-8')

    @property
    def icon(self):
        icon = self.serverinfo.get("icon", "This server has no icon.")
        if icon != 'This server has no icon.':
            with open(r"server_icon.png", "wb") as f:
                f.write(base64.b64decode(icon))
            icon = f'The server icon has been saved on the API folder: {f.name}'
        return icon
    
    @property
    def scripts(self):
        return self.serverinfo.get("resources", "This server has no scripts.")

    @property   
    def developers(self):
        return self.serverinfo_vars.get("Developer", "No developers were specified for this server.") 

    @property
    def discord(self):
        return self.serverinfo_vars.get("Discord", "No discord server was specified for this server.") 

    @property
    def pubfeed(self):
        return self.serverinfo_vars.get("activitypubFeed", "No activity pub feed was specified for this server.")

    @property
    def banner_connecting(self):
        return self.serverinfo_vars.get("banner_connecting", "This server has no banner for server connecting.")

    @property
    def banner_detail(self):
        return self.serverinfo_vars.get("banner_detail", "This server has no detail banner.")

    @property
    def license_key_token(self):
        return self.serverinfo_vars.get("sv_licenseKeyToken", "No license key token were specified for this server.")

    @property
    def max_players(self):
        return self.serverinfo_vars.get("sv_maxClients", "No information about max players were specified for this server.")

    @property 
    def tags(self):
        tags = self.serverinfo_vars.get("tags", "This server has no tags.")
        if tags != 'This server has no tags':
            tags = list(tags.split(','))
        return tags

    @property 
    def top_tag(self):
        tags = self.serverinfo_vars.get("tags", "This server has no tags.")
        if tags != 'This server has no tags':
            tags = list(tags.split(','))
            tags = tags[0]
        return tags   


    @property
    def version(self):
        return self.serverinfo.get("version", "No discord server was specified for this server.")     

    @property
    def anticheat(self):
        return self.serverinfo_vars.get("Anticheat", "Disabled")   

    @property
    def community(self):
        return self.serverinfo_vars.get("Community", "No community server was specified for this server.")   

    @property
    def txt(self):
        f = open(f"./serverinfo.txt", "w")
        f.write("""  
        ______ _____ _   _ ________  ___    ___  ______ _____ 
        |  ___|_   _| | | |  ___|  \/  |   / _ \ | ___ \_   _|
        | |_    | | | | | | |__ | .  . |  / /_\ \| |_/ / | |  
        |  _|   | | | | | |  __|| |\/| |  |  _  ||  __/  | |  
        | |    _| |_\ \_/ / |___| |  | |  | | | || |    _| |_ 
        \_|    \___/ \___/\____/\_|  |_/  \_| |_/\_|    \___/ 
        """)
        f.write(f"\n            Basic information about {self.serverip}")
        f.write("\n-------------------------------------------------------------------------------------------------------------------")
        f.write(f"\nServer community: {self.community}")
        f.write(f"\nServer players: {len(self.serverplayers)}/{self.max_players}")
        f.write(f"\nServer scripts: {len(self.scripts)}")
        f.write(f"\nServer developers: {self.developers}")
        f.write(f"\nServer tags: {', '.join(self.tags)}")
        f.write(f"\nServer top tag: {self.top_tag}")
        f.write(f"\nServer pubfeed: {self.pubfeed}")
        f.write("\n-------------------------------------------------------------------------------------------------------------------")
        f.write(f"\n            Links information about {self.serverip}")
        f.write("\n-------------------------------------------------------------------------------------------------------------------")
        f.write(f"\nServer discord (invite url link): {self.discord}")
        f.write(f"\nServer banner connecting (image url link): {self.banner_connecting}")
        f.write(f"\nServer banner detail (image url link): {self.banner_detail}")
        f.write("\n-------------------------------------------------------------------------------------------------------------------")
        f.write(f"\n            More information about {self.serverip}")
        f.write("\n-------------------------------------------------------------------------------------------------------------------")
        f.write(f"\nServer players slots: {self.max_players}")
        f.write(f"\nServer version: v{self.version}")
        f.write(f"\nServer anticheat: {self.anticheat}")
        f.write(f"\nServer license key token: {self.license_key_token}")
        f.write("\n-------------------------------------------------------------------------------------------------------------------")
        f.close()
        return f'The server information has been created on the API folder: {f.name}'
