from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
words_csv=pd.read_csv("C:/Users/nived/Desktop/Nivi ideapad Lenovo/Nivoo SJ/SJSU sem1/CS185C/Project/sarcasm detector project/wordcloud/wordCloudSarcasm.csv")
words_df=pd.DataFrame(words_csv)
words_df.columns=['Sno','Sarcasm']
print words_df.head()
word_String=""
for index,row in words_df.iterrows():
    word_String=word_String+str(row['Sarcasm'])
print word_String

%matplotlib.inline
#get_ipython().magic(u'matplotlib inline')

wordcloud = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=2000,
                          height=1000
                         ).generate(word_String)


plt.imshow(wordcloud)
plt.axis('off')
plt.show()

