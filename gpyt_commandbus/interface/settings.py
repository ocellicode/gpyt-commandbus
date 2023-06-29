from abc import ABC
from typing import Any, Callable, Dict, List


class Settings(ABC):
    resources: List[Dict[str, Callable[..., Any]]] = NotImplemented
