def application(environ, start_response):
    body = "Hello world!"
    response_headers = [
        ("Content-type", "text/html"),
        ("Content-length", str(len(body))),
    ]

    start_response("200 OK", response_headers)
    return [body, ]
