# Importing module for twitter scrape data
import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime

tweets_df = pd.DataFrame()
st.write("# TWITTER DATA SCRAPING")
option = st.selectbox('In what way do you prefer to conduct the data search? You can choose between "Keyword" or "Hashtag" as the search option?',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'Enter Text Here')
start = st.date_input("Select the start date", datetime.date(2023, 2, 9),key='d1')
end = st.date_input("Select the end date", datetime.date(2023, 3, 9),key='d2')
tweet_c = st.slider('how many numbers of tweets you want to scrap', 0, 1000, 5)
tweets_list = []

# Using TwitterSearchScraper for scraping the data of twitter
if word:
    if option=='Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>=tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break            
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(option,' cant be empty')

# Creating Sidebar for details view.
with st.sidebar:   
    st.info('DETAILS')
    if option=='Keyword':
        st.info('Keyword is '+word)
    else:
        st.info('Hashtag is '+word)
    st.info('Starting Date is '+str(start))
    st.info('End Date is '+str(end))
    st.info("Number of Tweets "+str(tweet_c))
    st.info("Total Tweets Scraped "+str(len(tweets_df)))
    x=st.button('Show Tweets',key=1)

# Dowloading in "CSV" (to download the scrape data in the CSV file).
@st.cache # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):    
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = convert_df(tweets_df) # CSV
        c=st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)        
    with col2:    # Dowloading the data in "JSON" file
        json_string = tweets_df.to_json(orient ='records')
        j=st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)

    with col3: # "Show" show data inslef on the website.
        y=st.button('Show Tweets',key=2)

if c:
    st.success("The Scraped Data is Downloaded as .CSV file:")  
if j:
    st.success("The Scraped Data is Downloaded as .JSON file")     
if x: # Display
    st.success("The Scraped Data is:")
    st.write(tweets_df)
if y: # Display
    st.balloons()
    st.success("Tweets Scraped Successfully:")
    st.write(tweets_df)
