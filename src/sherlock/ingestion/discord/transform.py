def transform(msg):
  return vector.embed({
    sender: msg.sender,
    text: msg.text,
    timestamp: msg.timestamp
  });