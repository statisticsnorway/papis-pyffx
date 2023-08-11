import string

class Filter:
    def __init__(self, alphabet : str = string.digits + string.ascii_letters) -> None:
        self.alphabet = alphabet
        self.asSet = {c for c in alphabet}

    def filter(self, v : str) -> str:
        """Filter a string v based on an alphabet, resturns an string containing only charactres contained in the alphabet.
            E.g. v = Åge and alphabet = string.ascii then filter returns ge"""
        return ''.join(ch for ch in v if ch in self.asSet)
    
    def unfilter(self, orig : str, pseudo : str) -> str:
        """Returns a string of pseudonmyised characters based on the origial and the pseudomyised tekst given in pseudo only changing elements
            that are part of the alphabet. Resturns an string of same length as orig with the elements in alphabet changed by the string in pseudo.
            E.g. orig = Åge, pseudo = th and alphabet = string.ascii then unfilter returns Åth
            Raises an error if pseudo is of wrong length. 
        """
        #Unfilter takes a string as orig and the pseudonymised value as string.
        #The length of pseudo and of the function filter should be the same 
        it = iter(pseudo)
        ret = ''.join(next(it) if ch in self.asSet else ch for ch in orig)
        ne = next(it, None)
        if ne != None:
            raise AttributeError('Wrong size of pseudo')
        return ret
