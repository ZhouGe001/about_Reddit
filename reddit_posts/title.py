import praw
import pytz
import pandas as pd
from datetime import datetime, timedelta

"""
脚本介绍：这个脚本的目的是从指定的 Reddit 子版块中获取前 100 个热门帖子的标题，
并将这些标题保存到一个名为 "hot_titles.csv" 的文件中。

"""

# 创建 Reddit 实例
reddit = praw.Reddit(
    client_id='rE_BWSQJPWyu5W7tP1keYw',
    client_secret='Cd9uxRBwh5LnNsfxWdyGGIJJAX9Z9g',
    user_agent='windows:aPigeon:1.0 (by /u/AP1g3on)'
)

# 示例：获取前 10 个热门帖子
subreddit = reddit.subreddit('EufyCam')

# time_start = '2018-05-01'
# time_end = '2024-08-26'
# date_format = "%Y-%m-%d"

# 设置起始时间和结束时间
# start_time = datetime.strptime(time_start, date_format)  
# end_time = datetime.strptime(time_end, date_format)

# # 打开一个名为 "hot_titles.csv" 的文件，以写入模式 ('w') 打开，并指定编码为 UTF-8。
# # 然后，遍历 "EufyCam" 子版块中的前 100 个热门帖子，并将每个帖子的标题写入文件中，每行一个标题。

df = pd.DataFrame(columns=['Title', 'Post_ID'])
all=[]

for submission in subreddit.new(limit=None):
    post_dict = {
        'Title': submission.title,
        'POST_ID': submission.id,
        'Timestamp': datetime.fromtimestamp(submission.created_utc, tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    }
    all.append(post_dict)
    # print(datetime.fromtimestamp(submission.created_utc))
    # if start_time <= datetime.fromtimestamp(submission.created_utc) <= end_time:

df = pd.DataFrame(all)
df.to_csv('posts.csv', index=False)
