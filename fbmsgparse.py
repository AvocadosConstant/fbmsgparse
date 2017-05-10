from bs4 import BeautifulSoup
from datetime import datetime
import re

def build_threads(soup):
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
    return zip(threads_ids, threads_msgs)

def extract_unique_u_messages(threads, u_id, u_name):
    texts = []
    for thread in threads:
        # Don't add personal chat
        if len(thread[0]) > 2:
            for msgs in thread[1]:
                if msgs[0] == u_name or msgs[0] == u_id:
                    texts.append(msgs[2])
    return texts

if __name__ == '__main__':
    # default_path = 'html/message_test_clean.html'
    default_path = 'html/messages.htm'
    with open(default_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    threads = build_threads(soup)

    # Replace with command line args prob
    u_name = 'Chris Beard'
    u_id = '1487474269@facebook.com'

    print(extract_unique_user_messages(threads, u_id, u_name))
