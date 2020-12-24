## AUTHENTICATION

### `POST /api/auhorize`

Used to authenticate a user, returns a token if authentication successful.

JSON Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| username | str | The username | Yes | None |
| pwd | str | The password | Yes | None |

## CHANNELS

### `GET /api/channels`

Gets a list of channels the given user attached to the token can view.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT |
| ----- | ---- | -------------------- | -------- | ------- |
| token | str | Authentication token | Yes | None |

JSON Response:

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

### `GET /api/channels/<channel>`

Gets a specific channel

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT |
| ----- | ---- | -------------------- | -------- | ------- |
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "flags": int // The flags of the channel
    "id": int // The id of the channel
    "name: str // The name of the channel
}
```

### `GET /api/channels/<channel>/messages`

Gets a list of messages in the specified channel.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT |
| -------- | ---- | -------------------------------------------------------------- | -------- | ------- |
| token | str | Authentication token | Yes | None |
| messages | int | how many messages you want the api to return | No | 50 |
| after | int | after what timestamp(snowflake) should the api return messages | No | 0 |

JSON Response:

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
                "attachment": int // The id of the attachment (if exists)
            }...
        }
    ]
}
```

### `GET /api/channels/<channel>/users`

Gets a list of members in the channel.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "users" = [{
                    "avatarurl": str // The url to the avatar
                    "id": int // The id of the user
                    "name": str // The name of the user
                }...]
}
```

### `DELETE /api/channels/<channel>`

Leave a channel.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `POST /api/channels/<channel>/messages`

Send a chat message.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Post Data:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| message | string | The message | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `POST /api/channels/<channel>/messages/attachment`

Send a chat message with attachment.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
| file-name | str | The filename of the attachemnt | Yes | None |

Post Data:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| attachment | blob | The attachment | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `GET /chat/messages/<id>`

Gets an attachment linked with the id.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | The attachment data |
| 404 | Attachment not found |
| 403 | Unauthorized |

## USERS

### `GET /api/users/<user>`

Gets the basic details of a user.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "id": int // The id of the user
    "username": str // The username of the user
    "class": str // The class of the user
    "avatar-url": str // The url to the avatar of the user
    "permissions": int // The permissions of the user
}
```

### `PATCH /api/users/<user>`

Modifies the user details.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Post Data:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| username | str | The new username | No | None |
| class | str | The new class | No | None |
| permissions | int | The new permissions | No | None |

Response
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `DELETE /api/users/<user>

Deletes a user.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Response
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `POST /api/users/register`

Register a user.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| username | str | The username of the user | Yes | None |
| password | str | The password of the user | Yes | None |
| permissions | int | The permissions flags of the user | No | 0 |

Response
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `GET /api/users/<user>/DM`

Creates a DM with the specified user.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "id": int // The DM channel id
    "name": str // The DM channel name
    "flags": int // The DM channel flags
}
```

### `GET /api/users/<user>/avatar`

Gets the avatar of the specified user.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
Response:
The avatar binary data

### `POST /api/users/<user>/avatar`

Sets the avatar of the specified user.
Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Post Data:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| data | blob | The avatar | Yes | None |

Response
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `GET /api/users/<user>/details`

Gets miscellaneous details about the user such as details in the diary

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Response
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | The JSON details |
| 403 | Unauthorized |

### `POST /api/users/<user>/details`

Sets additional details of the user.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Post Data:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| data | json | The details | Yes | None |

Response
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

## ANNOUNCEMENTS

### `GET /api/announcements`

Gets a list of announcements for a user attached to the token.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    {
        "id": int // The announcement id
        "creator": int // The id of the user who did the announcement
        "class": str // The class the announcement targets
        "content": str // The content of the announcement
    }...
]
```

### `POST /api/announcements`

Do an announcement.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| class | str | The class the announcement is targeted towards | Yes | None |
| content | str | The content of the announcement | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

## ASSIGNMENTS

### `GET /api/assignments/<class>/`

Gets a list of assignments for a class.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "assignments": [
        {
            "id": int // The assignment id
            "class": str // The class the assignment is targeted at
            "content": str // The description of the assignment
            "due-date": str // The due date of the assignment
            "attachment": str // The filename of the attachment
            "attachment-url": str // The url to the file attached to the announcement
        }...
    ]
}
```

### `POST /api/assignments/<class>`

Create an assignment for a class.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
| content | str | The description of the assignment | Yes | None |
| due-date | str | The due date of the assignment | Yes | None |
| attachment-name | str | The filename of the attachment | No | None |

Post Data:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| data | blob | The optional attachment for the assignment | No | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `GET /api/assignment/<assignment-id>`

Gets an assignment by its id.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "id": int // The assignment id
    "class": str // The class the assignment is targeted at
    "content": str // The description of the assignment
    "due-date": str // The due date of the assignment
    "attachment": str // The filename of the attachment
    "attachment-url": str // The url to the file attached to theannouncement
}
```

### `GET /api/assignment/<assignment-id>/attachment`

Gets the attachment for an assignment

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | the binary data |
| 403 | Unauthorized |

### `POST /api/assignment/<assignment-id>`

Submit an assignment.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
| attachment-name | str | The filename of the attachment | Yes | None |

Post Data:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| data | blob | The assignment data | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `GET /api/assignment/<assignment-id>/submissions/`

Gets a list of submissions for an assignment

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "submissions": [
        {
            "id": int // The submission id
            "assignment-id": int // The id of the assignment that this submission is for
            "user-id": int // The id of the user who submitted this assignment
            "status": int // The status of this assignment
            "attachment": str // The filename of the attachment
            "attachment-url": str // The url to the submitted data of the assignment
        }...
    ]
}
```

### `GET /api/assignment/<assignment-id>/submissions/<submission-id>/file`

Gets the submission file for an assignment.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | the binary data |
| 403 | Unauthorized |

### `PUT /api/assignment/<assignment-id>/submissions/<submission-id>`

Marks the assignment submission to specified status.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
| status | str | The submission status | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

## CLASSES

### `GET /api/classes`

Gets a list of classes.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    "class_name"...
]
```

### `GET /api/class/<class-name>/`

Gets a list of members in the class.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    {
        "id": int // The id of the user
        "username": str // The username of the user
        "class": str // The class of the user
        "avatar-url": str // The url to the avatar of the user
        "permissions": int // The permissions of the user
    }...
]
```

### `GET /api/class/<class-name>/students`

Gets a list of students in the class.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    {
        "id": int // The id of the user
        "username": str // The username of the user
        "class": str // The class of the user
        "avatar-url": str // The url to the avatar of the user
        "permissions": int // The permissions of the user
    }...
]
```

### `GET /api/class/<class-name>/teachers`

Gets a list of teachers in the class.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    {
        "id": int // The id of the user
        "username": str // The username of the user
        "class": str // The class of the user
        "avatar-url": str // The url to the avatar of the user
        "permissions": int // The permissions of the user
    }...
]
```

### `GET /api/staff`

Gets a list of staff members.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    {
        "id": int // The id of the user
        "username": str // The username of the user
        "class": str // The class of the user
        "avatar-url": str // The url to the avatar of the user
        "permissions": int // The permissions of the user
    }...
]
```

## DM REQUESTS

### `GET /api/requests`

Gets a list of incoming DM requests. (Available for SUPERUSER permissions only)

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    {
        "id": int // The DM request id
        "to-user": int // The recipient of the DM request
        "by-user": int // The sender of the DM request
        "content": str // The short description of the DM request
        "expires": str // The date till the DM request or the created DM channel lasts
    }...
]
```

### `POST /api/requests`

Creates a DM request to the specified recipient. (Specified recipient must be SUPERUSER or above)

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Parameters:
Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| target | int | The user to which the request has to be sent | Yes | None |
| content | str | The description of the request | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `GET /api/requests/sent`

Gets a list of sent DM requests.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    {
        "id": int // The DM request id
        "to-user": int // The recipient of the DM request
        "by-user": int // The sender of the DM request
        "content": str // The short description of the DM request
        "expires": str // The date till the DM request or the created DM channel lasts
    }...
]
```

### `GET /api/request/<request-id>/accept`

Accepts a DM request and returns the created DM channel info

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
{
    "flags": int // The flags of the channel
    "id": int // The id of the channel
    "name: str // The name of the channel
}

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | JSON Response |
| 403 | Unauthorized |
```

### `GET /api/request/<request-id>/rejects`

Rejects a DM request

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

## VIDEOS

### `GET /api/videos/<class>/<path>`

Gets a list of videos located at the path.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Response:

```
[
    "videos": [
        {
            "id": int // the video id
            "name": str // the video name
            "class": str // the class
            "link": str // the link to the video
            "path": str // the path to the video
        }...
    ]

    "folders": list<str> // the list of folders accessible from the current path
}
```

### `POST /api/videos/<class>/<path>`

Stores the video details to the specified path.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |

JSON Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| name | str | The name of the video | Yes | None |
| link | str | The link to the video | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `PATCH /api/videos/<class>/<path>`

Modifies the video details

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
| id | int | The id of the video | Yes | none |

JSON Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| name | str | The new name of the video | Yes | None |
| link | str | The new link to the video | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

### `DELETE /api/videos/<class>/<path>`

Deletes a video detail

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| token | str | Authentication token | Yes | None |
| id | int | The id of the video | Yes | none |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |
