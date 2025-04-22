import threading

typing_lock = threading.Lock()

def threaded(fn):
    def wrapper(*args, **kwargs):
        if typing_lock.locked():
            return
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
    return wrapper
