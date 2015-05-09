textFile = sc.textFile("../strata-hadoop/StrataHadoop-schedule.ics")

common_words = ['the', 'and', 'for', 'with', 'you', 'The', 'And', 'For', 'With', 'You']

def remove_short_words(phrase):
  words = phrase.split()
  phat_phrase = []
  for word in words:
    if (len(word) > 3) and (word not in common_words): phat_phrase += [word]
  return " ".join(phat_phrase)

titles = textFile.filter(lambda line: "SUMMARY" in line).map(lambda line: remove_short_words(line.split(":")[-1]))

def word_map(title):
  l = []
  for word in title.split():
    l.append((word, title))
  return l

v = titles.flatMap(lambda title: word_map(title)).groupByKey()

v = v.map(lambda (word, titles): (word, list(titles)))

# transform this to a normal dictionary
title_words_map = v.collectAsMap()

title_words_list = v.keys().collect()

# Get a collection of all the tweets with #StrataHadoop
tweets_file = sc.textFile('strata-tweets-text.txt').map(lambda line: remove_short_words(line))

def title_words(tweet):
  words = tweet.split()
  l = []
  for word in words:
    if (word in title_words_list):
      l.append((word, tweet))
  return l

# find all the tweets which might be referring to a conference title
all_tweets = tweets_file.flatMap(lambda tweet: title_words(tweet)).groupByKey()
all_tweets = all_tweets.map(lambda (word, tweets): (word, list(tweets)))

# (u'Hadoop', [u'great time at Learn Hadoop', u'Disaster Recovery on Hadoop highly recommend'])

def possible_titles(word, tweets):
  titles = title_words_map[word]
  l = []
  for title in titles:
    for tweet in tweets:
      l.append((title, tweet))
  return l

# (u'Learn Hadoop', u'great time at Learn Hadoop'), (u'Learn Hadoop', u'Disaster Recovery on Hadoop highly recommend')
titles_and_tweets = all_tweets.flatMap(lambda (word, tweets): possible_titles(word, tweets))

def generate_score(title, tweet):
  """ Very dumb scoring algorithm. Calculates how many words the tweet has in common with the title and divides by number of words in the title. """
  words_in_title = title.split()
  num_words_in_title = len(words_in_title)
  words_in_tweet = tweet.split()
  common_count = 0
  counted_words = []
  for word in words_in_tweet:
    if (word in words_in_title) and (word not in counted_words) and (word != 'data'):
      counted_words.append(word)
      common_count += 1
  return (common_count * 1.0) / num_words_in_title

titles_tweets_and_scores = titles_and_tweets.map(lambda (title, tweet): (title, tweet, generate_score(title, tweet)))

# Check out what ranks we have so far
# Might want to do some sort of reduceByKey to count how many of each score there are
rank_by_score = titles_tweets_and_scores.map(lambda (title, tweet, score): (score, (title, tweet))).sortByKey()

filter_tweets_likely_about_title = titles_tweets_and_scores.filter(lambda (title, tweet, score): score > 0.33)

group_by_title = filter_tweets_likely_about_title.map(lambda (title, tweet, score): (title, (tweet, score))).groupByKey()
group_by_title = group_by_title.map(lambda (title, tweets): (title, list(tweets)))

tweet_counts = group_by_title.map(lambda (title, tweets): (len(tweets), title)).sortByKey()
tweet_counts_filtered = tweet_counts.filter(lambda (tweet_count, title): tweet_count > 9)
titles_to_watch = tweet_counts_filtered.collect()

f = open('strata-titles-to-watch.txt', 'a+')

for title in titles_to_watch:
  count = str(title[0])
  title = title[1].encode('utf-8')
  f.write(title + "," + count + "\n")

f.close()

