import praw
import pandas as pd

post_id = '1f13b5f'
client_id='rE_BWSQJPWyu5W7tP1keYw'
client_secret='Cd9uxRBwh5LnNsfxWdyGGIJJAX9Z9g'
user_agent='windows:aPigeon:1.0 (by /u/AP1g3on)'

# 创建 Reddit 实例
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# 使用帖子的 ID 获取特定帖子
submission = reddit.submission(id=post_id)

# 获取评论
submission.comments.replace_more(limit=0)  # 移除 "MoreComments" 对象

# 创建一个空的 DataFrame
df = pd.DataFrame(columns=['Comment_ID', 'Parent_ID', 'Author', 'Body', 'Score', 'Created_UTC'])

# 递归函数来处理评论和子评论
def process_comment(comment, parent_id=None):
    global df
    dict = {
        'Comment_ID': comment.id,
        'Parent_ID': parent_id,
        'Author': comment.author.name if comment.author else 'Deleted',
        'Body': comment.body,
        'Score': comment.score,
        'Created_UTC': comment.created_utc
    }
    df = pd.concat([df, pd.DataFrame([dict])], ignore_index=True)
    
    # 处理子评论
    for reply in comment.replies:
        process_comment(reply, parent_id=comment.id)

# 遍历顶级评论
for top_level_comment in submission.comments:
    process_comment(top_level_comment)
df['Body'] = df['Body'].apply(lambda x: str(x).replace('\n', ' '))

df.to_csv('subcomments.csv', index=False)