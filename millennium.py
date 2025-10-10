from dataclasses import dataclass

@dataclass
class EDed:
    co : str
    id : str 

    def __post_init__(self):
        if len(self.co) > 10:
            raise ValueError("Field 'co' must be 10 characters or less.")
        if len(self.id) > 10:
            raise ValueError("Field 'id' must be 10 characters or less.")
        
