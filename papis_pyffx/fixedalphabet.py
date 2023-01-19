import string 
from papis_pyffx.codecs import Codec

class FixedAlphabet(Codec):
    #Filters a string removing encrypted only that are not part of the alphabet.
    #alphabet. The values not part of the alphabet are ignored.
    #E.g. if alphabet = 'abcde', and cleartext = 'table' then only 'abe' is
    # encrypted the other elements are left in place.
    #If no alphabet is given the the alphabet consists of 'a-z,A-z,0-9'
    def __init__(self, ffx, key,
                 alphabet=string.ascii_letters + string.digits, 
                 **kwargs):
        super().__init__(ffx, key, alphabet, **kwargs)
        
    def encrypt(self, v):
        #Encrypts the variable v
        pack, split = self.pack(v)
        return self.unpack(self.ffx.encrypt(pack), split)

    def decrypt(self, v):
        #Decrypts the variable v
        pack, split = self.pack(v)
        return self.unpack(self.ffx.decrypt(pack), split)

    def filter(self, v):
        #Filters v for values not part of the alphabet. Return filtered string.
        return ''.join([x for x in v if x in self.setAlphabet])
    
    def unfilter(self, orig : str, pseudo : str):
        #Unfilter takes a string as orig and the pseudonymised value as string.
        #The length of pseudo and of the function filter should be the same 
        it = iter(pseudo)
        ret = ''.join([next(it) if c in self.setAlphabet
                else c for c in orig])
        ne = next(it, None)
        if ne != None:
            raise AttributeError('Wrong size of pseudo')
        return ret

    def pack(self, v):
        #Splits the string into two strings, the first containing only the string
        #converted to integers based on the pack_map, and the second including 
        #elements not part of the pack_map 
        if not isinstance(v, str):
            v = str(v)
        split = [self.pack_map[c] if c in self.pack_map else c for c in v]
        pack = list(filter(lambda x: isinstance(x, int), split))
        return pack, split

    def unpack(self, v, split):
        #First converts the list v to 'letters' based on the pack_map, then 
        #merges v and split by inserting elements from v into split whenever
        #the element of split is an integer
        #Note: Modifies the list split
        unpacked = super().unpack(v)
        i = 0
        for j in range(len(split)):
            if isinstance(split[j], int):
                split[j] = unpacked[i]
                i += 1
        return ''.join(split)