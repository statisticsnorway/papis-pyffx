import time
from functools import wraps
from papis_pyffx.algorithms.ffx import FFX
from papis_pyffx.algorithms.ff1 import FF1
from papis_pyffx.algorithms.ff3 import FF3

#Function is timed result is written as print
def timeit(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Time {func.__name__}: {time.time()-start}s')
        return result
    return wrap

class SpeedTest():
    key1 = bytes.fromhex('2B7E151628AED2A6ABF7158809CF4F3C')
    key4 = bytes.fromhex('2B7E151628AED2A6ABF7158809CF4F3CEF4359D8D580AA4F')
    key7 = bytes.fromhex('2B7E151628AED2A6ABF7158809CF4F3CEF4359D8D580AA4F7F036D6F04FC6A94')
    
    clear1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    tweak1 = list(bytes.fromhex('39383736353433323130'))
    clear2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    tweak2 = list(bytes.fromhex('3737373770717273373737'))
    
    tweakff3 = bytes.fromhex('D8 E7 92 0A FA 33 0A 73')
    
    @classmethod
    def testAll(cls, repetions):
        return cls.ffx(repetions), cls.ff1(repetions), cls.ff3(repetions)
    
    @classmethod
    @timeit
    def ffx(cls, repetions):
        cipher = FFX(cls.key1, 10)
        for i in range(repetions):
            cipher.encrypt(cls.clear1, None)    
        cipher = FFX(cls.key1, 36)
        for i in range(repetions):
            cipher.encrypt(cls.clear2, cls.tweak2)      
        
    @classmethod
    @timeit
    def ff1(cls, repetions):
        cipher = FF1(cls.key1, 10)
        for i in range(repetions):
            cipher.encrypt(cls.clear1, [])    
        cipher = FF1(cls.key1, 36)
        for i in range(repetions):
            cipher.encrypt(cls.clear2, cls.tweak2)     
            
    @classmethod
    @timeit
    def ff3(cls, repetions):
        cipher = FF3(cls.key1, 10)
        for i in range(repetions):
            cipher.encrypt(cls.clear1, [])    
        cipher = FF3(cls.key1, 36)
        for i in range(repetions):
            cipher.encrypt(cls.clear2, cls.tweakff3)     