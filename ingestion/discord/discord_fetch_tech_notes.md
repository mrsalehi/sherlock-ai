Read new discord messages



# Implementation overview
We will use discord.py to read the messages from discord for a certain channel id. We will get all the messages that take place after timestamp1. Timestamp1 will be stored in a local json file. If timestamp1 doesn't exist then create and save timestamp1 and receive all available messages.

1. Setup the get_messages discord function which takes in channelId as the parameter
2. Setup the discord bot and its on ready event
3. Read the timestamp file (If exists) for the channel id
5. If timestamp file does not exist, create a new one and name it [channelId].json
6. Read the discord message and save it to the array
7. Return the message array as part of the function.

It may also be worthwhile creating this as a class

# Implementation details

## How to get messages after a timestamp
Discord's channel.history has an `after` parameter that takes in a datetime.datetime

```
channel.history(after=after_date, limit=None)
```

## What happens when fetching messages fail?
Ignore this for now. Assume it succeeds for now. Also we'd need to look at how discord.py handles read messages errors. [Channel.history documentation](https://discordpy.readthedocs.io/en/latest/api.html#discord.TextChannel.history)

But some ideas are to retry from the timestamp of the last successfully retrieved message. Or just retry the entire get. 

## Where to store the timestamp
Write the timestamp to a local json file for now. The fetch is for a specific channel id so we can have channel id be the file name. [channelId].json
```
{
    lastFetch: "2019-11-14T00:55:31.820Z" // ISO 8601 standard
}
```

## How to pass the messages for the transformation step
The read_messages function will just return the array of messages received for the transformation step. 