import telethon
from telethon import TelegramClient, events, sync
from telethon import functions, types, custom
from telethon.tl.types import *
from telethon.tl.functions.messages import *
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.functions.channels import EditBannedRequest,GetParticipantRequest
from telethon.tl.functions.messages import GetHistoryRequest,GetMessagesRequest,SendMediaRequest,SearchRequest
from telethon import errors,helpers, utils, hints
from googletrans import Translator
from bs4 import BeautifulSoup
import html
import os
import sys
import time
import emoji
import random
from random import randrange
import GoogleNews
from GoogleNews import GoogleNews
from dadjokes import Dadjoke
import googletrans
import json
import requests
import re
import urllib.request as urllib2
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from datetime import timedelta,date
import psycopg2
from psycopg2.extras import RealDictCursor
import sched, time
from better_profanity import profanity
import PIL
from PIL import Image
from io import BytesIO
import io
import base64
import logging
#import aiml
import pickle
import pandas as pd
import nltk
#nltk.download('popular', quiet=True)
from nltk.corpus import *
import numpy as np
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
#import sklearn.external.joblib as extjoblib
import joblib
import re, string, unicodedata
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
bot = ChatBot('MsTokyo')
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english.greetings","chatterbot.corpus.english.conversations" )

#con = psycopg2.connect(database="mstokyodb", user="postgres", password="O1EDxoMuzIAYzDtP", host="mstokyodb-ojncaublf6dgubfc-svc.qovery.io", port="5432")
global con
eventDict = {}
eventDict[0] = [0]
s = sched.scheduler(time.time, time.sleep)

async def getDbCon():
    con = psycopg2.connect(database="mstokyodb", user="postgres", password="O1EDxoMuzIAYzDtP", host="mstokyodb-ojncaublf6dgubfc-svc.qovery.io", port="5432")
    return con

def createQueries():
    try:      
        print("Started")
        tables = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
        queries = []
        queries.append(""" CREATE TABLE IF NOT EXISTS "ChannelDetails"("ChannelId" text,"ChannelTitle" text,"ChannelUsername" text,"AccessHash" text,"Active" boolean) WITH (OIDS = FALSE); ALTER TABLE "ChannelDetails" OWNER to postgres; """)
        queries.append(""" CREATE TABLE IF NOT EXISTS "ChannelSettings"("SettingsID" serial,"ChannelID" text,"Profanity" boolean,"Reputation" boolean,"AIChat" boolean,"Active" boolean,PRIMARY KEY ("SettingsID")) WITH (OIDS = FALSE); ALTER TABLE "ChannelSettings" OWNER to postgres; """)
        queries.append(""" CREATE TABLE IF NOT EXISTS "UserDetails"("ChannelID" text,"UserID" text,"TotalMessages" integer,"TotalReputation" integer,"FirstName" text)WITH (OIDS = FALSE); ALTER TABLE "UserDetails" OWNER to postgres; """)
        queries.append(""" CREATE TABLE IF NOT EXISTS "Messages"("ChannelID" text,"MessageID" text) WITH (OIDS = FALSE); ALTER TABLE "Messages" OWNER to postgres; """)
        queries.append(""" -- FUNCTION: DecreaseReputationCount(text) -- DROP FUNCTION "DecreaseReputationCount"(text); CREATE OR REPLACE FUNCTION "DecreaseReputationCount"("ChannelIDUserID" text) RETURNS void LANGUAGE 'sql' VOLATILE PARALLEL UNSAFE AS $BODY$ UPDATE "UserDetails" SET "TotalReputation" = (SELECT "TotalReputation" FROM "UserDetails" WHERE "ChannelID_UserID" = "ChannelIDUserID") - 1 WHERE "ChannelID_UserID" = "ChannelIDUserID" $BODY$; ALTER FUNCTION "DecreaseReputationCount"(text) OWNER TO postgres; """)
        queries.append(""" -- FUNCTION: IncreaseReputationCount(text) -- DROP FUNCTION "IncreaseReputationCount"(text); CREATE OR REPLACE FUNCTION "IncreaseReputationCount"("ChannelIDUserID" text) RETURNS void LANGUAGE 'sql' VOLATILE PARALLEL UNSAFE AS $BODY$ UPDATE "UserDetails" SET "TotalReputation" = (SELECT "TotalReputation" FROM "UserDetails" WHERE "ChannelID_UserID" = "ChannelIDUserID") + 1 WHERE "ChannelID_UserID" = "ChannelIDUserID" $BODY$; ALTER FUNCTION "IncreaseReputationCount"(text) OWNER TO postgres; """)
        queries.append(""" -- FUNCTION: IncreaseMessageCount(text) -- DROP FUNCTION "IncreaseMessageCount"(text); CREATE OR REPLACE FUNCTION "IncreaseMessageCount"("ChannelIDUserID" text) RETURNS void LANGUAGE 'sql' VOLATILE PARALLEL UNSAFE AS $BODY$ UPDATE "UserDetails" SET "TotalMessages" = (SELECT "TotalMessages" FROM "UserDetails" WHERE "ChannelID_UserID" = "ChannelIDUserID") + 1 WHERE "ChannelID_UserID" = "ChannelIDUserID" $BODY$; ALTER FUNCTION "IncreaseMessageCount"(text) OWNER TO postgres; """)
        queries.append(""" -- FUNCTION: .InsertUser(text, text, integer, integer, text, text) -- DROP FUNCTION ."InsertUser"(text, text, integer, integer, text, text); CREATE OR REPLACE FUNCTION ."InsertUser"("ChannelIDVal" text,"UserIDVal" text,"TotalMessagesVal" integer,"TotalReputationVal" integer,"FirstNameVal" text,"ChannelIDUserIDVal" text) RETURNS void LANGUAGE 'sql' VOLATILE PARALLEL UNSAFE AS $BODY$ INSERT INTO "UserDetails" ("ChannelID","UserID","TotalMessages","TotalReputation","FirstName","ChannelID_UserID") VALUES ("ChannelIDVal","UserIDVal","TotalMessagesVal","TotalReputationVal","FirstNameVal","ChannelIDUserIDVal") $BODY$; ALTER FUNCTION ."InsertUser"(text, text, integer, integer, text, text) OWNER TO postgres; """)
        con = psycopg2.connect(database="mstokyodb", user="postgres", password="O1EDxoMuzIAYzDtP", host="mstokyodb-ojncaublf6dgubfc-svc.qovery.io", port="5432")
        cur = con.cursor()
        cur.execute(tables)
        tabData = cur.fetchall()
        if tabData is None:        
            for query in queries:
                cur.execute(query)
                con.commit()
                time.sleep(1)
        print("Done")
        cur.close()
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

createQueries()

api_id = 1431692
api_hash = '4a91977a702732b8ba14fb92af6b1c2f'
bot_token = '1318065263:AAF_brgyVqsq5GKVYczM6WaMrENdG8dJNLs'

cmds = ".startbot : Start the bot \n" 
cmds = "++ : Increase reputation \n"
cmds += "-- : Reduce reputation \n"
cmds += ".toprep : Get top reputation \n"
cmds += ".mrep : Get your reputation \n"
cmds += ".yrep : Get others reputation \n"
cmds += ".translate : Get translation \n"
cmds += ".langcodes : Get language codes \n"
cmds += ".m : Mute user \n"
cmds += ".um : Unmute user \n"
cmds += ".b : Ban user \n"
cmds += ".news : Get news \n"
cmds += ".what : Get meaning \n"
cmds += ".joke : Get a joke \n"
cmds += ".yomama : Get yomama joke \n"
cmds += ".loc : Get location estimation \n"
cmds += ".quote : Get a quote \n"
cmds += ".advice : Get an advice \n"
cmds += ".dadjoke : Get a dad joke \n"
cmds += ".insult : Get insulted \n"
cmds += ".bored : Get an activity \n"
cmds += ".ping : Get bot status \n"
cmds += ".trv : Get trivia game \n"
cmds += ".reputation : use true/false to enable or disable reputation  \n"
cmds += ".profanity : use true/false to enable or disable profanity check  \n"
cmds += ".profaneadd : Add banned or profanity word eg: profaneadd word \n"
#cmds += ".profanedel : Add banned or profanity word eg: profanedel word \n"
#cmds += ".trvcat : Get trivia categories \n"
cmds += ".welcome : use true/false to enable or disable welcome \n"
cmds += ".welcometext : set welcome text eg: welcome first_name/user_name \n"
cmds += ".left : use true/false to enable or disable welcome \n"
cmds += ".lefttext : set left text eg: first_name/user_name left \n"
cmds += ".art : Get art pics \n"
#cmds += ".clean : Clean the group. Make sure you have disabled messages before using the command. \n"
cmds += ".cmd : Get list of commands \n"

client = TelegramClient('MsTokyoBot', api_id, api_hash).start(bot_token=bot_token)
client.start()

#kernel = aiml.Kernel()

#if os.path.isfile("bot_brain.brn"):
#	kernel.bootstrap(brainFile = "bot_brain.brn")
#else:
#	kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
#	kernel.saveBrain("bot_brain.brn")

settings = []

isActive = True
triviaDifficulty = ["easy","medium","hard"]
triviaCategory = {'GK':'9','Books':'10','Film':'11','Music':'12','Theatre':'13','Tv':'14','Video_games':'15','Board_games':'16','Science_Nature':'17','Computer':'18','Math':'19','Myth':'20','Sports':'21','Geography':'22','History':'23' ,'Politics':'24' ,'Art':'25' ,'Celebrities':'26' ,'Animals':'27' ,'Vehicles':'28','Comic':'29','Gadgets':'30','Anime':'31','Cartoon':'32','Any':'any'}
triviaUrl = "https://opentdb.com/api.php?amount=1&type=multiple"

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

async def AddClient(ChannelEntity):
    #if con is None or con.closed == 0:
    #    con = await getDbCon()
    if ChannelEntity is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        cid = ChannelEntity.id
        select = 'SELECT "SettingsID" FROM "ChannelSettings" WHERE "ChannelID" = %s'
        selectparam = (str(cid),)
        cur = con.cursor()
        cur.execute(select,selectparam)
        sid = cur.fetchone()
        if sid is None:
            insert = 'INSERT INTO "ChannelSettings" ("ChannelID","Profanity","Reputation","AIChat","Active") VALUES (%s,%s,%s,%s,%s)'
            insertparam = (str(ChannelEntity.id),False,True,False,True)
            cur = con.cursor()
            cur.execute(insert,insertparam)
            con.commit()
        select = 'SELECT "ChannelId" FROM "ChannelDetails" WHERE "ChannelId" = %s'
        selectparam = (str(cid),)
        cur = con.cursor()
        cur.execute(select,selectparam)
        id = cur.fetchone()
        if id is None:
            insert = 'INSERT INTO "ChannelDetails" ("ChannelId","ChannelTitle","ChannelUsername","AccessHash","Active") VALUES (%s,%s,%s,%s,%s)'
            insertparam = (ChannelEntity.id,ChannelEntity.title,ChannelEntity.username,ChannelEntity.access_hash,True)
            cur = con.cursor()
            cur.execute(insert,insertparam)
            con.commit()
        cur.close()

async def UpdateClientSettings(channelid,key,value):
    #if con is None or con.closed == 0:
    #    con = await getDbCon()
    if channelid is not None and key is not None and value is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        select = 'SELECT "SettingsID" FROM "ChannelSettings" WHERE "ChannelID" = %s'
        selectparam = (str(channelid),)
        cur = con.cursor()
        cur.execute(select,selectparam)
        sid = cur.fetchone()
        if sid is None:
            insert = 'INSERT INTO "ChannelSettings" ("ChannelID","Profanity","Reputation","AIChat") VALUES (%s,%s,%s,%s)'
            insertparam = (str(channelid),False,True,False)
            cur = con.cursor()
            cur.execute(insert,insertparam)
            con.commit()
            cur.close()
        else:
            if key == 'Profanity' and value == 'true':
                update = 'UPDATE "ChannelSettings" set "Profanity" = True WHERE "ChannelID" = %s'
            if key == 'Profanity' and value == 'false':
                update = 'UPDATE "ChannelSettings" set "Profanity" = False WHERE "ChannelID" = %s'
            if key == 'Reputation' and value == 'true':
                update = 'UPDATE "ChannelSettings" set "Reputation" = True WHERE "ChannelID" = %s'
            if key == 'Reputation' and value == 'false':
                update = 'UPDATE "ChannelSettings" set "Reputation" = False WHERE "ChannelID" = %s'
            if key == 'Welcome' and value == 'true':
                update = 'UPDATE "ChannelSettings" set "Welcome" = True WHERE "ChannelID" = %s'
            if key == 'Welcome' and value == 'false':
                update = 'UPDATE "ChannelSettings" set "Welcome" = False WHERE "ChannelID" = %s'
            if key == 'WelcomeText' and value is not None:
                update = 'UPDATE "ChannelSettings" set "WelcomeText" = \''+str(value)+'\' WHERE "ChannelID" = %s'
            if key == 'Left' and value == 'true':
                update = 'UPDATE "ChannelSettings" set "Left" = True WHERE "ChannelID" = %s'
            if key == 'Left' and value == 'false':
                update = 'UPDATE "ChannelSettings" set "Left" = False WHERE "ChannelID" = %s'
            if key == 'LeftText' and value is not None:
                update = 'UPDATE "ChannelSettings" set "LeftText" = \''+str(value)+'\' WHERE "ChannelID" = %s'
            cur = con.cursor()
            updateparam = (str(channelid),)
            cur.execute(update,updateparam)
            con.commit()
            await loadSettings()
            cur.close()

async def loadSettings():
    con = await getDbCon()
    while con.closed == 1:
            con = await getDbCon()
    select = 'SELECT * FROM "ChannelSettings"'
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute(select)
    allSettings = cur.fetchall()
    global settings
    settings = json.dumps(allSettings)
    cur.close()
    return settings

async def getUser(channelid,userid):
    if channelid is not None and userid is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        select = 'SELECT "ChannelID","UserID" FROM "UserDetails" WHERE "ChannelID_UserID" = %s'
        selectparam = (str(channelid) + "_" + str(userid),)
        cur = con.cursor()
        cur.execute(select,selectparam)
        uid = cur.fetchone()
        cur.close()
        return uid

async def AddUser(channelid,userid,firstname):
    #if con is None or con.closed == 0:
    #    con = await getDbCon()
    if channelid is not None and userid is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        uid = await getUser(channelid,userid)
        if uid is None:
            cur = con.cursor()
            cur.callproc('"InsertUser"',[str(channelid),str(userid),0,0,firstname,str(channelid) + "_" + str(userid)])
            con.commit()
            delete = 'DELETE FROM "UserDetails" WHERE "UserID" like \'Peer%\''
            cur = con.cursor()
            cur.execute(delete)
            con.commit()
            cur.close()

async def getUserStats(channelid,userid):
    #if con is None or con.closed == 0:
    #    con = await getDbCon()
    if channelid is not None and userid is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        select = 'SELECT "TotalReputation" FROM "UserDetails" WHERE "ChannelID_UserID" = %s'
        selectparam = (str(channelid) + "_" + str(userid),)
        cur = con.cursor()
        cur.execute(select,selectparam)
        stats = cur.fetchone()
        cur.close()
        return stats

async def updateRep(channelid,userid,rep):
    #if con is None or con.closed == 0:
    #    con = await getDbCon()
    if channelid is not None and userid is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        update = 'UPDATE "UserDetails" set "TotalReputation" = %s WHERE "ChannelID_UserID" = %s'
        updateparam = (rep,str(channelid) + "_" + str(userid),)
        cur = con.cursor()
        cur.execute(update,updateparam)
        con.commit()
        cur.close()

async def getTriviaCategory():
    s=""
    for key in triviaCategory.keys():
        s += key + "\n"
    return s

async def deleteCommandMessage(channelid,msgid):
    try:
        await client.delete_messages(channelid,msgid)
        #client(DeleteMessagesRequest(channelid, msgid))
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

async def getTopRep(channelid):
    if channelid is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        select = 'SELECT "TotalReputation","FirstName" FROM "UserDetails" WHERE "ChannelID" = %s order by "TotalReputation" DESC LIMIT 20'
        selectparam = (str(channelid),)
        cur = con.cursor()
        cur.execute(select,selectparam)
        reps = cur.fetchall()
        cur.close()
        return reps

async def getTopMsg(channelid):
    if channelid is not None:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        select = 'SELECT "TotalMessages","FirstName" FROM "UserDetails" WHERE "ChannelID" = %s order by "TotalMessages" DESC LIMIT 20'
        selectparam = (str(channelid),)
        cur = con.cursor()
        cur.execute(select,selectparam)
        reps = cur.fetchall()
        cur.close()
        return reps

async def getNews(term):
    try:
        if term is not None:
            googlenews = GoogleNews()
            googlenews = GoogleNews(lang='en')
            googlenews.set_encode('utf-8')
            googlenews.search(term)
            googlenews.get_page(1)
            result = googlenews.page_at(1)
            results = googlenews.results()
            rs = random.choice(results)
            return rs
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
async def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

async def get_meaning(word):
    dictionary = PyDictionary(word)
    info = dictionary.meaning(str(word))
    return info

async def eventData(event):
    replytomsgid = event.message.reply_to_msg_id
    if replytomsgid is not None:
        try:
            fromUserId = event.from_id
            fromUserEntity = await client.get_entity(fromUserId)
            fromUserName = fromUserEntity.username
            fromUserFirstName = fromUserEntity.first_name
            fromUserLastName = fromUserEntity.last_name
            channelId = event.message.to_id.channel_id
            channelEntity = await client.get_entity(channelId)
            msgSearch = await client.get_messages(channelId, ids=replytomsgid)
            toUserEntity = await client.get_entity(msgSearch.from_id)
            toUserId = toUserEntity.id
            toUserName = toUserEntity.username
            toUserFirstName = toUserEntity.first_name
            toUserLastName = toUserEntity.last_name
            eventDataList = [fromUserId,fromUserEntity,fromUserName,channelId,channelEntity,msgSearch,toUserEntity,toUserName,fromUserFirstName,fromUserLastName,toUserFirstName,toUserLastName,toUserId]
            return eventDataList
        except Exception as e:
            logging.exception("message")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    else:
        print('private chat')
        fromUserId = event.from_id
        fromUserEntity = await client.get_entity(fromUserId)
        fromUserName = fromUserEntity.username
        fromUserFirstName = fromUserEntity.first_name
        fromUserLastName = fromUserEntity.last_name
        channelId = event.message.to_id.channel_id
        channelEntity = await client.get_entity(channelId)
        msgSearch = ''
        toUserEntity = ''
        toUserId = ''
        toUserName = ''
        toUserFirstName = ''
        toUserLastName = ''
        eventDataList = [fromUserId,fromUserEntity,fromUserName,channelId,channelEntity,msgSearch,toUserEntity,toUserName,fromUserFirstName,fromUserLastName,toUserFirstName,toUserLastName,toUserId]
        return eventDataList

@client.on(events.NewMessage)
async def my_event_handler(event):
    try:
        myID = 1318065263
        channelId = event.message.to_id.channel_id
        msgid = event.message.id
        if channelId in eventDict:
            eventDict[channelId].append(msgid)
        else:
            eventDict[channelId] = [msgid]
            eventDict.pop(0)
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        replytomsgid = event.message.reply_to_msg_id
        toUserId = None
        if replytomsgid is not None:
            msgSearch = await client.get_messages(channelId, ids=replytomsgid)
            if msgSearch is not None:
                toUserEntity = await client.get_entity(msgSearch.from_id)
                toUserId = toUserEntity.id
        con = await getDbCon()
        channelEntity = await client.get_entity(channelId)
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        repEnabled = True
        profanityEnabled = False
        aichatEnabled = False
        welcomeEnabled = False
        leftEnabled = False
        fromUserId = event.from_id
        cur = con.cursor()
        #cur.callproc('"IncreaseMessageCount"', [str(channelId) + "_" + str(toUserId), ])
        #count = await getUserStats(channelId,fromUserId)
        #if count is None:
        #    count = 1
        #else:
        #    count = count[0] + 1

        if len(settings) == 0:
            await loadSettings()
        allsettings = json.loads(settings)
        for setting in allsettings:
            if setting["ChannelID"] == str(channelId):
                if setting["Reputation"] == True:
                    repEnabled = True
                else:
                    repEnabled = False
                if setting["Profanity"] == True:
                    profanityEnabled = True
                else:
                    profanityEnabled = False
                if setting["AIChat"] == True:
                    aichatEnabled = True
                else:
                    aichatEnabled = False
                if setting["Welcome"] == True:
                    welcomeEnabled = True
                else:
                    welcomeEnabled = False
                if setting["Left"] == True:
                    leftEnabled = True
                else:
                    leftEnabled = False
                if setting["Active"] == True:
                    isActive = True
                else:
                    isActive = False

        if profanityEnabled:
                if profanity.contains_profanity(event.raw_text.lower()):
                    await client(functions.channels.DeleteMessagesRequest(
                        channel=channelEntity,
                        id=[event.message.id]
                    ))
                    await client.send_message(channelId,message="Message was deleted because of profanity!")
            
        if event.raw_text.lower() == '.translate' or '.translate' in event.raw_text.lower():
                try:
                    cmd = event.raw_text.lower()
                    to_lang = cmd.replace('.translate ','').split(' ')[0]
                    if to_lang is not None and '.translate' not in to_lang and to_lang in googletrans.LANGCODES.values():
                        term = cmd.replace('.translate ','').replace(to_lang,'',1)
                        if term is not None:
                            translator = Translator()
                            translation = translator.translate(term,dest=to_lang)
                            await event.reply(translation.text)
                        else:
                            await event.reply('Provide data to translate!\n Example: .translate en gracias')
                    else:
                        term = cmd.replace('.translate ','').replace(to_lang + ' ','')
                        translator = Translator()
                        translation = translator.translate(term,dest='en')
                        await event.reply(translation.text)
                except Exception as e:
                    logging.exception("message")
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

        if event.raw_text.lower() == 'gif':
            header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            #url = "https://www.google.com/search?as_st=y&tbm=isch&hl=en-GB&as_q=art&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:70mp,itp:photo,ift:png"
            url = "https://gfycat.com/gifs/search/bye+bye"
            response = requests.get(url,headers=header)
            soup = BeautifulSoup(response.content,"html.parser")
            soup1 = soup.find_all("img")
            if len(soup1) > 0:
                imgsrc = random.choice(soup1)
                try:
                    await client.send_file(channelId,imgsrc['src'],force_document=False)
                except Exception as e:
                    print(e)
                    await event.reply("Oh snap! Try again later.")

        if myID == toUserId and event.raw_text.lower() not in cmds:
            responsedata = bot.get_response(event.raw_text.lower())
            if responsedata is None:
                await event.reply('I dont know what to reply!')
            else:
                await event.reply(responsedata.text)

    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.ChatAction)
async def chat_action_handler(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        channelId = event.chat.id
        welcomeEnabled = False
        leftEnabled = False
        welcomeText = ""
        leftText = ""
        userEntity = await client.get_entity(event.user_id)
        await AddUser(channelId,event.user_id,userEntity.first_name)
        await loadSettings()
        if len(settings) != 0:
            allsettings = json.loads(settings)
            for setting in allsettings:
                if setting["ChannelID"] == str(channelId):
                    if setting["Welcome"] == True:
                        welcomeEnabled = True
                        if setting["WelcomeText"] is None:
                            welcomeText = userEntity.first_name + " joined the group."
                        else:
                            welcomeText = setting["WelcomeText"]
                    else:
                        welcomeEnabled = False
                    if setting["Left"] == True:
                        leftEnabled = True
                        if setting["LeftText"] is None:
                            leftText = userEntity.first_name + " left the group."
                        else:
                            leftText = setting["LeftText"]
                    else:
                        leftEnabled = False

        if (event.user_joined or event.user_added) and welcomeEnabled:
            if "first_name" in welcomeText:
                welcomeText = welcomeText.replace("first_name",str(userEntity.first_name))
            if "user_name" in welcomeText:
                welcomeText = welcomeText.replace("user_name",str(userEntity.username))
            await event.reply(welcomeText)
            header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            #url = "https://www.google.com/search?as_st=y&tbm=isch&hl=en-GB&as_q=art&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:70mp,itp:photo,ift:png"
            url = "https://gfycat.com/gifs/search/welcome"
            response = requests.get(url,headers=header)
            soup = BeautifulSoup(response.content,"html.parser")
            soup1 = soup.find_all("img")
            if len(soup1) > 0:
                imgsrc = random.choice(soup1)
                try:
                    await client.send_file(channelId,imgsrc['src'],force_document=False)
                except Exception as e:
                    print(e)

        if (event.user_left or event.user_kicked) and leftEnabled:
            if "first_name" in leftText:
                leftText = leftText.replace("first_name",str(userEntity.first_name))
            if "user_name" in leftText:
                leftText = leftText.replace("user_name",str(userEntity.username))
            await event.reply(leftText)
            header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            #url = "https://www.google.com/search?as_st=y&tbm=isch&hl=en-GB&as_q=art&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:70mp,itp:photo,ift:png"
            url = "https://gfycat.com/gifs/search/bye+bye"
            response = requests.get(url,headers=header)
            soup = BeautifulSoup(response.content,"html.parser")
            soup1 = soup.find_all("img")
            if len(soup1) > 0:
                imgsrc = random.choice(soup1)
                try:
                    await client.send_file(channelId,imgsrc['src'],force_document=False)
                except Exception as e:
                    print(e)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.langcodes$'))
async def langcodes(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        s = googletrans.LANGUAGES
        listToStr = json.dumps(s)
        res = '\n'.join('{!r}: {!r},'.format(k, v) for k, v in s.items())
        await event.reply(res.rstrip(','))
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\++$'))
async def increaseRep(event):
    replytomsgid = event.message.reply_to_msg_id
    if replytomsgid is not None:
        try:
            con = await getDbCon()
            while con.closed == 1:
                con = await getDbCon()
            fromUserId = event.from_id
            fromUserEntity = await client.get_entity(fromUserId)
            fromUserName = fromUserEntity.username
            fromUserFirstName = fromUserEntity.first_name
            channelId = event.message.to_id.channel_id
            channelEntity = await client.get_entity(channelId)
            msgSearch = await client.get_messages(channelId, ids=replytomsgid)
            toUserEntity = await client.get_entity(msgSearch.from_id)
            toUserId = toUserEntity.id
            toUserName = toUserEntity.username
            toUserFirstName = toUserEntity.first_name
            toUserLastName = toUserEntity.last_name
            allsettings = json.loads(await loadSettings())
            for setting in allsettings:
                if setting["ChannelID"] == str(channelId):
                    if setting["Reputation"] == True:
                        repEnabled = True
                    else:
                        repEnabled = False

            if fromUserName == toUserName:
                    await event.reply('Nice Try, But NO ! You cannot give reputation to yourself !')
            else:
                if repEnabled == True:
                    await AddUser(channelId,toUserId,toUserFirstName)
                    cur = con.cursor()
                    cur.callproc('"IncreaseReputationCount"', [str(channelId) + "_" + str(toUserId), ])
                    con.commit()
                    count = await getUserStats(channelId,fromUserId)
                    print(count)
                    #if count is None:
                    #    countRep = 1
                    #else:
                    #    countRep = count[1] + 1
                    #await updateRep(channelId,toUserId,countRep)
                    await event.reply(fromUserFirstName + ' increased reputation of ' + toUserFirstName)
        except Exception as e:
            logging.exception("message")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^-+$'))
async def decreaseRep(event):
    replytomsgid = event.message.reply_to_msg_id
    if replytomsgid is not None:
        try:
            con = await getDbCon()
            while con.closed == 1:
                con = await getDbCon()

            fromUserId = event.from_id
            fromUserEntity = await client.get_entity(fromUserId)
            fromUserName = fromUserEntity.username
            fromUserFirstName = fromUserEntity.first_name
            fromUserLastName = fromUserEntity.last_name
            channelId = event.message.to_id.channel_id
            channelEntity = await client.get_entity(channelId)
            msgSearch = await client.get_messages(channelId, ids=replytomsgid)
            toUserEntity = await client.get_entity(msgSearch.from_id)
            toUserId = toUserEntity.id
            toUserName = toUserEntity.username
            toUserFirstName = toUserEntity.first_name
            allsettings = json.loads(await loadSettings())
            for setting in allsettings:
                if setting["ChannelID"] == str(channelId):
                    if setting["Reputation"] == True:
                        repEnabled = True
                    else:
                        repEnabled = False

            if fromUserName == toUserName:
                    await event.reply('Nice Try, But NO ! You cannot give reputation to yourself !')
            else:
                if repEnabled == True:
                    await AddUser(channelId,toUserId,toUserFirstName)
                    cur = con.cursor()
                    cur.callproc('"DecreaseReputationCount"', [str(channelId) + "_" + str(toUserId), ])
                    con.commit()
                    count = await getUserStats(channelId,fromUserId)
                    print(count)
                    #if count is None:
                    #    countRep = 0
                    #else:
                    #    countRep = count[1] - 1
                    #await updateRep(channelId,toUserId,count)
                    await event.reply(fromUserFirstName + ' decreased reputation of ' + toUserFirstName)
        except Exception as e:
            logging.exception("message")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.news [a-zA-Z]'))
async def getNewsData(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        command = event.raw_text.lower()
        term = command.replace('.news ','')
        newsData = await getNews(term)
        if newsData is not None:
            strg = newsData['title'] + '\nSource : ' + newsData['media'] + '\nLink : ' + newsData['link'] + '\nDesctiption : ' + newsData['desc']
            await event.reply(strg)
        else:
            await event.reply('Search topic was not provided or could not fetch news.')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.what [a-zA-Z]+$'))
async def getMeaning(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        search = event.raw_text.lower().replace('.what ','')
        if search is not None and '.what' not in search.lower():
            url = "https://www.vocabulary.com/dictionary/" + search + ""
            htmlfile = urllib2.urlopen(url)
            soup = BeautifulSoup(htmlfile, 'html.parser')
            soup1 = soup.find(class_="short")
            try:
                soup1 = soup1.get_text()
            except AttributeError:
                soup1 = 'Cannot find such word! Check spelling.'
        await event.reply(soup1)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.cmd$'))
async def getCommands(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        await event.reply(cmds)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.m$'))
async def mute(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        replytomsgid = event.message.reply_to_msg_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        msgSearch = await client.get_messages(channelId, ids=replytomsgid)
        channelEntity = await client.get_entity(channelId)
        toUserEntity = await client.get_entity(msgSearch.from_id)
        toUserId = toUserEntity.id
        toUserName = toUserEntity.username
        toUserFirstName = toUserEntity.first_name
        if isadmin or iscreator:
            await client.edit_permissions(channelEntity, toUserEntity, timedelta(minutes=60),send_messages=False)
            await event.reply(toUserFirstName + ', you are muted upto 1 hour for not following rules!.')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.um$'))
async def unmute(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        replytomsgid = event.message.reply_to_msg_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        msgSearch = await client.get_messages(channelId, ids=replytomsgid)
        channelEntity = await client.get_entity(channelId)
        toUserEntity = await client.get_entity(msgSearch.from_id)
        toUserId = toUserEntity.id
        toUserName = toUserEntity.username
        toUserFirstName = toUserEntity.first_name
        if isadmin or iscreator:
            await client.edit_permissions(channelEntity, toUserEntity, timedelta(minutes=0),send_messages=True)
            await event.reply(toUserFirstName + ', you are unmuted!.')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.b$'))
async def ban(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        replytomsgid = event.message.reply_to_msg_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        msgSearch = await client.get_messages(channelId, ids=replytomsgid)
        channelEntity = await client.get_entity(channelId)
        toUserEntity = await client.get_entity(msgSearch.from_id)
        toUserId = toUserEntity.id
        toUserName = toUserEntity.username
        toUserFirstName = toUserEntity.first_name
        if isadmin or iscreator:
            await client.edit_permissions(channelEntity, toUserEntity, timedelta(minutes=0),view_messages=False)
            await event.reply(toUserFirstName + ', you are banned!.')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.ub$'))
async def unban(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        replytomsgid = event.message.reply_to_msg_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        msgSearch = await client.get_messages(channelId, ids=replytomsgid)
        channelEntity = await client.get_entity(channelId)
        toUserEntity = await client.get_entity(msgSearch.from_id)
        toUserId = toUserEntity.id
        toUserName = toUserEntity.username
        toUserFirstName = toUserEntity.first_name
        if isadmin or iscreator:
            await client.edit_permissions(channelEntity, toUserEntity, timedelta(minutes=0),view_messages=True)
            await event.reply(toUserFirstName + ', you are unbanned!.')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
    
@client.on(events.NewMessage(pattern=r'^\.stat$'))
async def getUserStat(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        cur = con.cursor()
        selectparam = (str(channelId) + "_" + str(fromUserId))
        select = """ SELECT "TotalReputation" FROM "UserDetails" WHERE "ChannelID_UserID" = '{}' """.format(selectparam)
        cur.execute(select)
        data = cur.fetchall()
        if data is not None:
            for row in data:
                s = "Total Reputation : "+str(int(row[0]))
                await event.reply(s)
        cur.close()
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
@client.on(events.NewMessage(pattern=r'^\.joke$'))
async def getJoke(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = "https://v2.jokeapi.dev/joke/Any";
        data = requests.get(url = URL)
        data = data.json()
        joke = data['setup'] + '\n' + data['delivery'] + '\n\n\n' + 'Jokes are generated randomly.Dont get emotional! :v:'
        joke = emoji.emojize(joke, use_aliases=True)
        await event.reply(joke)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.yomama$'))
async def getYomama(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = "https://api.yomomma.info/"
        data = requests.get(url = URL)
        yomama = data.json()
        await event.reply(yomama['joke'])
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
@client.on(events.NewMessage(pattern=r'^\.quote$'))
async def getQuote(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=jsonp&jsonp=?"
        data = requests.get(url = URL)
        response = data.text[1:]
        qData = json.loads(response.replace("(","").replace(")",""))
        await event.reply(qData['quoteText'] + '\n\n' + 'By - ' + qData['quoteAuthor'])
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.bored$'))
async def getActivity(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = "https://www.boredapi.com/api/activity"
        data = requests.get(url = URL)
        activity = data.json()
        activityData = activity['activity']
        await event.reply(activityData)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.insult$'))
async def getInsulted(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        data = requests.get(url = URL)
        insult = data.json()
        insultData = insult['insult']
        await event.reply(insultData)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.advice$'))
async def getAdvice(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = "https://api.adviceslip.com/advice"
        data = requests.get(url = URL)
        advice = data.json()
        adviceData = advice['slip']['advice']
        await event.reply(adviceData)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.dadjoke$'))
async def getDadJoke(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = "https://icanhazdadjoke.com/"
        htmlfile = requests.get(url = URL)
        soup = BeautifulSoup(htmlfile.text, 'html.parser')
        soup1 = soup.find('p', attrs={'class' : 'subtitle'})
        await event.reply(soup1.get_text())
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.ping$'))
async def getPing(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        m = await event.respond('!pong')
        time.sleep(3)
        await client.delete_messages(event.chat_id, [event.id, m.id])
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.startbot$'))
async def startBot(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        await event.reply('Wait!')
        channelEntity = await client.get_entity(channelId)
        await AddClient(channelEntity)
        await event.reply('Working now!')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.reputation (?i)(true|false)$'))
async def updateReputationSettings(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if event.raw_text.lower() == '.reputation true' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Reputation","true")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                

        if event.raw_text.lower() == '.reputation false' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Reputation","false")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.profanity (?i)(true|false)$'))
async def updateProfanitySettings(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
                try:
                    con = await getDbCon()
                except psycopg2.OperationalError:
                    continue

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if event.raw_text.lower() == '.profanity true' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Profanity","true")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                

        if event.raw_text.lower() == '.profanity false' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Profanity","false")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.welcome (?i)(true|false)$'))
async def updateWelcomeSettings(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if event.raw_text.lower() == '.welcome true' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Welcome","true")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                

        if event.raw_text.lower() == '.welcome false' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Welcome","false")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.left (?i)(true|false)$'))
async def updateLeftSettings(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if event.raw_text.lower() == '.left true' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Left","true")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                

        if event.raw_text.lower() == '.welcome false' and (isadmin or iscreator):
            try:
                
                await UpdateClientSettings(channelId,"Left","false")
                await event.reply('Settings Updated!')
            except Exception as e:
                logging.exception("message")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.welcometext (.*)?$'))
async def updateWelcomeText(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if isadmin or iscreator:
            
            text = event.raw_text.lower().replace(".welcometext","",1)
            if text is not None:
                await UpdateClientSettings(channelId,"WelcomeText",text)
                await event.reply('Settings Updated!')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.lefttext (.*)?$'))
async def updateLeftText(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if isadmin or iscreator:
            
            text = event.raw_text.lower().replace(".lefttext","",1)
            if text is not None:
                await UpdateClientSettings(channelId,"LeftText",text)
                await event.reply('Settings Updated!')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.profaneadd \w+$'))
async def addProfaneWord(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if isadmin or iscreator:
            word = event.raw_text.lower().replace('.profaneadd')
            profanity.add_censor_words(word)
            await event.reply('Word Added!')
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.art$'))
async def getArt(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        await event.reply("Wait ! Let me find art for you.")
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        #url = "https://www.google.com/search?as_st=y&tbm=isch&hl=en-GB&as_q=art&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:70mp,itp:photo,ift:png"
        url = "https://unsplash.com/s/photos/art?order_by=latest"
        response = requests.get(url,headers=header)
        soup = BeautifulSoup(response.content,"html.parser")
        soup1 = soup.find_all("img")
        if len(soup1) > 0:
            imgsrc = random.choice(soup1)
            image = Image.open(BytesIO(requests.get(imgsrc['src']).content))
            image.save("art.png")
            imgbyte = image_to_byte_array(image)
            try:
                await client.send_file(channelId,imgbyte,force_document=False,caption=imgsrc["alt"])
            except Exception as e:
                print(e)
                await event.reply("Oh snap! Try again later.")
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        

@client.on(events.NewMessage(pattern=r'^\.trv$'))
async def getTrv(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        URL = triviaUrl
        data = requests.get(url = URL)
        trivia = json.loads(data.text)
        results = trivia.get('results')
        category = results[0]['category']
        difficulty = results[0]['difficulty']
        question_data = html.unescape( "Category : " + category + "\n" + "Difficulty : " + difficulty + "\n" + results[0]['question'])
        correct_answer = results[0]['correct_answer']
        incorrect_answer = results[0]['incorrect_answers']
        incorrect_answer.append(correct_answer)
        random.shuffle(incorrect_answer)
        correct_answer_id = incorrect_answer.index(correct_answer)
        await client.send_message(channelId,file=InputMediaPoll(
            poll=Poll(
                id=53453159,
                question=question_data,
                answers=[PollAnswer(incorrect_answer[0], b'0'), PollAnswer(incorrect_answer[1], b'1'), PollAnswer(incorrect_answer[2], b'2'), PollAnswer(incorrect_answer[3], b'3')],
                closed=None,quiz=True,multiple_choice=None,public_voters=True
            ),correct_answers=str(correct_answer_id)
        ))
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
@client.on(events.NewMessage(pattern=r'^\.toprep$'))
async def topRep(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        reps = await getTopRep(channelId)
        s=""
        for rep in reps:
            s += rep[1] + "(" + str(rep[0]) + ")" + "\n"
        if s != "" or s is not None:
            await event.reply(s)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
@client.on(events.NewMessage(pattern=r'^\.mrep$'))
async def getme(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        reps = await getUserStats(channelId,fromUserId)
        s = "TotalReputation : "
        for t in reps:
            s += str(t)
        if s != "" or s is not None:
            await event.reply(s)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.yrep$'))
async def getyou(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()
        channelId = event.message.to_id.channel_id
        replytomsgid = event.message.reply_to_msg_id
        if replytomsgid is not None:
            msgSearch = await client.get_messages(channelId, ids=replytomsgid)
            toUserEntity = await client.get_entity(msgSearch.from_id)
            toUserId = toUserEntity.id
            toUserName = toUserEntity.username
            toUserFirstName = toUserEntity.first_name
            reps = await getUserStats(channelId,toUserId)
            s = "TotalReputation : "
            for t in reps:
                s += str(t)
            if s != "" or s is not None:
                await event.reply(s)
    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@client.on(events.NewMessage(pattern=r'^\.clean$'))
async def clean(event):
    try:
        con = await getDbCon()
        while con.closed == 1:
            con = await getDbCon()

        fromUserId = event.from_id
        channelId = event.message.to_id.channel_id
        channelEntity = await client.get_entity(channelId)
        participant = await client(GetParticipantRequest(channel=event.original_update.message.to_id.channel_id,user_id=event.original_update.message.from_id))
        isadmin = (type(participant.participant) == ChannelParticipantAdmin)
        iscreator = (type(participant.participant) == ChannelParticipantCreator)
        if isadmin or iscreator:
            filter = InputMessagesFilterEmpty()
            result = client(SearchRequest(
                peer=channelEntity,  # On which chat/conversation
                q='',  # What to search for
                filter=filter,  # Filter to use (maybe filter for media)
                min_date=None,  # Minimum date
                max_date=None,  # Maximum date
                offset_id=0,  # ID of the message to use as offset
                add_offset=0,  # Additional offset
                limit=5,  # How many results
                max_id=0,  # Maximum message ID
                min_id=0,  # Minimum message ID
                from_id=None,  # Who must have sent the message (peer)
                hash=0  # Special number to return nothing on no-change
            ))

            async for message in client.iter_messages(channelEntity,filter=result):
                print(message.message)
            events = eventDict[channelId]
            affected = await client.delete_messages(channelId, events)
            if len(affected) > 0:
                await event.reply("Cleaned!")
            else:
                await event.reply("Something went wrong!")

    except Exception as e:
        logging.exception("message")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        
client.run_until_disconnected()
