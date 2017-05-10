import re
from bs4 import BeautifulSoup

with open("message_test_raw.html") as fp:
    soup = BeautifulSoup(fp)

threads = soup.find_all('div', class_='thread')

threads_messages = []
for thread in threads:
    ids = thread.find(text=re.compile("@facebook.com")).strip()
    # print(ids)
    
    senders = [sender.text.strip() for sender in thread.find_all('span', class_='user')]
    dates = [date.text.strip() for date in thread.find_all('span', class_='meta')]
    texts = [text.text.strip() for text in thread.find_all('p')]

    threads_messages.append(zip(senders, dates, texts))

for thread_messages in threads_messages:
    for messages in thread_messages:
        print(messages) 
