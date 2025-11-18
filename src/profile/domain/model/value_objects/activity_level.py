from enum import Enum


class ActivityLevel(Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"

    @classmethod
    def from_string(cls, value: str) -> "ActivityLevel":
        if not value:
            raise ValueError("Activity level cannot be empty.")
        normalized = value.strip().lower()
        mapping = {
            "sedentario": cls.SEDENTARY,
            "ligero": cls.LIGHT,
            "ligera": cls.LIGHT,
            "moderado": cls.ACTIVE,
            "activo": cls.ACTIVE,
            "muy_activo": cls.VERY_ACTIVE,
            "muy activo": cls.VERY_ACTIVE,
        }
        if normalized in mapping:
            return mapping[normalized]
        for level in cls:
            if level.value == normalized:
                return level
        raise ValueError(f"'{value}' is not a valid activity level.")
