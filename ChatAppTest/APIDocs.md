### `GET /api/channels`
Gets a list of channels the given user attached to the token can view.  
Parameters
```
{
    token: "AUTHENTICATION TOKEN"
}
```
Response
```
{
    "channels": [
        {
            "flags": int // The flags of the channel
            "id": int // The id of the channel
            "name: str // The name of the channel
        }...
    ]
}
```
### `GET /api/channels/<channel>/messages`
Gets a list of messages in the specified channel.  
Parameters
```
{
    token: "AUTHENTICATION TOKEN"
    messages: how many messages you want the api to return
    after: after what timestamp(snowflake) should the api return messages from
}
```
Response
```
{
    "channelid": int // The id of the channel
    "lastmessageid": int // The id of the last message in the list
    "messages": [
        {
            "author": {
                "avatarurl": str // The url to the avatar
                "id": int // The id of the user
                "name": str // The name of the user
            },
            "id": int // The id of the message 
            "messages": {
                "content": str // The message content
                "id": int // The same id of the message
            }...
        }
    ]
}
```
### `GET /api/channels/<channel>/users`
Gets a list of members in the channel.  
Parameters
```
{
    token: "AUTHENTICATION TOKEN"
}
```
Response
```
{
    {
        "avatarurl": str // The url to the avatar
        "id": int // The id of the user
        "name": str // The name of the user
    }...
}
```