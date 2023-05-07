import praw
import random
from praw.models import MoreComments
from search import *
import time
#TODO change login into oauth instead of password
r = praw.Reddit(
    client_id='jknOULmDh_Xkmi5xLSpl_A',
    client_secret='5jOGVzfdgGJgRrxS7oPZAzaBZnndEA',
    user_agent="smol man"
    
)

#post object
class post:
    def __init__(self, url, rating, title, wtc, id):
        self.url = url
        self.rating = rating
        self.title = title
        self.wtc = wtc
        self.post_id = id 
    def __str__(self):
        return f'Post name is {self.title} with rating {self.rating} Link: {self.url} id: {self.post_id}\n'
    

def sortRating(s):
    return s.rating

def getRating(comments):   
    rating = 0
    comments.replace_more(limit=None) #replace all unloaded comment obj with loaded comments
    for comment in comments:
        rating += sentiment_scores(comment.body)
    return rating
start_time = time.time() # to test what time is taking the longest

post_list = []

prompt = input('what do you want to search: \n')
#grabs posts based on prompt
posts = r.subreddit("FashionReps").search(query=prompt,
                                                   sort="relevance", 
                                                   limit=5, 
                                                   time_filter= "year")
end_time_for_api = time.time()

for s in posts:
    post_list.append(post("https://www.reddit.com"+ s.permalink, 
                          getRating(s.comments), 
                          s.title, 
                          s.url, s.id))
end_time_for_eval = time.time()
post_list.sort(key=sortRating)#sort the post obj in order of rating
for i in post_list:
    print(i)
print(f"time for reddit api was {end_time_for_api-start_time} and the time for eval was {end_time_for_eval-start_time}")



