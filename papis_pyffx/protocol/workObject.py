from dataclasses import dataclass, field, asdict, replace
from enum import Enum
from typing import Union, Iterable
from datetime import datetime
import hashlib


class FileTypes(Enum):
    SAS = 'SAS'
    MOCK = 'MOCK'
    JSON = 'JSON'

    @classmethod
    def _missing_(cls, file : str):
        if file.upper() not in FileTypes._member_names_:
            raise ValueError(f'{file} not in FileTypes names:{FileTypes._member_names_}')
        else:
            return FileTypes[file.upper()]

@dataclass(frozen=True)
class WorkObject():
    #Work parameters
    inn_file_name : str # Name of file with data
    out_file_name : str # File to be created with pseudoData can be temporary file
    pseudo_col : tuple # Tuple of coloums to pseudonymise
    file_type : str  # Only supports file_type in FileTypes
    file_len : int = field(default=0) # Filelength of innFileName
    #Work actions
    encrypt : bool = field(default=True) # Encrypt if true otherwise decrypt
    del_after : bool = field(default=False) # Deletes innFileName after pseudonymisation if set
    out_file_archive : str = field(default=None) #Archive location of original file, local filesystem
    #Ssh connection
    user_name : str = field(default=None) # Username as string if set
    user_hash : str = field(default=None) # If empty then ssh is not used
    #Progress
    timing : datetime = field(default_factory=datetime.now)
    progress : str = field(default = None) # Element used for tracking progress

    def __post_init__(self):
        #Enforcing types, enforcingg that file_types are in the set of FileTypes (case insensitive)
        if isinstance(self.file_type, FileTypes):
            object.__setattr__(self, 'file_type', self.file_type.value)
        else:
            object.__setattr__(self, 'file_type', self.file_type.upper())
        if not self.file_type in FileTypes._member_names_:
            raise ValueError(f'File type not in {FileTypes._member_names_}')
        for name, field_type in self.__annotations__.items():
            element = self.__dict__[name]
            if not (element == None or isinstance(element, field_type)):
                object.__setattr__(self, name, field_type(element))
    
    def asdict(self) -> dict[str, any]:
        return asdict(self)
    
    def touch(self):
        return replace(timing = datetime.now())
        
    @classmethod
    def shortWO(cls, inn_file_name : str, out_file_name : str, pseudo_col : Iterable, file_type : Union[FileTypes, str], file_len : int = 0,
        encrypt : bool = True, del_after : bool = False, out_file_archive : str = None, user_name : str = None, progress : str = None, 
        pw : str = None, secret_val : str = None):

        filetype = filetype if isinstance(filetype, FileTypes) else FileTypes(filetype)
        if None in (user_name, pw, secret_val):
            raise ValueError(f'username, pw or secret_val is None for user:{user_name}')
        return WorkObject(inn_file_name = inn_file_name, out_file_name = out_file_name, pseudo_col = tuple(pseudo_col), file_type = file_type, 
            file_len = file_len, encrypt = encrypt, del_after = del_after, out_file_archive = out_file_archive, user_name = user_name, progress = progress,
            user_hash = cls.get_user_hash(user_name, pw, secret_val))
    
    @staticmethod
    def get_user_hash(username : str, pw : str, secretVal : str):
        return hashlib.sha512(''.join([username, pw, secretVal]).encode()).hexdigest()[0:64]

    EQUAL_ELEMENTS = ('inn_file_name', 'out_file_name', 'pseudo_col', 'file_type', 
             'encrypt', 'user_name')
    def __eq__(self, other):
        return all(getattr(self, el) == getattr(other, el) for el in self.EQUAL_ELEMENTS)