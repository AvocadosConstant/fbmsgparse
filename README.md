# FB Messages Parser

Clean up, organize, and make sense of your Facebook message data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

[Install BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

Download an archive of your all your Facebook data.

1. Log into Facebook.
2. Navigate to [settings](https://www.facebook.com/settings).
3. At the bottom of General Account Settings find the line of text that says "Download a copy of your Facebook data" and click the link.
4. Follow the instructions on the next page.
5. After your archive is compiled, you will receive an email with your download link.
6. Extract your data dump. Your messages.htm file is located in ./html/messages.htm

### Example

How to extract all the messages sent by a given user.

Import fbmsgparse
```python
import fbmsgparse as fb
```

Create a FbMsgParse object with the path to your messages.htm document.
```python
messages_path ='html/messages.htm' 
parsed = fb.FbMsgParse(messages_path)
```
Use unique_user_messages() to extract a list of all of that user's messages.
```python
u_name = 'Chris Beard'
u_id = '1487474269'
print(parsed.unique_user_messages(u_id, u_name))
```


## Built With

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Scraping galore
