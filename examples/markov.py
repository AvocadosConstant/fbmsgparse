from fbmsgparse import FbMsgParse
import markovify

"""
A basic example using markovify to build a Markov model 
with a corpus of someone's Facebook messages.
"""

# Create a FbMsgParse object
messages_path ='html/messages.htm'
fmp = FbMsgParse(messages_path)

# Extract all messages sent by a certain user 
# from threads with a minimum of 3 members
u_id = '1234567890'
u_name = 'Richie Stallman'
msg_list = fmp.get_user_messages(u_id, u_name)

# Join the list into a newline delimited string
msgs = '\n'.join(msg_list)

# Build the markovify model
model = markovify.NewlineText(msgs)

# Print a randomly generated sentence
print(model.make_sentence())
