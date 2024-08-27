import praw
import pytz
import pandas as pd
from datetime import datetime


"""
脚本介绍：
这个脚本的目的是从 Reddit 的指定 subreddit 中收集前 100 个热门帖子的数据，并将这些数据写入到一个 CSV 文件中。
收集的数据包括帖子的标题、得分、帖子ID、URL、正文内容和评论数量。
数据被存储在一个名为 `hot_posts.csv` 的文件中，并且不包含索引列。
"""

# 创建 Reddit 实例
reddit = praw.Reddit(
    client_id='rE_BWSQJPWyu5W7tP1keYw',
    client_secret='Cd9uxRBwh5LnNsfxWdyGGIJJAX9Z9g',
    user_agent='windows:aPigeon:1.0 (by /u/AP1g3on)'
)

# 选择一个 subreddit
subreddit = reddit.subreddit('EufyCam')

# 设置起始时间和结束时间
start_time = datetime(2023, 9, 1)
end_time = datetime(2023, 9, 5)

# 将起始时间和结束时间转换为 Unix 时间戳格式
start_timestamp = int(start_time.timestamp())
end_timestamp = int(end_time.timestamp())

# 将起始时间转换为 Reddit API 所需的时间戳格式
start_timestamp = int(start_time.timestamp())

# 写入到dataframe中
df = pd.DataFrame(columns=['Title', 'Score', 'POST_ID', 'URL', 'Text', 'Comments', 'Timestamp'])

# 用于存储所有帖子的列表
all_posts = []

# 获取前 100 个热门帖子
for submission in subreddit.new(limit=None):

    """
    for 循环用于遍历 subreddit 中指定时间段内的所有帖子
    将每个帖子的相关信息存储在一个名为 dict 的字典中
    将这个字典添加到名为 all_posts 的列表中
    打印每个帖子的标题、得分、帖子ID、URL、正文内容和评论数量
    """
    post_dict = {
        'Title': submission.title,
        'Score': submission.score,
        'POST_ID': submission.id,
        'URL': submission.url,
        'Text': submission.selftext,
        'Comments': submission.num_comments,
        'Timestamp': datetime.fromtimestamp(submission.created_utc, tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    }
    all_posts.append(post_dict)

# 将列表转换为 DataFrame
df = pd.DataFrame(all_posts)

# 将 Text 列中的换行符替换为空格
df['Text'] = df['Text'].apply(lambda x: str(x).replace('\n', ' '))

# 将数据保存到 CSV 文件中
df.to_csv('hot_posts.csv', index=False)
