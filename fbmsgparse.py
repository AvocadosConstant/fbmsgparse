from bs4 import BeautifulSoup
from datetime import datetime
import re

class FbMsgParse:
    def __init__(self, path):
        with open(path) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        # Extract all threads
        threads = soup.find_all('div', class_='thread')

        threads_ids, threads_msgs = [], []

        for thread in threads:
            ids = thread.find(text=re.compile("@facebook.com")).split(',')
            threads_ids.append([uid.strip() for uid in ids])

            senders = [sender.text.strip() for sender in thread.find_all('span', class_='user')]
            # This doesn't work on Windows because it's dumb
            dates = [datetime.strptime(date.text.strip(), '%A, %B %d, %Y at %I:%M%p %Z')
                     for date in thread.find_all('span', class_='meta')]
            texts = [text.text.strip() for text in thread.find_all('p')]
            threads_msgs.append(zip(senders, dates, texts))
        self.threads = zip(threads_ids, threads_msgs)

    def unique_user_messages(self, u_id, u_name):
        texts = []
        for thread in self.threads:
            # Don't add personal chat
            if len(thread[0]) > 2:
                for msgs in thread[1]:
                    if msgs[0] == u_name or msgs[0] == u_id:
                        texts.append(msgs[2])
        return texts
