import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import matplotlib.pyplot as plt
import numpy as np

class TwitterClient(object): 
    def __init__(self): 
        consumer_key = 'Nt7ynRIbnJHZ4YggIshkoo208'
        consumer_secret = 'TV1oZol5VHKNJprHgKDjoSUUN08KAF7b3PzqlmyPkwRRybCSWd'
        access_token = '706742912629903361-sLCNwv4WRlpJnLwhASItGqTeFMAeE5X'
        access_token_secret = 'G6AheJ02ul8ZXJI1CcVWURQXBXDGGr1YCDlJpnHe3CuQa'
  
        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
  
    def get_tweet_sentiment(self, tweet):  
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        tweets = [] 
  
        try: 
            fetched_tweets = self.api.search(q = query, count = count) 

            for tweet in fetched_tweets:  
                parsed_tweet = {} 

                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            return tweets 
  
        except tweepy.TweepError as e:  
            print("Error : " + str(e)) 
  
def main():  
    api = TwitterClient() 
    query1=input("Enter the input query1:")
    query2=input("Enter the input query2:")
    tweets1 = api.get_tweets(query = query1,count = 200)
    tweets2 = api.get_tweets(query = query2,count = 200)
    xg1=[]
    yg1=[]
    xg2=[]
    yg2=[]
    x1=0
    x2=0
    y1=40
    y2=40
    pos1=0
    neg1=0
    pos2=0
    neg2=0
    for tweet1 in tweets1:
        if tweet1['sentiment']=='positive':
            y1=y1+1
            x1=x1+1
            pos1=pos1+1
            yg1.append(y1)
            xg1.append(x1)
        elif tweet1['sentiment']=='negative':
            y1=y1-1
            x1=x1+1
            neg1=neg1+1
            yg1.append(y1)
            xg1.append(x1)
        else:
            y1=y1
            x1=x1+1
            yg1.append(y1)
            xg1.append(x1)
    for tweet2 in tweets2:
        if tweet2['sentiment']=='positive':
            y2=y2+1
            x2=x2+1
            pos2=pos2+1
            yg2.append(y2)
            xg2.append(x2)
        elif tweet2['sentiment']=='negative':
            y2=y2-1
            x2=x2+1
            neg2=neg2+1
            yg2.append(y2)
            xg2.append(x2)
        else:
            y2=y2
            x2=x2+1
            yg2.append(y2)
            xg2.append(x2)
            
    print("No of Supportive tweets for {0}:".format(query1))
    print(pos1)
    print("No of hatred tweets {0}:".format(query1))
    print(neg1)
    print("No of Supportive tweets for {0}:".format(query2))
    print(pos2)
    print("No of hatred tweets {0}:".format(query2))
    print(neg2)
    plt.plot(xg1,yg1,color='red')
    plt.plot(xg2,yg2)
    plt.legend(["{0}".format(query1),"{0}".format(query2)])
    plt.xlabel('Tweets')
    plt.ylabel('Diff in Sentiments')
    plt.title('Sentiment Analysis')
    if(len(tweets1)>len(tweets2)):
        plt.xticks(np.arange(1,len(tweets1)+1,1))
    else:
        plt.xticks(np.arange(1,len(tweets2)+1,1)) 
    plt.yticks(np.arange(0,100,5))
    plt.show()
            
    df1=pd.DataFrame(tweets1,columns=['text'])
    df2=pd.DataFrame(tweets2,columns=['text'])
    df1.to_csv('tttwet1.csv')
    df2.to_csv('tttwet2.csv')
  
if __name__ == "__main__": 
    main() 
