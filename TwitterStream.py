import tweepy as tp
from tweepy import Stream
from tweepy.streaming import StreamListener
import time

consumer_key = 'zvrutjFOSpHQDpfhwiiFYu6On'
consumer_secret = 'P2o2Qg1N8BCcCoCyE7nGlHp5mIWuPN3eng3EZv0OPAHP5DzPPg'
access_token = '1644401298-xFwciqSKcUJ0ybgUzZSPfrBBBm30UzeUlR2JXEm'
access_token_secret = 'WPy9CSrnRJF6fpic1yL6mMkbclcJMAvOH0fq5AlIIesw7'

class StdOutListener(StreamListener):

    def on_data(self, raw_data):
        #print raw_data;
        try:
            tweettext = raw_data.split(',"text":"')[1].split('","source')[0];
            #print "tweet text is: %s",tweettext;
            if tweettext[0:2] != 'RT':  #RT - Re-tweet
                #print tweettext
                saveFile = open('C:/Users/nived/Desktop/twitDB_sarcasm_2017.csv', 'a')
                saveFile.write(tweettext)
                saveFile.write('\n')
                saveFile.close()
            return True
        except BaseException, e:
            print 'Base Exception'
            time.sleep(5)

    def on_status(self, status):
        print('Tweet text: ' + status.text)
        for hashtag in status.entries['hashtags']:
            print(hashtag['text'])
        return True;

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening


if __name__ == '__main__':
    listener = StdOutListener()
    auth = tp.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=['#sarcasmonly','#sarcasm','#Sarcasm','#sarcastweet'],languages=['en'])