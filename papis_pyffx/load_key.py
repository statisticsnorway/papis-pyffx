from Crypto.Cipher import AES

#Loads key from file
#1'st line of file is key
#2'nd line of file is a key verification code (16-bytes encryption of nullvector)

def load_key_from_file(filename: str) -> str:
    with open(filename, 'r') as file:
        keyHex = file.readline().strip()
        cvcHex = file.readline().strip()
        if not len(keyHex) in [16*2,24*2,32*2]:
            errorMessage = f'Keylength is {len(keyHex)} not 16, 24 or 32 bytes (x2 for length)'
            raise ValueError(errorMessage)
        if not len(cvcHex) in [16*2]:
            errorMessage = f'CVC is {len(cvcHex)} is not 16 bytes'
            raise ValueError(errorMessage)
            
        key = bytes.fromhex(keyHex)
        cvc = bytes.fromhex(cvcHex)
        
        if getCVC(key) != cvc:
            #print getCVC(key).hex()
            raise ValueError('CVC does not match')
        return key

def getCVC(key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(bytes.fromhex('00000000000000000000000000000000'))
        
        