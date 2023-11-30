csrf_token_extra = {
    "responses": {
        200: {
            "headers": {
                "Set-Cookie": {
                    "type": "string",
                    "description": "csrftoken=<csrf_token>; expires=<time>; "
                                   "HttpOnly; Max-Age=<time>; Path=/; SameSite=Lax"
                }
            }
        }
    }
}

auth_in_extra = {
    "responses": {
        201: {
            "headers": {
                "Set-Cookie": {
                    "type": "string",
                    "description": "`sessionid` and `csrftoken` cookies with expires, HttpOnly, Max-Age, "
                                   "Path and SameSite attributes"
                }
            }
        }
    }
}
