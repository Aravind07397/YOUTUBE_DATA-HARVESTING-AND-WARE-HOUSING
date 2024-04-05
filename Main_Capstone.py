import streamlit as st
import mysql.connector
import pandas as pd

# MySQL Connection
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Bala@9944",
    database="mycapstone"
)

cursor = connection.cursor()

# Function to execute queries and return results as dataframe
def execute_query(query):
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    return df

# Function to display dataframe as table
def display_table(df):
    st.dataframe(df)

# Home page
def home():
    st.title("YouTube Data Analysis App")
    st.subheader("Select an action:")
    action = st.sidebar.selectbox("Choose an action", ["Home", "View Data"])
    return action

# Collect data page 
def collect_data():
    st.title("Collect Data")
    st.write("Enter the channel IDs to collect data:")
    channel_ids = st.text_input("Enter channel IDs (comma-separated)", "")
    if st.button("Collect Data"):
        channel_ids = channel_ids.split(",")
        for channel_id in channel_ids:
            st.write(f"Data collection in progress for Channel ID: {channel_id}")
        st.success("Data collection complete!")

# View data page
def view_data():
    st.title("View Data")
    st.subheader("Select a table to view or answer a question:")
    table = st.selectbox("Choose a table or question", ["Channel", "Playlist", "Comment", "Video", "Answer 10 Questions"])
    if table == "Channel":
        query = "SELECT * FROM channel"
        df = execute_query(query)
        display_table(df)
    elif table == "Playlist":
        query = "SELECT * FROM playlist"
        df = execute_query(query)
        display_table(df)
    elif table == "Comment":
        query = "SELECT * FROM comment"
        df = execute_query(query)
        display_table(df)
    elif table == "Video":
        query = "SELECT * FROM video"
        df = execute_query(query)
        display_table(df)
    elif table == "Answer 10 Questions":
        ten_questions()

def ten_questions():
    st.title("Answer 10 Questions")
    st.subheader("Select a question to answer:")
    question = st.selectbox("Choose a question", [
        "What are the names of all the videos and their corresponding channels?",
        "Which channels have the most number of videos, and how many videos do they have?",
        "What are the top 10 most viewed videos and their respective channels?",
        "How many comments were made on each video, and what are their corresponding video names?",
        "Which videos have the highest number of likes, and what are their corresponding channel names?",
        "What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
        "What is the total number of views for each channel, and what are their corresponding channel names?",
        "What are the names of all the channels that have published videos in the year 2022?",
        "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
        "Which videos have the highest number of comments, and what are their corresponding channel names?"
    ])
    if st.button("Answer"):
        if question == "What are the names of all the videos and their corresponding channels?":
            query = """
            SELECT v.video_name, c.channel_name
            FROM video v
            JOIN channel c ON v.playlist_id = c.channel_id
            """
        elif question == "Which channels have the most number of videos, and how many videos do they have?":
            query = """
            SELECT channel_id, COUNT(*) AS num_videos
            FROM video
            GROUP BY channel_id
            ORDER BY num_videos DESC
            LIMIT 1
            """
        elif question == "What are the top 10 most viewed videos and their respective channels?":
            query = """
            SELECT v.video_name, c.channel_name, v.view_count
            FROM video v
            JOIN channel c ON v.playlist_id = c.channel_id
            ORDER BY v.view_count DESC
            LIMIT 10
            """
        elif question == "How many comments were made on each video, and what are their corresponding video names?":
            query = """
            SELECT v.video_name, COUNT(*) AS num_comments
            FROM video v
            JOIN comment co ON v.video_id = co.video_id
            GROUP BY v.video_name
            """
        elif question == "Which videos have the highest number of likes, and what are their corresponding channel names?":
            query = """
            SELECT v.video_name, c.channel_name, v.like_count
            FROM video v
            JOIN channel c ON v.playlist_id = c.channel_id
            ORDER BY v.like_count DESC
            LIMIT 10
            """
        elif question == "What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
            query = """
            SELECT v.video_name, SUM(v.like_count) AS total_likes, SUM(v.dislike_count) AS total_dislikes
            FROM video v
            GROUP BY v.video_name
            """
        elif question == "What is the total number of views for each channel, and what are their corresponding channel names?":
            query = """
            SELECT c.channel_name, SUM(v.view_count) AS total_views
            FROM video v
            JOIN channel c ON v.playlist_id = c.channel_id
            GROUP BY c.channel_name
            """
        elif question == "What are the names of all the channels that have published videos in the year 2022?":
            query = """
            SELECT DISTINCT c.channel_name
            FROM channel c
            JOIN video v ON c.channel_id = v.playlist_id
            WHERE YEAR(v.published_at) = 2022
            """
        elif question == "What is the average duration of all videos in each channel, and what are their corresponding channel names?":
            query = """
            SELECT c.channel_name, AVG(duration_seconds) AS average_duration
            FROM (
            SELECT v.video_id, v.playlist_id, TIMESTAMPDIFF(SECOND, '00:00:00', v.duration) AS duration_seconds
            FROM video v
            ) AS video_duration
            JOIN channel c ON video_duration.playlist_id = c.channel_id
            GROUP BY c.channel_name
            """
        elif question == "Which videos have the highest number of comments, and what are their corresponding channel names?":
            query = """
            SELECT v.video_name, c.channel_name, COUNT(*) AS num_comments
            FROM video v
            JOIN comment co ON v.video_id = co.video_id
            JOIN channel c ON v.playlist_id = c.channel_id
            GROUP BY v.video_name
            ORDER BY num_comments DESC
            LIMIT 10
            """
        df = execute_query(query)
        display_table(df)


def main():
    action = home()
    if action == "Home":
        collect_data()
    elif action == "View Data":
        view_data()
    else:
        ten_questions()

if __name__ == "__main__":
    main()

# Close cursor and connection
cursor.close()
connection.close()
