from pydantic import BaseModel

class CameraOption(BaseModel):
    """This class stores camera options
    """
    use_depth: bool = False