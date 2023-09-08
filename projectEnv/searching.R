library(car)
library(RedditExtractoR)
library(tidyverse)


sexbot <- function(comment_body) {
  good_patt <- "gl|good|\\.*\\sW\\.*\\s+|fire"
  bad_patt <- "rl|\\sbad|\\soff|return"
    
  good <- str_count(comment_body, regex(good_patt, ignore_case = TRUE))
  bad <- str_count(comment_body, regex(bad_patt, ignore_case = TRUE))
  
  score <- good - bad
  return(score)
}

prompt <- "QC"
subreddit <- "FashionReps"
time_filter <- "year"  # For RedditExtractoR, this will be either "all" or "day"

# Fetch posts
posts <- find_thread_urls(subreddit, keywords = prompt, sort_by = "relevance", period = time_filter)
post_content <- get_thread_content(posts$url)
threads <- post_content$threads
comments <- post_content$comments

# Compute averages
average_upvotes <- mean(threads$score)
average_comments <- mean(posts$num_comments)

# linear reg
comxup <- lm(threads$upvotes ~ threads$comments)
summary(comxup)




# Print results
print(paste("Average number of upvotes for posts: ", average_upvotes))
print(paste("Average number of comments for posts: ", average_comments))
