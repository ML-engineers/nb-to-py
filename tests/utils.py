import inspect

def function_to_lines(func):
    source_code = inspect.getsource(func)
    return [line+"\n" for line in source_code.split('\n')]