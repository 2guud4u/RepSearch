# attempting to explore the relationship between the average special char score and the number of upvotes
from search import sexbot
from searchCode import *
import praw


r = praw.Reddit(
    client_id='jknOULmDh_Xkmi5xLSpl_A',
    client_secret='5jOGVzfdgGJgRrxS7oPZAzaBZnndEA',
    user_agent="smol man",
)

plist = []
listyy = []
prompt = "QC"

for i in r.subreddit("FashionReps").search(query=prompt,
                                           sort="relevance", 
                                            limit=100, 
                                            time_filter= "year"):
    plist.append((i.score, i.num_comments))
    listyy.append(getRating(i.comments))


print(len(plist))
average_upvotes = sum(upvotes for upvotes, _ in plist) / len(plist)
average_comments = sum(comments for _, comments in plist) / len(plist)
average_score = sum(listyy) / len(listyy)

print(f"average score is {average_score}")
print(f"Average number of upvotes for posts with '{len(plist)}' posts: {average_upvotes}")
print(f"Average number of comments for posts with '{len(plist)}' posts: {average_comments}")




