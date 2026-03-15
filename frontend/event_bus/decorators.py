# decorators.py

def subscribe(func):
    func._subscribe = True
    return func