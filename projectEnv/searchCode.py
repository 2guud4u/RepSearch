import praw
from praw.models import MoreComments
from search import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from praw.models.util import stream_generator

cur_prompt= ""

post_list = []
total_post_list = []
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
        print("not found", p_key)
        return False
    
def sortRating(s):
    return s.rating

def getRating(prpost):   
    rating = 0
    sentrating = 0
    sentnum = 0
    prpost.comments.replace_more(limit=None) #replace all unloaded comment obj with loaded comments
    # rating from the comment lin reg
    baserate = linreg(prpost)
    for comment in prpost.comments:
        sentrating += sentiment_scores(comment.body)
        sentnum = sentnum + 1
    rating = baserate * (1 + (sentrating / sentnum))
    return rating



def addToPosts(p_data):
#look for cached data
    cached= True
    rating = get_data_if_exist(p_data.id)    
    if rating == False:
        print("getting ratings", p_data.id)
        rating = getRating(p_data)
        cached = False
        print("not cached")
    #add to processed post
        print("not cached")
    #add to processed post
    
    post_list.append(post("https://www.reddit.com"+ p_data.permalink, 
                        rating, 
                        p_data.title, 
                        p_data.url, 
                        p_data.id, 
                        cached))

    
def searchItem(db,prompt):

    # purge old processed_ids and posts
    
    post_list.clear()
    total_post_list.clear()
    #grabs posts based on prompt
    for i in r.subreddit("FashionReps").search(query=prompt,
                                                    sort="relevance", 
                                                    limit=24, 
                                                    time_filter= "year"):
        total_post_list.append(i)
    #add first 6 posts
    print("looked for posts")
    for s in total_post_list[:6]:
        addToPosts(s)
        
    post_list.sort(key=sortRating, reverse = True)#sort the post obj in order of rating
   
    return post_list

def loadMore():
    #add 6 more
    #remove previous 6
    del total_post_list[:6]
    for s in total_post_list[:6]:
        print("loaded one")
        addToPosts(s)

    
    post_list.sort(key=sortRating, reverse = True)#sort the post obj in order of rating
    return post_list
