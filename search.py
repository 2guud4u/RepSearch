import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def keywords(comment_body): 
    score = 0
    good_patt = re.compile(r'gl|good|\.*\sW\.*\s+|fire', re.IGNORECASE)
    bad_patt = re.compile(r'rl|\sbad|\soff|return', re.IGNORECASE)
    good = good_patt.findall(comment_body)
    bad = bad_patt.findall(comment_body)
    good_score = len(good)
    bad_score = len(bad)
    score = good_score + bad_score
    return(score)

def sentiment_scores(comment_body):

    # creates SentimentIntensityAnalyzer object
    sid_obj = SentimentIntensityAnalyzer()
    scores = sid_obj.polarity_scores(comment_body)
    if scores['compound'] >= 0.05:
        return("Positive")
 
    elif scores['compound'] <= - 0.05:
        return("Negative")
 
    else:
        return("Neutral")



c = "man these shoes look bad u can see the stitches RL"

d = sentiment_scores(c)
print(d)
