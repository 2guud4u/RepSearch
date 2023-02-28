import re
def sexbot(comment_body): 
    score = 0
    good_patt = re.compile(r'(gl)|(good)|(W\.*\s+)|(fire)', re.IGNORECASE)
    bad_patt = re.compile(r'(rl)|(bad)|(off)|(return)', re.IGNORECASE)
    good = re.findall(comment_body, good_patt)
    bad = re.findall(comment_body, bad_patt)
    good_score = len(good)
    bad_score = len(bad)
    score = good_score + bad_score
    return(score)
