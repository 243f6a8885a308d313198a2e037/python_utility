import os
import sys
import enum
import datetime
import traceback
import collections
import dataclasses
from typing import Tuple, List, Optional


class ErrorLevel(enum.Enum):
    CRITICAL = 1
    ERROR = 2
    WARNING = 4
    INFO = 8
    TRACE = 16

@dataclasses.dataclass
class ErrorInstance:
    error_id: int
    datetime_utc: datetime.datetime
    error_level: ErrorLevel
    direct_causes: Tuple[int, ...]
    message: str
    stack_trace: List[traceback.FrameSummary]
    kwargs: Optional[dict]

    def __str__(self):
        stack_trace = [f'<file {st.filename}, line {st.lineno} in {st.name}>' for st in self.stack_trace]
        return f"[{self.error_id}] {self.datetime_utc.isoformat()} <{self.error_level}> {self.direct_causes} {repr(self.message)} {repr(self.kwargs)} {repr(stack_trace)}"

class ErrorManager:
    def __init__(self, name, logpath: Optional[os.PathLike] = None):
        self.name = name
        self.errors = []
        self.logfile = None
        if logpath is not None:
            self.set_logpath(logpath)
        self.level_statistics = collections.Counter()

    def set_logpath(self, logpath: os.PathLike):
        if getattr(self, 'logfile') is not None:
            self.logfile.close()
        self.logpath = logpath
        self.logfile = open(self.logpath, 'w', encoding='utf_8')

    def check_is_ready(self):
        if not hasattr(self, 'logpath'):
            raise Exception('ERROR: ErrorManager: `self.logpath` not set. abort.')
        if getattr(self, 'logfile') is None:
            raise Exception('ERROR: ErrorManager: `self.logfile` is None. abort.')

    def is_critical_happened(self):
        return self.level_statistics[ErrorLevel.CRITICAL] > 0

    def is_error_happened(self):
        return self.level_statistics[ErrorLevel.ERROR] > 0

    def is_error_or_worse_happened(self):
        return self.is_error_happened() or self.is_critical_happened()

    def add_message(
        self,
        error_level: ErrorLevel, message: str, direct_causes: Tuple[int, ...] = (), *,
        ignore_traces: Optional[int] = 1, **kwargs):

        self.check_is_ready()
        datetime_utc = datetime.datetime.utcnow()
        stack_trace = traceback.extract_stack()[:-ignore_traces]
        error_id = len(self.errors)
        error = ErrorInstance(error_id, datetime_utc, error_level, direct_causes, message, stack_trace, kwargs)
        self.errors.append(error)
        self.level_statistics[error_level] += 1
        self.logfile.write(str(error) + '\n')
        return error_id

    def add_critical(self, message: str, direct_causes: Tuple[int, ...] = (), **kwargs):
        self.add_message(ErrorLevel.CRITICAL, message, direct_causes, ignore_traces=2, **kwargs)
        raise Exception(message)

    def add_error(self, message: str, direct_causes: Tuple[int, ...] = (), **kwargs):
        return self.add_message(ErrorLevel.ERROR, message, direct_causes, ignore_traces=2, **kwargs)

    def add_warning(self, message: str, direct_causes: Tuple[int, ...] = (), **kwargs):
        return self.add_message(ErrorLevel.WARNING, message, direct_causes, ignore_traces=2, **kwargs)

    def add_info(self, message: str, direct_causes: Tuple[int, ...] = (), **kwargs):
        return self.add_message(ErrorLevel.INFO, message, direct_causes, ignore_traces=2, **kwargs)

    def add_trace(self, message: str, direct_causes: Tuple[int, ...] = (), **kwargs):
        return self.add_message(ErrorLevel.TRACE, message, direct_causes, ignore_traces=2, **kwargs)

    def add_exception(
        self,
        error_level: ErrorLevel, exc: Exception, **kwargs):

        self.check_is_ready()
        datetime_utc = datetime.datetime.utcnow()
        message = traceback.format_exc().splitlines()[-1]
        stack_trace = traceback.extract_tb(sys.exc_info()[2])
        error_id = len(self.errors)
        error = ErrorInstance(error_id, datetime_utc, error_level, (), message, stack_trace, kwargs)
        self.errors.append(error)
        self.level_statistics[error_level] += 1
        self.logfile.write(str(error) + '\n')
        return error_id

    def add_critical_exception(self, exc: Exception, **kwargs):
        self.add_exception(ErrorLevel.CRITICAL, exc, **kwargs)
        raise exc

    def add_error_exception(self, exc: Exception, **kwargs):
        return self.add_exception(ErrorLevel.ERROR, exc, **kwargs)

def trace_func_enter_leave(error_manager: ErrorManager):
    def deco_func(func: callable):
        def wrapper(*args, **kwargs):
            error_manager.add_trace(f'function {func.__name__} started.')
            func(*args, **kwargs)
            error_manager.add_trace(f'function {func.__name__} finished.')
        return wrapper
    return deco_func
