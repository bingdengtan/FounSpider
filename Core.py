import time

class common():
    @staticmethod
    def props(obj):
        pr = {}
        for name in dir(obj):
            value = getattr(obj, name)
            if not name.startswith('__') and not callable(value) and not name.startswith('_'):
                pr[name] = value
        return pr

    @staticmethod
    def getCurrentDateTimeString():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())