import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    # fetching the unique users for the analysis
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'overall')
    user_selected = st.sidebar.selectbox("show analysis wrt particular user", user_list)
    if st.sidebar.button('show analysis'):
        st.title("TOP STATISTICS")
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(user_selected, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("total messages")
            st.title(num_messages)

        with col2:
            st.header("words")
            st.title(num_words)

        with col3:
            st.header("Media messages")
            st.title(num_media_messages)

        with col4:
            st.header("links shared")
            st.title(num_links)
    # monthly timeline of the w.r.t user
    st.title("MONTHLY TIMELINE")
    timeline = helper.monthly_timeline(user_selected, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # daily timeline
    st.title("DAILY TIMELINE")
    timeline = helper.daily_timeline(user_selected, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['only_date'], timeline['message'], color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # activity map
    st.title('ACTIVITY MAP')
    col1, col2 = st.columns(2)
    with col1:
        st.header("MOST BUSY DAY")
        busy_day = helper.week_actvity_map(user_selected, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("MOST BUSY MONTH")
        busy_month = helper.month_actvity_map(user_selected, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title('USER HEATMAP')
    user_heatmap = helper.activity_heatmap(user_selected, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    # finding the busiest user in the group (alawys preformed in the group level)
    if user_selected == 'overall':
        st.title("most busiest users")
        x, new_df = helper.most_busy_user(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

# vibe analysis of wrt to userselected


    # most common words
    most_common_df = helper.most_common_words(user_selected, df)
    fig, ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title("Most Common words")
    st.pyplot(fig)

    # EMOJI ANALYSIS
    emoji_df = helper.emoji_helper(user_selected, df)
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)
