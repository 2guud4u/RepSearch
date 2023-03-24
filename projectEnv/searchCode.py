import praw
from praw.models import MoreComments
from search import *
#TODO change login into oauth instead of password
r = praw.Reddit(
    client_id='jknOULmDh_Xkmi5xLSpl_A',
    client_secret='5jOGVzfdgGJgRrxS7oPZAzaBZnndEA',
    user_agent="smol man",
)
#post object
class post:
    def __init__(self, url, rating, title, wtc):
        self.url = url
        self.rating = rating
        self.title = title
        self.wtc = wtc 
    def __str__(self):
        return f'Post name is {self.title} with rating {self.rating} Link: {self.url}\n'
    

def sortRating(s):
    return s.rating

def getRating(comments):   
    rating = 0
    comments.replace_more(limit=None) #replace all unloaded comment obj with loaded comments
    for comment in comments:
        rating += sentiment_scores(comment.body)
    return rating
def searchItem(prompt):
    post_list = []

    #grabs posts based on prompt
    for s in r.subreddit("FashionReps").search(query=prompt,
                                                    sort="relevance", 
                                                    limit=5, 
                                                    time_filter= "year"):
        post_list.append(post("https://www.reddit.com"+ s.permalink, 
                            getRating(s.comments), 
                            s.title, 
                            s.url))

    post_list.sort(key=sortRating, reverse = True)#sort the post obj in order of rating
    
    return post_list