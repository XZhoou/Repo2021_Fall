from playsound import playsound
from functools import wraps

class PlaySoundClass:
    def __init__(self):
        pass
    
    def __call__(self,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            func(*args,**kwargs)
            playsound("BUAA_21/Week8/sound/14430.wav")
        return wrapper