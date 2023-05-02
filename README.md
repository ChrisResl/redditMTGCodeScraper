# redditMTGCodeScraper

## A script for detecting redeemable codes posted on the Magic Arena subreddit and sent to your mobile phone

This tool utilizes the Praw framework to scrape the MTG Arena subreddit for redemption codes that can be used in the game's store. The script is designed to monitor the subreddit every minute and only report codes that have not already been reported that day, as older ones will already be redeemed and are no longer relevant. To automate this process, scheduling is achieved through the use of a cron script.


## Setup

* Create a Telegram bot: https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot <br />
   Note the token.
* Create a Reddit app under https://www.reddit.com/prefs/apps <br />
Choose a name (eg. magicbot) and select "script". For "redirect uri" set ```http://localhost:8080``

* Clone the repository
* Setup of environment <br />
```conda create -n python=3.11.3 redditMTGCodeScrapper pip```<br />
```pip install -r requirements.txt```

* In Telegram, initiate a conversation with your bot by typing ```/start```
* In the telegram_id.py script fill in the token information received upon setup of the Telegram bot and run the script to get chat id
* Information obtained in the previous two steps will be added to ``send_message_to_telegram()``` in the reddit_scraper.py file 
* Complete the praw.ini file with your reddit account and script information
* Setup of ```cron``` to schedule script <br />
In terminal: ```crontab -e``` <br />
```*/1 * * * * cd <path-to-project-directory> && source <path-to-conda-activate-file> <environment-name>; <path-to-conda-python> <path-to-reddit-scrapper.py-file>``` <br />
Example: <br />
```*/1 * * * * cd /home/chris/Workspace/redditMTGCodeScrapper && source /home/chris/anaconda3/bin/activate redditMTGCodeScrapper; /home/chris/anaconda3/envs/redditMTGCodeScrapper/bin/python /home/chris/Workspace/redditMTGCodeScrapper/reddit_scrapper.py```

* To check if everything is working as intended, a log file was included, reporting at which times the script has been executed.

## Dependencies
* pandas==2.0.1
* praw==7.7.0
* Requests==2.29.0

##  End result

<img src="./images/example1.jpeg" alt="Alt text" width="400" height="600"> <img src="./images/example2.jpeg" alt="Alt text" width="400" height="600"> 
