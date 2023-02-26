import praw

r= praw.Reddit(
    client_id='jknOULmDh_Xkmi5xLSpl_A',
    client_secret='5jOGVzfdgGJgRrxS7oPZAzaBZnndEA',
    password='Happyguy20031024',
    user_agent="smol man",
    username='fake_t4xi'
)
for submission in r.subreddit("FashionRep").search(query="AJ1",sort="relevance", limit=100, time_filter= "year"):
    print(submission.title)