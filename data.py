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

class NounItem(DictionaryItem):
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
        return self._german.lower() + '\n\n' + self._croatian.upper()

class VerbItem(DictionaryItem):
    pass

class AdverbAdjectiveItem(DictionaryItem):
    pass

class PhraseItem(DictionaryItem):
    pass

_Parsers : Tuple[type[Parseable]] = ( NounItem, )

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