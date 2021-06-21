# The Python micro framework for building web applications.
from flask import request


# The below code always gives the public IP of the client (and not a private IP behind a proxy).
def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        # if behind a proxy
        return request.environ['HTTP_X_FORWARDED_FOR']


# https://stackoverflow.com/questions/9878020/how-do-i-get-the-user-agent-with-flask
def get_user_agent():
    user_agent = request.user_agent
    return {
        'platform': user_agent.platform,
        'browser': user_agent.browser,
        'language': user_agent.language,
        'version': user_agent.version,
    }
