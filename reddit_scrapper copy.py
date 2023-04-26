import praw
from time import sleep
import pandas as pd
from os.path import exists
import requests
import datetime

# Get credentials from DEFAULT instance in praw.ini
reddit = praw.Reddit()

class SubredditScrapper:

    def __init__(self, sub, sort='new', lim = 50):
        """Constructor
        Args:
            sort: category of the subreddit where scraping occurs
            lim: number of posts that should be scraped
        """
        self.sub = sub
        self.sort = sort
        self.lim = lim

    def get_posts_new(self):
        """Getting posts in certain subreddit in new category
        Returns:
            post objects
        """
        if self.sort == 'new':
            return self.sort, reddit.subreddit(self.sub).new(limit=self.lim)

    def get_relevant_posts(self, checkedPosts):
        """Going through Subreddit and getting posts in "new" category
        Args:
            checkedPosts: pandas Dataframe containig information about posts already checked
        Returns:
            dictionary of posts fulfilling criteria"""
        sub_dict = checkedPosts.to_dict('list')

        new_posts = {'id':[],'time':[], 'url': []}
        sort, subreddit = self.get_posts_new()

        for post in subreddit:
            #converting float time into datetime object
            date_obj = datetime.datetime.fromtimestamp(post.created_utc).date() # with date() method at end only date portion is extracted
            
            if (datetime.date.today() == date_obj) and (post.id not in sub_dict["id"]) and (find_word_in_text("code",post.title) or find_word_in_text("code", post.selftext)):
                new_posts['id'].append(post.id)
                new_posts['url'].append(post.url)
                new_posts['time'].append(datetime.datetime.utcfromtimestamp(post.created_utc))
             
            sleep(0.1)
        return new_posts

    def send_message_to_telegram(post_dict):
        """Sending new posts to telegram as a message
        Args: 
            post_dict: dictionary of new posts
        """
        if len(post_dict["id"]) > 0 :
            TOKEN = "TOKEN" #information from telegram_id.py
            chat_id = "chat_id" #information from telegram_id.py
            message = ''
            for url in post_dict['url']:
                message += '* ' + str(url) + ' *\n'

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url).json()

    def write_posts_to_csv(post_dict):
        """Saving new posts to output csv file
        Args:
            post_dict: dictionary of new posts
        """
        if len(post_dict["id"]) > 0 :
            post_dict = pd.DataFrame(post_dict)
            post_dict.to_csv("mtg_arena_code_links.csv", header=False, index=False, mode="a")

    def check_file_exist(filepath):
        """Check if a file already exists
        Args:
            filepath: string
        Returns:
            boolean
        """
        return exists(filepath)

    def read_in_csv(filepath):
        """Reading in a csv file containing information about subreddit posts
        Args:
            filepath: string
        Returns:
            pandas dataframe of subreddit post information
        """
        csvFile = pd.read_csv(filepath)
        return csvFile
    
    def create_output_file(filepath):
        """Creating an output file to store subreddit post information
        Args:
            filepath: string 
        """
        with open(filepath, mode='w') as file:
            file.write("id,time,url")
            file.close()
    
def find_word_in_text(word, text):
        """Looking through a text to find if a certain word is present or not.
        Args:
            word: string
            text: string
        Returns:
            boolean
        """
        return word in text.lower()

        
if __name__ == '__main__':
    csvExist = SubredditScrapper.check_file_exist("./mtg_arena_code_links.csv")
    if not csvExist:
        SubredditScrapper.create_output_file("./mtg_arena_code_links.csv")
        checkedPosts = SubredditScrapper.read_in_csv("./mtg_arena_code_links.csv")
    else:
        checkedPosts = SubredditScrapper.read_in_csv("./mtg_arena_code_links.csv")

    newPosts = SubredditScrapper('MagicArena').get_relevant_posts(checkedPosts)

    SubredditScrapper.write_posts_to_csv(newPosts)
    SubredditScrapper.send_message_to_telegram(newPosts)