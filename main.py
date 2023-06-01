from datetime import datetime
from discord.ui import button
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
load_dotenv()

def run_chrome():
    global driver
    driver = webdriver.Chrome()
    url="https://www.twitter.com/login"
    driver.get(url)
    driver.maximize_window()

def Account_login():

    tweetUSer = os.environ.get('user')
    tweetPass = os.environ.get('pass')
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))).send_keys(
        tweetUSer)
    time.sleep(random.uniform(1, 2))
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))).send_keys(
        Keys.ENTER)
    time.sleep(random.uniform(1, 3))
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))).send_keys(
        tweetPass)
    time.sleep(random.uniform(2, 3))
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))).send_keys(
        Keys.ENTER)
    time.sleep(random.uniform(1, 3))


links = []
url = []

def dataTweet():
    global url
    global links
    driver.get("https://twitter.com/ThomasLoydPub")
    time.sleep(5)
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True
    while scrolling:
        soup = BeautifulSoup(driver.page_source,'html.parser')
        anchor_tags = soup.find_all("a", href=lambda href: href and "/ThomasLoydPub/status/" in href)
        for anchor_tag in anchor_tags:
            href = anchor_tag.get("href")
            if not href.endswith("/analytics"):
                timestamp = anchor_tag.find("time")["datetime"]
                full_link = "https://twitter.com" + href
                links.append({"link": full_link, "timestamp": timestamp})

        sorted_links = sorted(links, key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"))

        for link in sorted_links:
            if link["link"] not in url:
                url.append(link["link"])
                print("Link:", link["link"])
                print("Timestamp:", link["timestamp"])
                print("----------------------")

        scroll_attempt = 0
        while True:
            driver.execute_script("window.scrollBy(0, 250);")
            time.sleep(0.5)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    time.sleep(2)
            else:
                last_position = curr_position
                break
    driver.close()


def reply_to_message(update, context):
    text = update.message.text.lower()
    if text != '/start':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Twitter Bot Use /start to start")


def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Recent Tweets", callback_data='recent')],
        [InlineKeyboardButton("New Tweet", callback_data='new')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please select an option:",
                             reply_markup=reply_markup)


def button_click(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data='menu')],
    ]

    reply_Home = InlineKeyboardMarkup(keyboard)
    if query.data == 'recent':
        for link in url:
            context.bot.send_message(chat_id=query.message.chat_id, text=link)
        query.message.reply_text(text="You are viewing tweets.", reply_markup=reply_Home)

    elif query.data == 'new':
        for link in url:
            context.bot.send_message(chat_id=query.message.chat_id, text=link)
        query.message.reply_text(text=link, reply_markup=reply_Home)
    elif query.data == 'menu':
        print("hey")
        start(update, context)


def telleBot():
    TOKEN = "5999504644:AAHVRZqCdLMdieI1su1saRmG-47Sq505_dg"
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CallbackQueryHandler(button_click, pattern='recent'))
    dispatcher.add_handler(CallbackQueryHandler(button_click, pattern='new'))
    dispatcher.add_handler(CallbackQueryHandler(button_click, pattern='menu'))
    message_handler = MessageHandler(Filters.text, reply_to_message)
    dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()



run_chrome()
Account_login()
dataTweet()
telleBot()

