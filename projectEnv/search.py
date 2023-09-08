import re
import praw
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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

def regbot(comment_body): 
    score = 0
    good_patt = re.compile(r'gl|good|\.*\sW\.*\s+|fire', re.IGNORECASE)
    bad_patt = re.compile(r'rl|\sbad|\soff|return', re.IGNORECASE)
    good = good_patt.findall(comment_body)
    bad = bad_patt.findall(comment_body)
    good_score = len(good)
    bad_score = len(bad)
    score = good_score + bad_score
    score = good_score - bad_score
    return(score)

def linreg(submission):
    # creates  score for a post based on the linear relation 
    # between the comments and the average number of upvotes for a QC post
    sd = 28.6
    m = 2.59
    int = 5.85
    c = m * submission.score + int
    return(c/sd)




    

