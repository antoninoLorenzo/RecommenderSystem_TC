import os
import time
import linecache
import tracemalloc
from functools import wraps


def performance_test(function):
    """
    Decorator to evaluate performance of a given function, returns a tuple that consists of:
        - result of the function
        - execution_time
        - memory usage snapshot
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start = time.time()

        result = function(*args, **kwargs)

        execution_time = (time.time() - start)
        memory_snapshot = tracemalloc.take_snapshot()

        return result, execution_time, memory_snapshot

    return wrapper


def display_top(snapshot, key_type='lineno', limit=3):
    """
    StackOverflow: https://stackoverflow.com/questions/552744/how-do-i-profile-memory-usage-in-python
    """
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))
