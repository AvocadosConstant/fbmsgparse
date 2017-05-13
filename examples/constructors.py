from fbmsgparse import FbMsgParse

messages_path ='html/messages.htm'
save_file_path ='save.p'

"""
This example highlights the different ways 
you can construct a FbMsgParse object.

The constructor definition for FbMsgParse is
    def__init__(self, source_path=None, save_path=None)

Construction depends on which of the 2 parameters are passed.
"""

# Forces construction by parsing a messages.htm file
fmp = FbMsgParse(messages_path)

# Can also do
# fmp = FbMsgParse(source_path=messages_path)



# Forces construction by parsing a messages.htm file
fmp = FbMsgParse(save_path=save_file_path)



# When both parameters are specified, it will try to load from the save file.
# If the save file is not valid, it will be parsed anew from source_path.
# It will also save the newly parsed object to save_path.
fmp = FbMsgParse(messages_path, save_file_path)

# Can also do
# fmp = FbMsgParse(messages_path, save_path=save_file_path)
