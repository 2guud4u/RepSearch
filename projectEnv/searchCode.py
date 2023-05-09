import praw
from praw.models import MoreComments
from search import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from praw.models.util import stream_generator

cur_prompt=""
processed_ids = set()
post_list = []

#TODO change login into oauth instead of password
r = praw.Reddit(
    client_id='jknOULmDh_Xkmi5xLSpl_A',
    client_secret='5jOGVzfdgGJgRrxS7oPZAzaBZnndEA',
    user_agent="smol man",
)
#post object
class post:
    def __init__(self, url, rating, title, wtc, post_id, cached):
        self.url = url
        self.rating = rating
        self.title = title
        self.wtc = wtc 
        self.post_id = post_id
        self.cached = cached
    def __str__(self):
        return f'Post name is {self.title} with rating {self.rating} Link: {self.url} id: {self.url}\n'
    
def get_data_if_exist(p_key):
    from databases.dataModels import Product
    record = Product.query.get(p_key)
    
    if record is not None:
        return record.score
    else:
        return False
    
def sortRating(s):
    return s.rating

def getRating(comments):   
    rating = 0
    comments.replace_more(limit=None) #replace all unloaded comment obj with loaded comments
    for comment in comments:
        rating += sentiment_scores(comment.body)
    return rating
def addToPosts(p_data):
#look for cached data
        cached= True
        rating = get_data_if_exist(p_data.id)    
        if rating == False:
            rating = getRating(p_data.comments)
            cached = False
        #add to processed post
        processed_ids.add(p_data.id)
        post_list.append(post("https://www.reddit.com"+ p_data.permalink, 
                            rating, 
                            p_data.title, 
                            p_data.url, 
                            p_data.id, 
                            cached))

        post_list.sort(key=sortRating, reverse = True)#sort the post obj in order of rating
    
def searchItem(db,prompt):
    cur_prompt = prompt
    
    #purge old processed_ids
    processed_ids.clear()

    #grabs posts based on prompt
    for s in r.subreddit("FashionReps").search(query=prompt,
                                                    sort="relevance", 
                                                    limit=6, 
                                                    time_filter= "year"):
        addToPosts(p_data)
    post_list.sort(key=sortRating, reverse = True)#sort the post obj in order of rating
    return post_list

def loadMore():
    #add 6 more
    newNum = 0
    while(newNum >= 6):
        for post in stream_generator(r.subreddit("FashionReps").search(query=cur_prompt,
                                                                    sort="relevance", 
                                                                    limit=1, 
                                                                    time_filter= "year")
                                                        , skip_existing=True):
            if post.id not in processed_ids:
                # Process the post here
                addToPosts(post)
                newNum += 1
        
        break      
    post_list.sort(key=sortRating, reverse = True)#sort the post obj in order of rating
    return post_list