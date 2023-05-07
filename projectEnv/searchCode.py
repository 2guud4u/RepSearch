import praw
from praw.models import MoreComments
from search import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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
def searchItem(db,prompt):
    post_list = []

    #grabs posts based on prompt
    for s in r.subreddit("FashionReps").search(query=prompt,
                                                    sort="relevance", 
                                                    limit=5, 
                                                    time_filter= "year"):
        #look for cached data
        cached= True
        rating = get_data_if_exist(s.id)    
        if rating == False:
            rating = getRating(s.comments)
            cached = False
        post_list.append(post("https://www.reddit.com"+ s.permalink, 
                            rating, 
                            s.title, 
                            s.url, 
                            s.id, 
                            cached))

    post_list.sort(key=sortRating, reverse = True)#sort the post obj in order of rating
    
    return post_list