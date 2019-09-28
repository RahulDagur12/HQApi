from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
import random
import requests
from discord.ext.commands import Bot
import discord
from discord.ext import commands
import random
import aiohttp
import csv
import json
import datetime
import string


client = Bot(command_prefix='+')
client.remove_command('help')


def rand():
    ran = random.randint(2,4)
    x = "1234567890"
    name = "Lasie"
    for i in range(ran):
        c = random.choice(x)
        name = name+c
        api = HQApi()
    check = api.check_username(name)
    if not check:
        return name
    else:
        return rand()

api = HQApi()


@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("I'm ready")

@client.command(pass_context=True, no_pm=True)
async def hq(ctx, message=None):
    api = HQApi()
    phonenumber = message
    print(phonenumber)
    x = api.send_code("+" + phonenumber, "sms")
    print(x)
    v = x['verificationId']
    global smscode
    smscode = None
    def code_check(msg1):
        return msg1.content.lower().startswith('+code')
    smg = await client.wait_for_message(author=ctx.message.author, check=code_check)
    smscode = smg.content[len('+code'):].strip()
    print(smscode)
    value = int(smscode)
    s = api.confirm_code(v, value)
    await client.say("success")
    name = rand()
    print(name)
    referral = 'None'
    d = api.register(v, name, referral)
    token = d['authToken']
    print(d)
    embed=discord.Embed(title=f"HQ coin bot", description="", color=0x73ee57 )
    embed.add_field(name="Question {0}/{1}", value='Starting', inline=False)
    embed.set_footer(text="")
    x=await client.say(embed=embed)
    api = HQApi(token)
    
    
    try:
        offair_id = api.start_offair()['gameUuid']
    except ApiResponseError:
        offair_id = api.get_schedule()['offairTrivia']['games'][0]['gameUuid']
    while True:
        offair = api.offair_trivia(offair_id)
        print("Question {0}/{1}".format(offair['question']['questionNumber'], offair['questionCount']))
        print(offair['question']['question'])
        bed=discord.Embed(title=f"HQ coin bot", description="", color=0x73ee57 )
        bed.add_field(name=f"Question {offair['question']['questionNumber']}/{offair['questionCount']}", value='\u200b', inline=False)
        bed.add_field(name="Question ", value=offair['question']['question'], inline=False)
        bed.set_footer(text="")
        r = await client.edit_message(x,embed=bed)
        for answer in offair['question']['answers']:
            print('{0}. {1}'.format(answer['offairAnswerId'], answer['text']))
            abed=discord.Embed(title=f"HQ coin bot", description="", color=0x73ee57 )
            abed.add_field(name=f"Question {offair['question']['questionNumber']}/{offair['questionCount']}", value='\u200b', inline=False)
            abed.add_field(name="Question ", value=offair['question']['question'], inline=False)
            abed.add_field(name=f"Options", value=(answer['offairAnswerId'], answer['text']), inline=False)
            abed.set_footer(text="")
            e = await client.edit_message(r,embed=abed)
        lol = random.randint(0,3)
        answer = api.send_offair_answer(offair_id, offair['question']['answers'][lol]['offairAnswerId'])
        print('You got it right: ' + str(answer['youGotItRight']))
        await client.say('You got it right: ' + str(answer['youGotItRight']))
        if answer['gameSummary']:
            print('Game ended')
            await client.say('Game ended')
            print('Earned:')
            await client.say('Earned:')
            print('Coins: ' + str(answer['gameSummary']['coinsEarned']))
            await client.say('Coins: ' + str(answer['gameSummary']['coinsEarned']))
            print('Points: ' + str(answer['gameSummary']['pointsEarned']))
            await client.say('Points: ' + str(answer['gameSummary']['pointsEarned']))
            embed=discord.Embed(title=f"HQ coin bot", description="", color=0x73ee57 )
            embed.add_field(name=f"**Game ended**", value='\u200b', inline=False)
            embed.add_field(name="Earned Coins:", value=str(answer['gameSummary']['coinsEarned']), inline=False)
            embed.add_field(name="Earned Points:", value=str(answer['gameSummary']['pointsEarned']), inline=False)
            embed.set_footer(text="")
            await client.edit_message(e,embed=embed)
            break

client.run("Bot token")
