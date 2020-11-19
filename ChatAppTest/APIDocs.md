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
    {
        "avatarurl": str // The url to the avatar
        "id": int // The id of the user
        "name": str // The name of the user
    }...
}
```

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

### `POST /api/auhorize`

Used to authenticate a user, returns a token if authentication successful.

Query String Parameters:
| FIELD | TYPE | DESCRIPTION | REQUIRED | DEFAULT|
|-------|------|-------------|----------|--------|
| username | str | The username | Yes | None |
| pwd | str | The password | Yes | None |

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
| class | str | The class the announcement is targeted towards | Yes | None |
| content | str | The content of the announcement | Yes | None |

Response:
| STATUS CODE | RESPONSE |
|-------------|----------|
| 200 | OK |
| 403 | Unauthorized |

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