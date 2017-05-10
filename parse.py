import re
from bs4 import BeautifulSoup
from datetime import datetime

# This is absolutely retarded
# This line works on linux, but not on Windows
# If EDT is changed to DST than it works
# datetime_object = datetime.strptime('Friday, July 29, 2016 at 5:06pm EDT', '%A, %B %d, %Y at %I:%M%p %Z')
# print(datetime_object)

default_path = "html/message_test_raw.html"
with open(default_path) as fp:
    soup = BeautifulSoup(fp)

# Extract all threads
threads = soup.find_all('div', class_='thread')

threads_ids = []
threads_msgs = []

for thread in threads:
    ids = thread.find(text=re.compile("@facebook.com")).split(',')
    ids = [cur_id.strip() for cur_id in ids]
    threads_ids.append(ids)
    
    senders = [sender.text.strip() for sender in thread.find_all('span', class_='user')]
    dates = [date.text.strip() for date in thread.find_all('span', class_='meta')]
    texts = [text.text.strip() for text in thread.find_all('p')]
    threads_msgs.append(zip(senders, dates, texts))

threads = zip(threads_ids, threads_msgs)

for thread in threads:
    print(thread[0])
    for msgs in thread[1]:
        print(msgs)
    print()
