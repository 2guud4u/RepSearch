import praw
import random
from praw.models import MoreComments
r = praw.Reddit(
    client_id='jknOULmDh_Xkmi5xLSpl_A',
    client_secret='5jOGVzfdgGJgRrxS7oPZAzaBZnndEA',
    password='Happyguy20031024',
    user_agent="smol man",
    username='fake_t4xi'
)
class post:
    def __init__(self, url, rating, title, wtc):
        self.url = url
        self.rating = rating
        self.title = title
        self.wtc = wtc
    def __str__(self):
        return f'Post name is {self.title} with rating {self.rating}\n'
    
def sortRating(s):
    return s.rating

def getRating(comments):   
    return random.randint(0,10)
post_list = []

prompt = input('what do you want to search: \n')

for s in r.subreddit("FashionReps").search(query="prompt",
                                                   sort="relevance", 
                                                   limit=10, 
                                                   time_filter= "year"):
    post_list.append(post(s.permalink, getRating(s.comments), s.title, s.url))

post_list.sort(key=sortRating)

for s in post_list:
    print(str(s))


