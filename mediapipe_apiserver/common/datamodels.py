from pydantic import BaseModel
from typing import List

class IntrinsicsMatrix(BaseModel):
    color: List[List[float]] = None
    depth: List[List[float]] = None