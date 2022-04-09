import time


def stTime(func):
    """
        st decorator to calculate the total time of a func
    """

    def stFunc(*args, **keyArgs):
        t1 = time.time()
        r = func(*args, **keyArgs)
        t2 = time.time()
        print("Function=%s, Time=%s" % (func.__name__, t2 - t1))
        return r

    return stFunc
