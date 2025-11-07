from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UpdateProfileCommand:
    """
    Command to update an existing profile.
    """
    id: str
    first_name: str
    age: int
    height_cm: float
    weight_kg: float
    goal_type: str

def __init__(self, user_id, first_name,last_name, age, height_cm, weight_kg, gender, goal_type):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.gender = gender
        self.goal_type = goal_type