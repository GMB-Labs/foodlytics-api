from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    @classmethod
    def from_string(cls, gender_str: str):
        try:
            return cls(gender_str.upper())
        except ValueError:
            raise ValueError(f"'{gender_str}' no es un género válido.")