import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            res = {
                'time': f'{datetime.datetime.now()}',
                'name_function': old_function.__name__,
                'arguments': [args, kwargs],
                'result': result
            }
            with open(path, 'a') as main:
                main.write(str(res) + '\n')
            return result
        return new_function
    return __logger