import fbmsgparse as fb

# Create a FbMsgParse object
messages_path ='messages.html'
fmp = fb.FbMsgParse(messages_path)

# Print out some stats
print(fmp.stats())

# Extract all messages sent by a certain user
u_name = 'Chris Beard'
u_id = '1487474269'
msgs = fmp.unique_user_messages(u_id, u_name, allow_personals=False)
