# Strata + Hadoop twitters analysis

This repo holds the scripts and files I used to generate a simple analysis of tweets with the hashtag `#StrataHadoop`

It uses the twitter api to get all tweets since the first day of the conference (May 5, 2015). See`scripts/collect-strata-hadoop-tweets.rb`. 

It uses a downloaded ics file of the schedule to then do a simplistic text analysis on the tweets to detect tweets which seem to be about a particular talk and counts the number of tweets. See `spark-strata-tweet-analysis.py`.
