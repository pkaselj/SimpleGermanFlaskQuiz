from typing import Callable, List, Self, Tuple, Union
from error import DictionaryAppError, DictionaryAppErrorAggregate
import csv

class Displayable:
    def GetCroatian(self) -> str:
        pass

    def GetGerman(self) -> str:
        pass

    def GetSolution(self) -> str:
        pass


class Parseable:
    @classmethod
    def GetIdentifier(cls) -> str:
        pass

    def Parse(self, data : Tuple[str]) -> bool:
        pass

class DictionaryItem(Displayable, Parseable):
    pass

class VerbItem(DictionaryItem):
    _german : str
    _croatian : str

    @classmethod
    def GetIdentifier(cls):
        return 'verb'
    
    def Parse(self, data : Tuple[str]) -> bool:
        try:
            self._german = data[1]
            self._croatian = data[2]
        except Exception as ex:
            return False
        return True
    
    def GetGerman(self):
        return self._german
    
    def GetCroatian(self):
        return self._croatian
    
    def GetSolution(self):
        return self._german.lower() + ' - ' + self._croatian.upper()

class NounItem(DictionaryItem):
    _german_singular : str
    _german_article : str
    _german_plural : str
    _croatian : str

    @classmethod
    def GetIdentifier(cls):
        return 'noun'
    
    def Parse(self, data : Tuple[str]) -> bool:
        try:
            self._german_article = data[1]
            self._german_singular = data[2]
            self._german_plural = data[3]
            self._croatian = data[4]
        except Exception as ex:
            return False
        return True
    
    def GetGerman(self):
        return self._german_singular.capitalize()
    
    def GetCroatian(self):
        return self._croatian
    
    def GetSolution(self):
        _str = f'{self._german_article} {self._german_singular.capitalize()} - '
        if len(self._german_plural) > 0 :
            _str += f'die {self._german_plural.capitalize()} - '
        _str += f'{self._croatian.upper()}'
        return _str

class AdverbAdjectiveItem(DictionaryItem):
    _german : str
    _croatian : str

    @classmethod
    def GetIdentifier(cls):
        return 'ad'
    
    def Parse(self, data : Tuple[str]) -> bool:
        try:
            self._german = data[1]
            self._croatian = data[2]
        except Exception as ex:
            return False
        return True
    
    def GetGerman(self):
        return self._german
    
    def GetCroatian(self):
        return self._croatian
    
    def GetSolution(self):
        return self._german.lower() + ' - ' + self._croatian.upper()

class PhraseItem(DictionaryItem):
    _german : str
    _croatian : str

    @classmethod
    def GetIdentifier(cls):
        return 'phrase'
    
    def Parse(self, data : Tuple[str]) -> bool:
        try:
            self._german = data[1]
            self._croatian = data[2]
        except Exception as ex:
            return False
        return True
    
    def GetGerman(self):
        return self._german
    
    def GetCroatian(self):
        return self._croatian
    
    def GetSolution(self):
        return self._german.lower() + ' - ' + self._croatian.upper()
    
class PrononunItem(DictionaryItem):
    _german : str
    _croatian : str

    @classmethod
    def GetIdentifier(cls):
        return 'pron'
    
    def Parse(self, data : Tuple[str]) -> bool:
        try:
            self._german = data[1]
            self._croatian = data[2]
        except Exception as ex:
            return False
        return True
    
    def GetGerman(self):
        return self._german
    
    def GetCroatian(self):
        return self._croatian
    
    def GetSolution(self):
        return self._german.lower() + ' - ' + self._croatian.upper()

_Parsers : Tuple[type[Parseable]] = (
    VerbItem,
    NounItem,
    PhraseItem,
    AdverbAdjectiveItem,
    PrononunItem
)

def _GetParser(id : str) -> Union[DictionaryItem | None]:
    for parser_cls in _Parsers:
        if parser_cls.GetIdentifier().lower().strip() == id.lower().strip():
            parser_obj = parser_cls()
            return parser_obj
    return None

def ParseFile(file : str, warn_logger : Callable = None) -> Tuple[DictionaryItem]:
    if warn_logger is None:
        warn_logger = lambda *args : None

    data : List[DictionaryItem] = []
    with open(file, 'r', encoding="utf-8-sig") as fp:
        reader = csv.reader(fp)
        ctr = 0
        for row in reader:
            ctr += 1
            if len(row) < 1:
                raise DictionaryAppError(f'Error while parsing row {ctr} of CSV file "{file}". Row empty.')
            else:
                parser = _GetParser(row[0])
                if parser is None:
                    warn_logger(f'Error while parsing row {ctr} of CSV file "{file}". Cannot find parser for id: {row[0]}.')
                else:
                    parser.Parse(row)
                    data.append(parser)
    return tuple(data)