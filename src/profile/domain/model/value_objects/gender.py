from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

    @classmethod
    def from_string(cls, gender_str: str) -> "Gender":
        if not gender_str:
            raise ValueError("Gender cannot be empty.")
        normalized = gender_str.strip().lower()
        for gender in cls:
            if gender.value == normalized:
                return gender
        raise ValueError(f"'{gender_str}' is not a valid gender.")