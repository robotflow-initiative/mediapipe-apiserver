from pydantic import BaseModel

class CameraOption(BaseModel):
    use_depth: bool = False