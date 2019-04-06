import discord
import os
import configparser
import pymongo

client = discord.Client()

discord_token = ""

if os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    discord_token = config.get("Discord", "token")


@client.event
async def on_ready():
    print("Running as {name} - {id}".format(name=client.user.name, id=client.user.id))
    await client.change_presence(game=discord.Game(name="Backups sichern!"))

    # Cron Job Sicherung


@client.event
async def on_message(message):
    if message.content.startswith("&help"):
        if message.author.server_permissions.manage_server:
            help = """
                    **Hi, ich bin Backbot :)**\n
                    Ich mache regelmäßige Backups für deinen Server und schicke dir sie auf Wunsch gerne per PM :)
                    
                    **Commands:**
                    &help ~ Diese Seite xD
                    &backup <on|off|file> ~ Command zum (De-)Aktivieren der Backups und zum versenden per PM
                    
                    Um die Backups jetzt zu starten: &backup on
            """

            help_embed = discord.Embed(color=discord.Color.green(), description=help)

            await client.send_message(message.channel, embed=help_embed)
    if message.content.startswith("&backup"):
        args = message.content.split(" ")

        db_client = pymongo.MongoClient()
        db = db_client.backbot
        backup_db = db.backups

        #
        print(len(args))
        if len(args) == 2:
            if args[1] == "on":
                print("Started")
            elif args[1] == "off":
                print("Stopped")
            elif args[1] == "file":
                print("File")

client.run(discord_token)
