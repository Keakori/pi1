import discord

TOKEN = "ODI1MjgwODM5NjI5Mjc1MTM2.YF7orQ.PMKRI5SvETRHWJyqmEF7DzLpvcg"
client = discord.Client()
client.run(TOKEN)

token = "token"
@client.event
async def on_ready():
    print(f'{client.user} подключен к Discord!')
    for guild in client.guilds:
        print(
            f'{client.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})')
