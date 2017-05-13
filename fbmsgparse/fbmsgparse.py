from collections import namedtuple
from datetime import datetime
import re
import pickle
import sys
import os.path

from bs4 import BeautifulSoup, SoupStrainer


DATE_FORMAT = '%A, %B %d, %Y at %I:%M%p %Z'
"""
The date format used in messages.
"""

Message = namedtuple('Message', 'sender date text')
Thread = namedtuple('Thread', 'uids messages')


class FbMsgParse:
    """ Represents the Facebook message archive as a whole.

    At least one of the params is required to construct a FbMsgParse object.
    If only source_path is defined, the object will be parsed anew.
    If only save_path is defined, the object will be loaded from a save file.
    If both are provided, the object will try to load from a save file.
        If the save file is not valid, it will be parsed anew from source_path.
        It will also save the newly parsed object to save_path.

    Parameters
    ----------
    source_path : str, optional
        The path to the Facebook message archive htm-document.

    save_path : str, optional
        The location to the serialized save file.

    Attributes
    ----------
    _threads : list of Thread
        All the direct messages or group chats in the archive.
    """
    def __init__(self, source_path=None, save_path=None):
        # Only `source_path` is defined
        if not source_path and save_path:
            self.load(save_path)

        # Only `save_path` is defined
        elif source_path and not save_path:
            self.parse(source_path)

        # Both params are defined
        elif source_path and save_path:
            if os.path.isfile(save_path):
                self.load(save_path)
            else:
                self.parse(source_path)
                self.save(save_path)

        # Neither param is defined
        else:
            self._threads = []

    def parse(self, path):
        """ Parses a source Facebook message archive .htm file into self._threads

        Parameters
        ----------
        path : str
            The path to the Facebook message archive htm-document.
        """
        only_threads = SoupStrainer('div', class_='thread')

        with open(path) as fileobj:
            soup = BeautifulSoup(fileobj, 'lxml', parse_only=only_threads)

        # Extract all threads
        thread_divs = soup.find_all('div', class_='thread')

        self._threads = []

        for div in thread_divs:
            ids = [uid.replace('@facebook.com', '').strip()
                    for uid
                    in div.find(text=re.compile('@facebook.com')).split(',')]

            senders = [sender.text.replace('@facebook.com', '').strip()
                       for sender in div.find_all('span', class_='user')]
            dates = [datetime.strptime(date.text.strip(), DATE_FORMAT)
                     for date in div.find_all('span', class_='meta')]
            texts = [text.text.strip() for text in div.find_all('p')]

            messages = [Message(*msg) for msg in zip(senders, dates, texts)]
            self._threads.append(Thread(ids, messages))

    def save(self, path):
        """ Serializes self._threads into the given path.

        Parameters
        ----------
        path : str
            Path to savefile.
        """
        pickle.dump(self._threads, open(path, 'wb'))

    def load(self, path):
        """ Loads self._threads from serialized save file.

        Parameters
        ----------
        path : str
            Path to savefile.
        """
        try:
            with open(path, 'rb') as f:
                self._threads = pickle.load(f)
        except FileNotFoundError as e:
            print(e)
            print('FileNotFoundError: Path', path, ' does not exist!')
            sys.exit(1)
        except pickle.UnpicklingError as e:
            print('Error: Cannot load from file', path, '!')
            sys.exit(1)

    def threads_with_user(self, u_id, u_name):
        """ Returns a FbMsgParse object containing the threads a given user is in

        Parameters
        ----------
        u_id : str
            A Facebook user id.

        u_name : str
            A user's displayed name on Facebook.

        Returns
        -------
        retFMP : FbMsgParse
            Contains all threads with specified user
        """
        retFMP = FbMsgParse()
        for thread in self._threads:
            for msg in thread.messages:
                if msg.sender == u_name or msg.sender == u_id:
                    retFMP._threads.append(thread)
                    break
        return retFMP

    def get_user_messages(self, u_id, u_name, min_size=0, max_size=None):
        """ Retrieves all unique messages sent by a specified user.

        Parameters
        ----------
        u_id : str
            A Facebook user id.

        u_name : str
            A user's displayed name on Facebook.

        min_size : int, optional
            Minimum group size inclusive

        max_size : int, optional
            Maximum group size inclusive

        Returns
        -------
        texts : list of str
            All the message bodies sent by a user.
        """
        texts = []
        for thread in self._threads:
            num_users = len(thread.uids)
            if num_users >= min_size and (max_size is None or num_users <= max_size):
                for msg in thread.messages:
                    if (msg.sender == u_name or msg.sender == u_id) and msg.text:
                        texts.append(msg.text)
        return texts

    def stats(self):
        return 'There are %d parsed conversations.\n' % len(self._threads)
