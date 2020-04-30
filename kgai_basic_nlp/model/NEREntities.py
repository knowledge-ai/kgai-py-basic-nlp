from dataclasses import dataclass
from typing import Optional


@dataclass
class NEREntities(object):
    word: str
    entity: str
    tool: str
    confidence: Optional[float]
