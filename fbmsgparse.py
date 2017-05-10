from collections import namedtuple
from datetime import datetime
import re

from bs4 import BeautifulSoup


DATE_FORMAT = '%A, %B %d, %Y at %I:%M%p %Z'

Message = namedtuple('Message', 'sender date text')
Thread = namedtuple('Thread', 'uids messages')


class FbMsgParse:
    def __init__(self, path):
        with open(path) as fileobj:
            soup = BeautifulSoup(fileobj, 'html.parser')

        # Extract all threads
        thread_divs = soup.find_all('div', class_='thread')

        self.threads = []

        for div in thread_divs:
            ids = div.find(text=re.compile("@facebook.com")).split(',')
            senders = [sender.text.strip()
                       for sender in div.find_all('span', class_='user')]
            dates = [datetime.strptime(date.text.strip(), DATE_FORMAT)
                     for date in div.find_all('span', class_='meta')]
            texts = [text.text.strip() for text in div.find_all('p')]

            messages = [Message(*msg) for msg in zip(senders, dates, texts)]
            self.threads.append(Thread(ids, messages))

    def unique_user_messages(self, u_id, u_name, allow_personals=True):
        """
        Gets all unique messages sent by a user.

        Parameters
        ----------
        u_id : str
            A Facebook user id.

        u_name : str
            A user's displayed name on Facebook.

        allow_personals : bool
            Whether or not direct messages should be included.
        """
        texts = []
        for thread in self.threads:
            # Don't add personal chat
            if allow_personals or len(thread.uids) > 2:
                for msg in thread.messages:
                    if msg.sender == u_name or msg.sender == u_id:
                        texts.append(msg.text)
        return texts
