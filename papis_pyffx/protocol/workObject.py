from dataclasses import dataclass
from enum import Enum
from typing import Union, Iterable
import hashlib

class FileTypes(Enum):
    SAS = 'SAS'
    MOCK = 'MOCK'

    @classmethod
    def _missing_(cls, file : str):
        if file.upper() not in FileTypes._member_names_:
            raise ValueError(f'{file} not in FileTypes names:{FileTypes._member_names_}')
        else:
            return FileTypes[file.upper()]

@dataclass(frozen=True)
class WorkObject():
    #Work parameters
    innFileName : str # Name of file with data
    outFileName : str # File to be created with pseudoData can be temporary file
    pseudoCol : tuple # Tuple of coloums to pseudonymise
    filetype : FileTypes = FileTypes.MOCK #'sas' and 'mock' supported
    filelen : int = 0# Filelength of innFileName
    #Work actions
    encrypt : bool = True # Encrypt if true otherwise decrypt
    del_after : bool = False # Deletes innFileName after pseudonymisation if set
    outFileArchive : str = None #Archive location of original file, local filesystem
    #Ssh connection
    username : str = None # Username as string if set
    userHash : str = None # If empty then ssh is not used 

    @staticmethod
    def shortWO(innFileName : str, outFileName : str, pseudoCol : Union[tuple, Iterable], filetype : Union[FileTypes, str], filelen : int = 0,
        encrypt : bool = True, del_after : bool = False, outFileArchive : str = None, username : str = None, userHash = None):

        filetype = filetype if isinstance(filetype, FileTypes) else FileTypes(filetype)
        return WorkObject(innFileName = innFileName, outFileName = outFileName, pseudoCol = tuple(pseudoCol), filetype = filetype, 
            filelen = filelen, encrypt = encrypt, del_after = del_after, outFileArchive = outFileArchive, username = username, 
            userHash = userHash)
    
    @staticmethod
    def getUserHash(username : str, pw : str, secretVal : str):
        return hashlib.sha224(''.join([username, pw, secretVal]).encode()).hexdigest()

    def copy(self):
        return WorkObject(innFileName = self.innFileName, outFileName = self.outFileName, pseudoCol = self.pseudoCol, 
            filetype = self.filetype, filelen = self.filelen, encrypt = self.encrypt, del_after = self.del_after, 
            outFileArchive = self.outFileArchive, username = self.username, userHash = self.userHash)
    
    #def asdict(self) -> dict:       
