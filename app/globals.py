from dataclasses import dataclass
from typing import Tuple

from data import Displayable


@dataclass
class GlobalContext:
    ITEM_STORE : Tuple[Displayable] = ()
    NR_OF_ITEMS_TO_SELECT = 10
    QUIZ_DATA_DIR = None