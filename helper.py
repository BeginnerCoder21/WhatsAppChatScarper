from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor=URLExtract()

def fetchStats(selectedUser,df):
    if selectedUser!="Overall":
        df=df[df['users']==selectedUser]

    #Total messages
    num_msgs=df.shape[0]

    #Total words
    words=[]
    for msg in df['message']:
        words.extend(msg)

    #Media Messages
    no_of_media_msgs=df[df['message']=="<Media omitted>\n"].shape[0]

    links=[]
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))
    
    return num_msgs, len(words), no_of_media_msgs, len(links), links
    

def fetch_interactive_user(df):
    counts=df['users'].value_counts().head(5)
    df=round((df['users'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index':'names','user': 'percent'})

    return counts, df

def createWordCloud(selectedUser, df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selectedUser!="Overall":
        df=df[df['users']==selectedUser]
    
    temp=df[df['users']!='group_noti']
    temp=temp[temp['message']!="<Media omitted>\n"]

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud( width=500, height=200, min_font_size=10, background_color="white")
    temp['message']=temp['message'].apply(remove_stopwords)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selectedUser,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selectedUser!="Overall":
        df=df[df['users']==selectedUser]
    
    temp=df[df['users']!='group_noti']
    temp=temp[temp['message']!="<Media omitted>\n"]

    wordsC=[]
    for message in temp["message"]:
        for word in message.lower().split():
            word = word.strip('!@#$%^&*()-_=+[]{}|:;"<>,.?/\~`')
            if word not in stop_words:
                wordsC.append(word)
            
    commom_words_df=pd.DataFrame(Counter(wordsC).most_common(20))
    return commom_words_df

def emoji_extract(selectedUser,df):
    if selectedUser!="Overall":
        df=df[df['users']==selectedUser]
    
    emojis=[]
    
    for msg in df['message']:
        emojis.extend([emo for emo in msg if emo in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()
