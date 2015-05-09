require 'oauth'
require 'json'

def prepare_access_token(oauth_token, oauth_token_secret)
  consumer = OAuth::Consumer.new("rIWkdoylGpGOI0qOzZDc2TyCk", "nz30g60CziTOtAyd59c4inFaNJll0rHVILumEQ4ITEcjZ34wco", { :site => "https://api.twitter.com", :scheme => :header })
   
  # now create the access token object from passed values
  token_hash = { :oauth_token => oauth_token, :oauth_token_secret => oauth_token_secret }
  access_token = OAuth::AccessToken.from_hash(consumer, token_hash )

  return access_token
end
 
# Exchange our oauth_token and oauth_token secret for the AccessToken instance.
ACCESS_TOKEN = prepare_access_token("345493899-h79ByiQNXCpshxMhBVIfN8LDf4IQA6WuGaJ2gZvC", "8Iw9gq3XQiIZfW724yJUhTAmhxFrBPSZeow3ZyEcLmxLQ")
 
FILE = File.open('strata-tweets.json', 'a+')
FILE.write('[')

def get_tweets(query_string = "?q=%23StrataHadoop&count=100&since=2015-05-05")
  # use the access token as an agent to get the home timeline
  res = ACCESS_TOKEN.request(:get, "https://api.twitter.com/1.1/search/tweets.json#{query_string}")
  puts "GOT RESPONSE #{res}"
  res
end

def add_results(response)
  body = JSON.parse(response.body); nil
  next_results_string = body['search_metadata']['next_results']

  FILE.write(body['statuses'].to_json)

  if next_results_string
    FILE.write(',')
    puts "GETTING RESULTS FOR #{next_results_string}"
    response = get_tweets(next_results_string)
    add_results(response)
  else
    FILE.write(']')
    FILE.close()
    return
  end
end

first_result = get_tweets
add_results(first_result)

f = File.open('strata-tweets-text.txt', 'a+')

res = JSON.parse(f.read).flatten; nil

res.count()
# 6919

tweets = res.map {|tweet| tweet['text']}; nil

for tweet in tweets
  f.write("#{tweet}\n")
end; nil

f.close()
