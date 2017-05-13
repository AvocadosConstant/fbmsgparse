from collections import namedtuple
from datetime import datetime
import re
import pickle
import sys

from bs4 import BeautifulSoup, SoupStrainer


DATE_FORMAT = '%A, %B %d, %Y at %I:%M%p %Z'
"""
The date format used in messages.
"""

Message = namedtuple('Message', 'sender date text')
Thread = namedtuple('Thread', 'uids messages')


class FbMsgParse:
    """
    Represents the Facebook message archive as a whole.

    Parameters
    ----------
    path : str
        The location of the message archive html-document
        or the location of the serialized save file.

    load : bool, optional
        True if loading from a serialized save file

    Attributes
    ----------
    threads : list of Thread
        All the direct messages or group chats in the archive.
    """
    def __init__(self, path, load=False):
        if load:
            print('Creating FbMsgParse object from save file', path)
            self.load(path)
        else:
            print('Creating FbMsgParse object from source html', path)
            only_threads = SoupStrainer('div', class_='thread')

            with open(path) as fileobj:
                soup = BeautifulSoup(fileobj, 'lxml', parse_only=only_threads)

            # Extract all threads
            thread_divs = soup.find_all('div', class_='thread')

            self.threads = []

            for div in thread_divs:
                ids = [uid.replace('@facebook.com', '')
                        for uid
                        in div.find(text=re.compile('@facebook.com')).split(',')]
                senders = [sender.text.strip()
                           for sender in div.find_all('span', class_='user')]
                dates = [datetime.strptime(date.text.strip(), DATE_FORMAT)
                         for date in div.find_all('span', class_='meta')]
                texts = [text.text.strip() for text in div.find_all('p')]

                messages = [Message(*msg) for msg in zip(senders, dates, texts)]
                self.threads.append(Thread(ids, messages))

    def save(self, path):
        """
        Serializes self.threads into the given path.

        Parameters
        ----------
        path : str
            Path to savefile.
        """
        pickle.dump(self.threads, open(path, 'wb'))

    def load(self, path):
        """
        Loads self.threads from serialized savefile.

        Parameters
        ----------
        path : str
            Path to savefile.
        """
        try:
            with open(path, 'rb') as f:
                self.threads = pickle.load(f)
        except FileNotFoundError as e:
            print(e)
            print('FileNotFoundError: Path', path, ' does not exist!')
            sys.exit(1)
        except pickle.UnpicklingError as e:
            print('Error: Cannot load from file', path, '!')
            sys.exit(1)

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

        Returns
        -------
        texts : list of str
            All the message bodies sent by a user.
        """
        texts = []
        for thread in self.threads:
            # Don't add personal chat
            if allow_personals or len(thread.uids) > 2:
                for msg in thread.messages:
                    if msg.sender == u_name or msg.sender == u_id:
                        texts.append(msg.text)
        return texts

    def stats(self):
        return 'There are %d parsed conversations.\n' % len(self.threads)
