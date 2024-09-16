# 0x02. Session authentication

## About
- Simple HTTP API for playing with `User` model.
- Implements `Basic Authentication` scheme and `Session Authentication`

## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model
- `user_session.py`: session models

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/
status`, `/stats`, `/authorized` and `/forbidden`
- `views/session_auth.py`: login and logout endpoints of the API: `/auth_session/login`, `/auth_session/logout`
- `views/users.py`: all users endpoints
- `auth/auth.py`: authentication base module
- `auth/basic_auth.py`: basic authentication module
- `auth/session_auth.py`: session authentication module
- `auth/session_exp_auth.py`: expiring session module
- `auth/session_db_auth.py`: storable session module

## Setup

```
$ pip3 install -r requirements.txt
```


## Run

- Without authentication
```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```
- Basic authentication
```
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
```
- Infinite session authentication
```
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_auth SESSION_NAME='name_of_session_cookie' python3 -m api.v1.app
```
- Expiring session authentication
```
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_exp_auth SESSION_NAME='name_of_session_cookie' SESSION_DURATION=60 python3 -m api.v1.app
```
- Expiring session without session duration constraint
```
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_exp_auth SESSION_NAME='name_of_session_cookie' python3 -m api.v1.app
```
- Persistent session authentication. Persists even if the server is shutdown. 
```
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_exp_auth SESSION_NAME='name_of_session_cookie' SESSION_DURATION=60 python3 -m api.v1.app
```
## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `GET /api/v1/unauthorized`: returns a 401 response
- `GET /api/v1/forbidden`: returns a 403 response
- `POST /api/v1/auth_session`: creates new session when given the writer credentials (Form fields: `email`, `password`)
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `DELETE /api/v1/auth_session`: logs out user and deletes their session when given the right credentials (Form fields: `email`, `password`)

## Simple to use with curl

### Without authentication
```
$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
```
### Basic authentication
```
$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Basic Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh"
[
  {
    "created_at": "2017-09-25 01:55:17", 
    "email": "bob@hbtn.io", 
    "first_name": null, 
    "id": "9375973a-68c7-46aa-b135-29f79e837495", 
    "last_name": null, 
    "updated_at": "2017-09-25 01:55:17"
  }
]
```
### Session Authentication
- #### Login
```
$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=bobsession@hbtn.io" -d "password=fake pwd" -vvv
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> POST /api/v1/auth_session/login HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> Content-Length: 42
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 42 out of 42 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Set-Cookie: _my_session_id=e173cb79-d3fc-4e3a-9e6f-bcd345b24721; Path=/
< Access-Control-Allow-Origin: *
< Content-Length: 210
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Mon, 16 Oct 2017 04:57:08 GMT
< 
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
* Closing connection 0
```
- #### Access endpoint with session cookie
```
$ curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=e173cb79-d3fc-4e3a-9e6f-bcd345b24721"
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
```
- #### Logout
```
$ curl "http://0.0.0.0:5000/api/v1/auth_session/logout" --cookie "_my_session_id=e173cb79-d3fc-4e3a-9e6f-bcd345b24721" -XDELETE
{}
```
