import tweepy

# Consumer keys and access tokens, used for OAuth
consumer_key = 'zvrutjFOSpHQDpfhwiiFYu6On'
consumer_secret = 'P2o2Qg1N8BCcCoCyE7nGlHp5mIWuPN3eng3EZv0OPAHP5DzPPg'
access_token = '1644401298-xFwciqSKcUJ0ybgUzZSPfrBBBm30UzeUlR2JXEm'
access_token_secret = 'WPy9CSrnRJF6fpic1yL6mMkbclcJMAvOH0fq5AlIIesw7'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Sample method, used to update a status
api.update_status('Hello World!');

# Creates the user object. The me() method returns the user whose authentication keys were used.
user = api.me()

print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count));