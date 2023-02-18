import sqlite3
import pymongo
from pyrogram import Client, filters
from telegram.ext import CommandHandler

API_ID = ""
API_HASH = ""
BOT_TOKEN = ""

VPCREATION=Client(
    name="searchfromcommand",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


print("Bot Started !")

# Connects to the client of MongoDB 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")  

# Set up database and collection 
db = myclient['sharedFiles'] 
filesCollection = db["files"] 

# Connecting to the SQLite database  
connection = sqlite3.connect("FileSearch.db") 
crsr = connection.cursor() 

# Function to search file from SQLite Database  
def search_sqlite_file(update, context):    

    # Taking keyword as input from user  
    kwrd = context.args[0] 

    # SQL query to search file with given keyword  
    query = "SELECT * FROM Files WHERE Name LIKE '%{}%'".format(kwrd)

    crsr.execute(query)     

    ans = crsr.fetchall()  

    if ans: 
        message = "File name and File type associated with {} are : \n".format(kwrd) 

        for i in ans:             
            message += 'File Name : {} and File Type : {}\n'.format(i[0], i[1])         

    else:    
        message = "No file found"   

    update.message.reply_text(message)

# function to use mongodb to search for files 
def search_mongodb_file(update, context): 

    # Retrieving data from the mongodb collection - Pass search query as argument  
    searchedFilesCursor = filesCollection.find({"name": context.args[0]}) 

    # Loop over the retrieved documents and display their "name" field  
    message = "Files found:\n"
    for file in searchedFilesCursor: 
        message += file["name"] + "\n"

    if message == "Files found:\n":
        message = "No file found"

    update.message.reply_text(message)

# creating handlers
sqlite_handler = CommandHandler('sqlite', search_sqlite_file)
mongodb_handler = CommandHandler('mongodb', search_mongodb_file)

# adding handlers to dispatcher
dispatcher.add_handler(sqlite_handler)
dispatcher.add_handler(mongodb_handler)

bot.run()
