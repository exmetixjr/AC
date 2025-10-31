import re, os, asyncio, random, keep_alive
import discord
from discord.ext import commands

version = 'v2.9'

user_token = os.environ['user_token']
catch_ids = os.environ['catch_id']

catch_channels = [int(ch_id.strip()) for ch_id in catch_ids.split(',')]

with open('data/pokemon','r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/level','r') as file: 
    to_level = file.readline()
    
num_pokemon = 0
poketwo = 716390085896962058
client = commands.Bot(command_prefix='&', self_bot=True)

def log(message):
    print(message)

def random_delay(min_seconds=3.5, max_seconds=5.0):
    return random.uniform(min_seconds, max_seconds)

def solve(message):
    hint = []
    for i in range(15,len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^'+hint_replaced+'$', pokemon_list, re.MULTILINE)
    return solution

def extract_pokemon_name(content):
    try:
        split = content.split(' ')
        if len(split) > 7:
            return split[7].replace('!','').replace('*','')
        return "Unknown"
    except Exception as e:
        log(f"Error extracting pokemon name: {e}")
        return "Unknown"

@client.event
async def on_ready():
    log(f'✅ Logged into account: {client.user.name}')
    log(f'🤖 Bot version: {version}')
    log(f'📺 Monitoring {len(catch_channels)} channel(s)')
    try:
        for channel_id in catch_channels:
            channel = client.get_channel(channel_id)
            if channel:
                await channel.send("<@716390085896962058> inc r")
                log(f"📡 Sent incubator command to channel: {channel.name if hasattr(channel, 'name') else channel_id}")
            else:
                log(f"⚠️ Warning: Could not find channel {channel_id}")
    except Exception as e:
        log(f"❌ Error in on_ready: {e}")
    
@client.event
async def on_message(message):
    try:
        if message.channel.id not in catch_channels:
            if not message.author.bot:
                await client.process_commands(message)
            return
        
        if message.channel.id in catch_channels:
            if message.author.id == poketwo:
                if message.embeds:
                    embed_title = message.embeds[0].title
                    
                    if 'wild pokémon has appeared!' in embed_title:
                        delay = random_delay(3.5, 5.0)
                        await asyncio.sleep(delay)
                        await message.channel.send('<@716390085896962058> h')
                        
                    elif "Congratulations" in embed_title:
                        embed_content = message.embeds[0].description
                        if 'now level' in embed_content:
                            try:
                                split = embed_content.split(' ')
                                level = int(split[-1].replace('!', ''))
                                if level == 100:
                                    delay = random_delay(2.0, 3.0)
                                    await asyncio.sleep(delay)
                                    await message.channel.send(f".s {to_level}")
                                    log(f"⬆️ Level 100 reached - selected Pokemon {to_level}")
                                    
                                    with open('data/level', 'r') as fi:
                                        data = fi.read().splitlines(True)
                                    with open('data/level', 'w') as fo:
                                        fo.writelines(data[1:])
                            except Exception as e:
                                log(f"⚠️ Error processing level up: {e}")
                else:
                    content = message.content
                    
                    if 'The pokémon is ' in content:
                        solutions = solve(content)
                        
                        if not solutions:
                            log('❌ Pokemon not found')
                        else:
                            for pokemon in solutions:
                                log(f"🎯 Catching: {pokemon}...")
                                delay = random_delay(3.5, 5.0)
                                await asyncio.sleep(delay)
                                await message.channel.send(f'<@716390085896962058> c {pokemon}')
                                
                    elif 'Congratulations' in content:
                        global num_pokemon
                        num_pokemon += 1
                        pokemon_name = extract_pokemon_name(content)
                        log(f"✅ Caught {pokemon_name} | Total: {num_pokemon}")
                        print()
                        
                    elif 'human' in content:
                        delay = random_delay(3.0, 4.0)
                        await asyncio.sleep(delay)
                        await message.channel.send('<@716390085896962058> inc p')
                        log('⚠️ Captcha detected - paused autocatcher')
                        log('💡 Please solve captcha manually and press enter to restart')
                        
                    elif 'Please respond with the name of the pokémon' in content:
                        log('🔐 Captcha detected - starting automatic solver')
                        try:
                            hint = re.findall(r'`(.*?)`', content)[0]
                            solutions = re.findall(f'^{hint}$', pokemon_list, re.MULTILINE)
                            
                            if not solutions:
                                log("❌ Captcha solution not found")
                            else:
                                delay = random_delay(3.5, 5.0)
                                await asyncio.sleep(delay)
                                await message.channel.send(f'<@716390085896962058> c {solutions[0]}')
                                log(f"✅ Captcha solved: {solutions[0]}")
                        except Exception as e:
                            log(f"❌ Error solving captcha: {e}")
                        
                        input()
                        await message.channel.send('<@716390085896962058> h')
                        
        if not message.author.bot:
            await client.process_commands(message)
            
    except Exception as e:
        log(f"❌ Error in on_message: {e}")

@client.command()
async def say(ctx, *, args):
    await ctx.send(args)

async def run_bot():
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            log(f'🚀 Starting Pokétwo Autocatcher {version}')
            log(f'Modified by @kurkure.xd | Partner with @xtxnuh')
            keep_alive.keep_alive()
            await client.start(user_token)
        except discord.LoginFailure:
            log("❌ Login failed - Invalid token")
            break
        except Exception as e:
            retry_count += 1
            log(f"❌ Bot crashed: {e}")
            if retry_count < max_retries:
                wait_time = min(60 * retry_count, 300)
                log(f"🔄 Reconnecting in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                log("❌ Max retries reached - stopping bot")
                break
                                  if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        log("👋 Bot stopped by user")
      
