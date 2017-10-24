import json
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

f = open('clean_raw_posts.txt', 'r')
s = f.read()
f.close()

posts = json.loads(s)
df = pd.DataFrame(posts)

len(posts)
# 13311

len(set(df['thread_id']))
# 1106

len(set(df['user_id']))
# 2035

# get a sense of the thread counts
threads = df.groupby('thread_id')
sizes = threads.size().value_counts()
plt.bar(sizes.index, sizes.values)
plt.show()

threads_by_size = threads.size().sort_values(ascending=False)
plt.bar(range(0, len(threads_by_size)), threads_by_size.values)
plt.show()
## reveals something about my scraping
## type of missingness!!

# get a sense of user activity
users = df.groupby('user_id')
volumes = users.size().value_counts()
plt.bar(volumes.index, volumes.values)
plt.show()

users = users.size().sort_values(ascending=False)
plt.bar(range(0, len(users)), users.values)
plt.show()

# get users per thread
users_per_thread = threads['user_id'].nunique().sort_values(ascending=False)
plt.bar(range(0, len(users_per_thread)), users_per_thread.values)
plt.show()

users_per_thread.value_counts()

# datetime activity
# datetime.strptime(testdate, '%m-%d-%Y, %I:%M %p')
df['datetime'] = pd.to_datetime(df['datetime'])

print(min(df['datetime']))
# 2003-06-06 00:09:00

print(max(df['datetime']))
# 2017-10-08 20:04:00

# over the years
dates = df['datetime']
dates.groupby([dates.dt.month, dates.dt.year]).count().plot(kind="bar")
plt.show()

# hourly per day
dates.groupby([dates.dt.hour, dates.dt.day]).count().plot()
plt.show()
### can also split by day