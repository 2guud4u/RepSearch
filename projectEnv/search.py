import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_scores(comment_body):

    # creates SentimentIntensityAnalyzer object
    sid_obj = SentimentIntensityAnalyzer()
    scores = sid_obj.polarity_scores(comment_body)
    if scores['compound'] >= 0.05: #positive
        return 1
 
    elif scores['compound'] <= - 0.05: #negative
        return -1
 
    else:
        return 0    #neutral




