from functools import wraps
import error
import os
import signal 

def timeout(seconds=1):
    def decorator(func):
        def _handle_timeout(signum, frame):
            print("timeout triggered")
            raise error.ResponseTimeoutError()

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator