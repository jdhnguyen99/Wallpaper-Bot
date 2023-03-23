import json
import discord
import random
import math
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from discord.ext import commands,tasks
secrets = json.load(open("secrets.json"))

#XPATH Samples
#//*[@id="profileBlock"]/div/div[3]/div[1]
#//*[@id="profileBlock"]/div/div[3]/div[20]
#//*[@id="profileBlock"]/div/div[3]/div[27]
#//*[@id="profileBlock"]/div/div[3]/div[13]

#https://steamcommunity.com/workshop/browse/?appid=431960&browsesort=trend&section=readytouseitems&requiredtags%5B0%5D=Relaxing&requiredtags%5B1%5D=Everyone&excludedtags%5B0%5D=Abstract&excludedtags%5B1%5D=Anime&excludedtags%5B2%5D=Memes&created_date_range_filter_start=0&created_date_range_filter_end=0&updated_date_range_filter_start=0&updated_date_range_filter_end=0&actualsort=trend&p=1&days=1

def wallpaperRandomizer():
    options = Options()
    options.headless = True
    chrome_service = Service('./chromedriver')
    driver = webdriver.Chrome(service=chrome_service,chrome_options=options)
    pageNum = random.randint(1,2)
    wallpaperUrl = f"https://steamcommunity.com/workshop/browse/?appid=431960&browsesort=trend&section=readytouseitems&requiredtags%5B0%5D=Relaxing&requiredtags%5B1%5D=Everyone&excludedtags%5B0%5D=Abstract&excludedtags%5B1%5D=Anime&excludedtags%5B2%5D=Memes&created_date_range_filter_start=0&created_date_range_filter_end=0&updated_date_range_filter_start=0&updated_date_range_filter_end=0&actualsort=trend&p={pageNum}&days=1"
    driver.get(wallpaperUrl)
    
    #for loop iterating through all 30 wallpapers on 1 page to check if there are stars.
    wallpaperArray = []
    for i in range(1,30):
        substring4 = '4-star'
        substring5 = '5-star'
        string = driver.find_element(By.XPATH, f'//*[@id="profileBlock"]/div/div[3]/div[{i}]/img[2]').get_attribute('src')
        if substring4 in string or substring5 in string:
            wallpaperArray.append(i)
    
    #Randomizes the integer from the size of the array to pick out the element index
    randomWallpaperArrayInt = random.randint(0,len(wallpaperArray)-1)
    intForImage = wallpaperArray[randomWallpaperArrayInt]

    #click action
    clickable = driver.find_element(By.XPATH,f'//*[@id="profileBlock"]/div/div[3]/div[{intForImage}]')
    ActionChains(driver)\
        .click(clickable)\
        .perform()
    title = driver.find_element(By.XPATH, '//*[@id="mainContents"]/div[5]/div[2]').text
    printString = driver.current_url
    driver.close()
    
    
    # reading through the list line by line
    with open('UrlList.txt','r') as f:
        file_content = f.read()
        for line in f:
            if line.strip() == title:
                return wallpaperRandomizer()
    
    # writing a list for all wallpapers posted
    with open('UrlList.txt','a') as f:
        f.write(title + "\n")
        
    return title, printString

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# my userID: 186332743150338048
@client.event
async def on_message(message):
    if message.author.id == client.user:
        return
    if message.content.startswith('!wallpaper'):
        message.channel.send("I hear you! Give me a moment...")
        title,url = wallpaperRandomizer()
        await message.channel.send(title + "\n" + url)

#TODO: make a Already Posted file to do a check.
#      make asynchronous

client.run(secrets['token'])
