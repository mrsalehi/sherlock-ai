# long standing process that reads messages and writes 
# them to knowledge base.

def onNewMessage(msg):
  msg = transfrom(msg)
  save_data(msg)

def start_pipeline:
  readMessages()