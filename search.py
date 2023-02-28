import re
def sexbot(comment_body): 
    score = 0
    good_patt = re.compile(r'gl|good|\.*\sW\.*\s+|fire', re.IGNORECASE)
    bad_patt = re.compile(r'rl|\sbad|\soff|return', re.IGNORECASE)
    good = good_patt.findall(comment_body)
    bad = bad_patt.findall(comment_body)
    good_score = len(good)
    bad_score = len(bad)
    score = good_score + bad_score
    return(score)


