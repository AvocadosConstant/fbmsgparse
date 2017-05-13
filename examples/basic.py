from fbmsgparse import FbMsgParse

# Create a FbMsgParse object
messages_path ='html/messages.htm'
fmp = FbMsgParse(messages_path)

# Print out some stats
print(fmp.stats())

# Extract all messages sent by a certain user 
# from threads with a minimum of 3 members
u_id = '1234567890'
u_name = 'Name Surname'
msgs = fmp.get_user_messages(u_id, u_name, min_size=3)
