import telebot
from telebot import types
from decouple import config
import urllib , requests , random , unicodedata , re
from pathlib import Path

API_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(API_TOKEN , parse_mode="markdown")
helpCommands= '''
/start check if bot offline or not!\n
send your post formast like:\n
Title\n
Tags\n
Link
'''

@bot.message_handler(commands=['start'])
def send_welcome(message : types.Message):
  bot.reply_to(message, helpCommands)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message : types.Message):
  arr = message.text.split("\n")
  title = '*'+ arr[0] + '*'
  tags = getTags(arr[1])
  link = shortURL(arr[2])
  caption = title  + '\n\n' +  tags + '\n\n' + link
  photo = downloadimages(random.choice(getTags(arr[1] , True)))
  # bot.send_message(chat_id=config('CHANNEL_IDS') ,text="\n".join(arr) ,parse_mode="markdown")
  bot.send_photo(chat_id=config('CHANNEL_IDS') ,photo=photo, caption=caption)

def shortURL(URL):
  key = config('CUTTLY_TOKEN')
  parsedURL = urllib.parse.quote(URL)
  r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(key, parsedURL))
  data = r.json()
  return data['url']['shortLink']

def downloadimages(search_term): # Define the function to download images
  print(f"https://source.unsplash.com/random/900x600/?"+str(search_term)+", allow_redirects=True") # State the URL
  path = Path("D:\\Ali\\Projects\\telegram-snippet-bot\\assets")
  savePath = str(path) + "\\" + str(search_term) + ".png"
  # Loop for chosen amount of times
  # Download the photo(s)
  _get = lambda search_term : requests.get(f"https://source.unsplash.com/random/900x600/?"+str(search_term)+", allow_redirects=True")
  response = _get(search_term)
  _404 = "https://images.unsplash.com/source-404?fit=crop&fm=jpg&h=800&q=60&w=1200"
  if response.url == _404 : response = _get("")
  # State the filename
  print("Saving to:" + savePath)
  # Write image file
  open(savePath, 'wb').write(response.content)
  return response.content

def sanitize(value, allow_unicode=False):
  value = str(value)
  if allow_unicode:
    value = unicodedata.normalize('NFKC', value)
  else:
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'[-\s\_]+', ' ', value).strip(' _')


def getTags(str , raw = False):
  arr = str.split(" ")
  arr = ["#" + x.lower() for x in arr]
  return str.split(" ") if raw else " ".join(arr)  

bot.infinity_polling()