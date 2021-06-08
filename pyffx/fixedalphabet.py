import string 
from pyffx.codecs import Codec

class FixedAlphabet(Codec):
    #Same as String except encrypted values that are not part of the standard
    #alphabet are ignored. E.g. if alphabet = 'abcde', and cleartext = 'table'
    #then only 'abe' is encrypted the other elements are left in place.
    #If no alphabet is given the the alphabet consists of 'a-z,A-z,0-9'
    def __init__(self, ffx, 
                 alphabet=string.ascii_lowercase + string.ascii_uppercase + string.digits, 
                 **kwargs):
        super(FixedAlphabet, self).__init__(ffx, alphabet, **kwargs)
        
    def encrypt(self, v):
        #Encrypts the variable v
        pack, split = self.pack(v)
        return self.unpack(self.ffx.encrypt(pack), split)

    def decrypt(self, v):
        #Decrypts the variable v
        pack, split = self.pack(v)
        return self.unpack(self.ffx.decrypt(pack), split)


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
        unpacked = super(FixedAlphabet, self).unpack(v)
        i = 0
        for j in range(len(split)):
            if isinstance(split[j], int):
                split[j] = unpacked[i]
                i += 1
        return ''.join(split)