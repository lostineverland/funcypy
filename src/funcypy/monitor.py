'''It's good to have data about the functions and processes that we run
'''
import functools
import random
import json
import traceback
import time, datetime
from datetime import datetime
from typing import Callable, Any, Dict, Union
from . times import epoch_to_iso
from . seqs import is_lazy

missing = object()

def json_serializer(obj: object) -> Callable:
    if isinstance(obj, set):
        return str(obj)
    
    if isinstance(obj, datetime):
        return epoch_to_iso(obj.timestamp())
    
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    
    if isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return namedtuple_to_dict(obj)

    if isinstance(obj, Exception):
        return {
            'type': type(obj).__name__,
            'message': str(obj),
            'args': obj.args,
            'traceback': traceback.format_exception(None, obj, obj.__traceback__),
        }
    
    if is_lazy(obj):
        return str(obj)

    raise TypeError('Type {} not serializable'.format(str(type(obj))))

def namedtuple_to_dict(obj):
    if isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return {field: namedtuple_to_dict(getattr(obj, field)) for field in obj._fields}
    elif isinstance(obj, list):
        return [namedtuple_to_dict(item) for item in obj]
    else:
        return obj

def log(x=None, name='value', logger=print, **kwargs) -> Any:
    '''A logging function which returns the value (as opposed to print which returns `None`)
        but will also print a JSON `{value: x}` of the given value. It also allows for
        kwargs to be included in the JSON.
    '''
    if x: kwargs = {name: x, **kwargs}
    try:
        logger(json.dumps(kwargs, default=json_serializer))
    except TypeError as e:
        try:
            logger(json.dumps({ **kwargs, 
                    'res': str(kwargs.get('res')),
                    'args': str(kwargs.get('args')),
                    'kwargs': str(kwargs.get('kwargs')),
                    'log_err': {'level 1':str(e.args)},
                }))
        except Exception as e:
            logger(json.dumps({'args': str(kwargs), 'log_err': {'level 2': str(e.args)}}))
            print({**kwargs, 'logging_error': e})
    except Exception as e:
        logger(json.dumps({'args': str(kwargs), 'log_err': {'level 3': str(e.args)}}))
        print({**kwargs, 'logging_error': e})
    return x

def track(func: Callable=missing, frequency: Union[int, Callable]=0, arg_history={}, **log_opts: Dict) -> Callable:
    '''This function wraps any function and logs metrics on the function
        func: the funcion being tracked
        frequency: an integer for sampling frequency (1/frequency) or a function which returns a boolean
            such that frequency(func(*args **kwargs)) -> bool
            A `False` or falsy value will only log on error
    '''
    if func is missing:
        return functools.partial(
            track,
            frequency=frequency,
            arg_history=arg_history,
            **log_opts)
    @functools.wraps(func)
    def f(*args0, **kwargs0):
        if hasattr(func, '__name__'):
            func_name = func.__name__
        else:
            func_name = repr(func)
        try:
            args = arg_history.get('args', []) + list(args0)
            kwargs = {**arg_history.get('kwargs', {}), **kwargs0}
            t0 = time.time()
            res = func(*args0, **kwargs0)
            t1 = time.time()
            if callable(res):
                return track(
                    functools.update_wrapper(res, func),
                    frequency=frequency,
                    arg_history=dict(args=args, kwargs=kwargs),
                    **log_opts)
            if frequency:
                if callable(frequency):
                    if frequency(res):
                        log(func=func_name, res=res, args=args, kwargs=kwargs, duration=t1-t0, **log_opts)
                elif random.randint(1, frequency) == 1:
                    log(func=func_name, res=res, args=args, kwargs=kwargs, duration=t1-t0, **log_opts)
        except Exception as e:
            try:
                log(func=func_name, args=args, kwargs=kwargs, error=e, **log_opts)
            except:
                last_resource_logger(func=func, args=args, kwargs=kwargs, error=e, **log_opts)
            raise e
        return res
    return f

def last_resource_logger(*args, **kwargs):
    for i, x in enumerate(args):
        try:
            print({'last_resource_logger: arg[{}]:'.format(i): x})
        except:
            print('last_resource_logger: could not log arg[{}]'.format(i))
    for k, v in kwargs.items():
        try:
            print('last_resource_logger:', {k: v})
        except:
            print('last_resource_logger: could not log kwargs: {}'.format(k))
