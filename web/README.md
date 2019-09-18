

## Chapter 2 'Flask Web Development'

### Dynamic routes

Example:
```
@app.route('/user/<name>')
    def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)
```


### The request object

Example:
```
from flask import request
    @app.route('/')
    def index():
        user_agent = request.headers.get('User-Agent')
        return '<p>Your browser is {}</p>'.format(user_agent)
```

|Attribute or method | Description |
|---|---|
|cookies| A dictionary with all the cookies included in the request. |
|headers| A dictionary with all the HTTP headers included in the request. |
|get_json()| Returns a Python dictionary with the parsed JSON included in the body of the request. |
