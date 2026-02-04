from dataclasses import dataclass
from typing import List, Optional

@dataclass
class VideoInfo:
    title: str
    url: str
    duration: Optional[int] = None  # Duration in seconds
    description: Optional[str] = None
    tags: Optional[List[str]] = None


