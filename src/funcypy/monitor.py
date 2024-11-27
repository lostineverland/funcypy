'''It's good to have data about the functions and processes that we run
'''
import functools
import json
import time, datetime
from typing import Callable, Any, Dict
from . times import epoch_to_iso


def json_serializer(obj: object) -> Callable:
    if isinstance(obj, set):
        return str(obj)
    
    if isinstance(obj, datetime):
        return epoch_to_iso(obj.timestamp())
    
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    
    raise TypeError(f"Type {type(obj)} not serializable")

def log(x=None, name='value', logger=print, **kwargs) -> Any:
    '''A logging function which returns the value (as opposed to print which returns `None`)
        but will also print a JSON `{value: x}` of the given value. It also allows for
        kwargs to be included in the JSON.
    '''
    if x: kwargs = {name: x, **kwargs}
    try:
        logger(json.dumps(kwargs, default=json_serializer))
    except TypeError as e:
        logger(json.dumps({ **kwargs, 
                res: str(kwargs.get(res)),
                args: str(kwargs.get(args)),
                kwargs: str(kwargs.get(kwargs)),
                err: str(e.args),
            }))
        print('error: {}\nargs: {}'.format(e, kwargs))
    except Exception as e:
        logger(json.dumps({'args': str(kwargs), 'error': str(e.args)}))
        print({**kwargs, 'logging_error': e})
    return log

def track(func: Callable, erronly: bool=True, logger: Dict={}) -> Callable:
    '''This function wraps any function and logs metrics on the function'''
    @functools.wraps(func)
    def f(*args, **kwargs):
        try:
            t0 = time.time()
            res = func(*args, **kwargs)
            t1 = time.time()
            if not erronly:
                log(func=func.__name__, res=res, args=args, kwargs=kwargs, duration=t1-t0, **logger)
        except Exception as e:
            try:
                log(func=func.__name__, args=args, kwargs=kwargs, error=e.args, **logger)
            except:
                pass
            raise e
        return res
    return f
