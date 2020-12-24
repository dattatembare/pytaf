import inspect
import logging
import logging.config as logging_config
import os
from datetime import datetime
from functools import wraps, lru_cache
from logging import Logger
from time import time
from typing import TypeVar, cast, Callable, Any

from lib.commandline_args import cargs
from lib.utils import get_logger_config

T = TypeVar('T')
THIS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = '../zlogs'
LOG_FILE_PATH = f'{THIS_DIR_PATH}/{CONFIG_DIR}/'

PERF = 9
TRACE = 8
PERF_TEXT = 'PERF'
TRACE_TEXT = 'TRACE'


class MyLogger(Logger):

    def trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)  # type: ignore

    def perf(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(PERF):
            self._log(PERF, msg, args, **kwargs)  # type: ignore


@lru_cache()
def get_logger(obj: Any = 'default') -> MyLogger:
    """
    Creates a logging object and returns it
    :param obj: obj with module, class and method information
    :return: logger object
    """

    name = obj if type(obj) == str else f'{obj.__module__}.{type(obj).__name__}'

    # Set new log levels
    logging.setLoggerClass(MyLogger)
    logging.addLevelName(PERF, PERF_TEXT)
    logging.addLevelName(TRACE, TRACE_TEXT)

    # Get logger-config json
    logger_config = get_logger_config()

    # Add timestamp to create new file for each new run
    # Updating the filename when {time} is part of filename in logger-config, otherwise log filename will be same
    for k, v in logger_config['handlers'].items():
        if 'filename' in v:
            filename = v.get('filename').replace('{time}', datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            v['filename'] = f'{LOG_FILE_PATH}/{filename}'

    logging_config.dictConfig(logger_config)

    logger = logging.getLogger(name)
    _cargs = cargs()
    logger.setLevel(_cargs.log_level.upper())
    assert isinstance(logger, MyLogger)

    return logger


def trace(orig_func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that wraps the passed in function and zlogs tracing messages
    :param orig_func: original calling function
    :return: wrapper for orig_func
    """
    frm = inspect.stack()[1]  # Calling method absolute file/module path
    logger: MyLogger = get_logger()

    @wraps(orig_func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : '
                     f'START execution with args: {args}, and kwargs: {kwargs}')
        func_result = orig_func(*args, **kwargs)
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : END execution')
        return func_result

    return wrapper


def timer(orig_func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that wraps the passed in function and zlogs execution time for that function
    :param orig_func: original calling function
    :return: wrapper for orig_func
    """

    frm = inspect.stack()[1]  # Calling method absolute file/module path
    logger: MyLogger = get_logger()

    @wraps(orig_func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : '
                     f'START execution with args: {args}, and kwargs: {kwargs}')
        start = time()
        func_result = orig_func(*args, **kwargs)
        execution_time = time() - start
        logger.perf(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : Ran in: {execution_time} sec')
        logger.trace(f'[{_source_path(frm.filename)}.{orig_func.__name__}()] : END execution')
        return cast(T, func_result)

    return wrapper


def exception(orig_func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that wraps the passed in function and zlogs exceptions should one occur
    :param orig_func: original calling function
    :return: wrapper for orig_func
    """

    logger: MyLogger = get_logger()

    @wraps(orig_func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            func_result = orig_func(*args, **kwargs)
        except Exception as e:
            logger.exception(f'{e}')
            raise
        return cast(T, func_result)

    return wrapper


def _source_path(filename: str) -> str:
    """
    method returns source path
    :param filename: source code file name
    :return: source file path from src package
    """

    source_path = filename.replace('.py', '').replace('/', '.').replace('\\', '.')
    if '.test.' in source_path:
        return source_path[source_path.index('.test.') + 1:]
    elif '.test_automation.' in source_path:
        return source_path[source_path.index('.test_automation.') + 1:]
    elif '.src.' in source_path:
        return source_path[source_path.index('.src.') + 1:]
    else:
        return source_path
