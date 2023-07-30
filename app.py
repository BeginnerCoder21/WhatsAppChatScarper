import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper
import emoji
import seaborn as sns

st.title("WhatsApp Chat Analyzer")
st.divider()
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    st.write("Filename:", uploaded_file.name)
    df=preprocessor.preprocess(data)
    # st.dataframe(df)

    #fetch unique users
    users_lst=df['users'].unique().tolist()
    # users_lst.remove('group_noti')
    users_lst.sort()
    users_lst.insert(0,"Overall")
    # st.write(users_lst)

    selected_user=st.sidebar.selectbox("Show Analysis of",users_lst)
    if selected_user=="Overall":
        st.dataframe(df)
    else:
        st.dataframe(df[df['users']==selected_user])
    if st.sidebar.button('Show Analysis'):
        num_msgs, words, num_media_msgs, num_links, links=helper.fetchStats(selected_user,df)
        col1, col2, col3, col4 =st.columns(4)
        with col1:
            st.subheader("Total messages")
            st.title(num_msgs)
        with col2:
            st.subheader("Total words")
            st.title(words)
        with col3:
            st.subheader("Media Shared")
            st.title(num_media_msgs)
        with col4:
            st.subheader("Links Shared")
            st.title(num_links) 
        
        col1,col2=st.columns(2)
        with col1:
            # Monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            fig.set_figheight(4)
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            # Daily timeline
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            fig.set_figheight(4.7)
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user=="Overall":
            st.title("Most interactive users")
            busy_user, new_busy_user=helper.fetch_interactive_user(df)
            fig,ax= plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(busy_user.index, busy_user.values, color="orange")
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_busy_user)
        
        st.title("Word Cloud")
        df_wc=helper.createWordCloud(selected_user,df)
        fig,ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='blueviolet')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Most common words
        st.title("Most Common Words")
        commom_words_df=helper.most_common_words(selected_user,df)
        commom_words_df=commom_words_df.head(10)
        fig, ax= plt.subplots()
        ax.barh(commom_words_df[0],commom_words_df[1], color="turquoise")
        st.pyplot(fig)
        # st.dataframe(commom_words_df)

        #Emoji analysus
        st.title("Emoji Analysis")
        emoji_df=helper.emoji_extract(selected_user,df)
        if(len(emoji_df)!=0):
            col1, col2=st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax= plt.subplots()
                
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.write("No Emoji is used \U0001F610")
    