# long standing process that reads messages and writes 
# them to knowledge base.

def syncSource:
  const messages = readMessages();
  const transformedMessages = transform(messages);
  saveMessages(transformedMessages)