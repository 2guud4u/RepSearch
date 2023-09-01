import praw
from praw.models import MoreComments
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from praw.models.util import stream_generator
from searchCode import *
from search import *


    
def searchItems(prompt):

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
    return total_post_list

postslst = searchItems(prompt='bapesta QC')
for sub in postslst[:6]:
    print(linreg(sub))

print(postslst[3].score)
print(postslst[3].num_comments)

rating = 0
for comment in postslst[3].comments:
        rating += sentiment_scores(comment.body)

print(rating)