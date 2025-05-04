from typing import List


class DictionaryAppError(Exception):
    def __init__(self, message):            
        super().__init__(message)

class DictionaryAppErrorAggregate(DictionaryAppError):
    _errors : List[DictionaryAppError] = []

    def __init__(self):            
        super().__init__(None)

    def AppendError(self, err : DictionaryAppError):
        self._errors.append(err)

    def __str__(self):
        message = f'Aggregate error, total count = {len(self._errors)}.\n'
        for i, err in enumerate(self._errors):
            message += '\n'
            message += f'Error {i}: {err}'
            message += '\n'
        return message