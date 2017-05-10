import fbmsgparse as fb

messages_path ='messages.html'
parsed = fb.FbMsgParse(messages_path)

u_name = 'Chris Beard'
u_id = '1487474269'
print(parsed.unique_user_messages(u_id, u_name))
