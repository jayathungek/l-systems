from functools import wraps
import error
import os
import signal

import params

def timeout(func, seconds=params.TIMEOUT):
    def decorator(decarg1, decarg2): 
        def _handle_timeout(signum, frame):
            print("timeout triggered")
            raise error.ResponseTimeoutError()

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                print("starting image creation")
                result = func(decarg1, decarg2)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator