import fbmsgparse as fb

messages_path ='html/message_test_raw.html' 
parsed = fb.FbMsgParse(messages_path)

u_name = 'Chris Beard'
u_id = '1487474269@facebook.com'
print(parsed.unique_user_messages(u_id, u_name))
