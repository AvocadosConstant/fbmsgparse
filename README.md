# FB Messages Parser

A simple python module to clean, organize, preprocess, and make sense of your entire Facebook message history.

This module was originally written to help create a Markov chatbot to emulate our friend [Chris](https://github.com/chrisbeard) after he was kicked from a chat group for excessive crassness.
The messages.htm file retreived from the downloadable archive off of Facebook was too unwieldy to work with, and I couldn't find any specific libraries that minimalistically processed the corpus the way I wanted to, so this module was written.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

 - Install [python3](https://www.python.org/downloads/): Self explanatory.

 - Install [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup): Required for HTML parsing.

 - Install the [lxml parser](http://lxml.de/installation.html): lxml is way faster than html.parser or html5lib.

 - Download an archive of your all your Facebook data.
    1. Log into Facebook.
    2. Navigate to [settings](https://www.facebook.com/settings).
    3. At the bottom of General Account Settings find the line of text that says "Download a copy of your Facebook data" and click the link.
    4. Follow the instructions on the next page.
    5. After your archive is compiled, you will receive an email with your download link.
    6. Extract your data dump. Your messages.htm file is located in ./html/messages.htm

### Example

See [examples](./examples/) for more.

Import fbmsgparse
```python
from fbmsgparse import FbMsgParse
```
Create a FbMsgParse object with the path to your messages.htm document.
```python
messages_path ='html/messages.htm'
fmp = FbMsgParse(messages_path)
```
Print out some stats
```python
print(fmp.stats())
```
Use get_user_messages() to extract a list of all of a specified user's messages from threads with a minimum of 3 members.
```python
u_id = '1234567890'
u_name = 'Name Surname'
msgs = fmp.get_user_messages(u_id, u_name, min_size=3)
```


## Built With

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Scraping galore
