from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.downloader.download('vader_lexicon')

# from wordcloud import WordCloud

def fetch_stats(user_selected, df):
    if user_selected != 'overall':
        df = df[df['user'] == user_selected]

    # 1. fetching number of overall messages in the group
    num_messages = df.shape[0]

    # 2. fetching the number of words
    words = []
    for message in df['message']:
        words.extend((message.split()))
        num_words = len(words)

    # number of media files shared
    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    # number of links shared
    extract = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    num_links = len(links)

    return num_messages, num_words, num_media_messages, num_links


def most_busy_user(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, new_df


#   MOST COMMON WORDS

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common())
    emoji_df.rename(columns={'0': "EMOJI", "1": "COUNT"}, inplace=True)
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    df = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()

    time = []

    for i in range(df.shape[0]):
        time.append(df['month'][i] + "-" + str(df['year'][i]))

    df['time'] = time

    return df


def daily_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    df = df.groupby('only_date').count()['message'].reset_index()

    return df


def week_actvity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_actvity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)


def get_vibe(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    pos=0
    neg=0

    for i in range(df.shape[0]):
        text = df['message'][i]
        score = SentimentIntensityAnalyzer().polarity_scores(text)
        pos += score['pos']
        neg += score['neg']

    pos = pos / df.shape[0]
    neg = neg / df.shape[0]

    if pos>neg:
        return "pos"
    elif neg>pos:
        return "neg"
    else:
        return "nu"
