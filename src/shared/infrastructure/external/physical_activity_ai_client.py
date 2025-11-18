from abc import ABC, abstractmethod
from typing import Optional


class PhysicalActivityAIClient(ABC):
    """
    Abstracción de un servicio externo (IA) para estimar calorías quemadas.
    """

    @abstractmethod
    def estimate_calories(
        self,
        *,
        weight_kg: float,
        activity_type: str,
        duration_minutes: float,
        intensity: Optional[str] = None,
    ) -> float:
        """
        Retorna las calorías quemadas estimadas para la actividad indicada.
        """
        raise NotImplementedError


class StubPhysicalActivityAIClient(PhysicalActivityAIClient):
    """
    Implementación stub que aproxima calorías usando METs según intensidad.
    """

    METS_BY_INTENSITY = {
        "low": 3.0,
        "moderate": 6.0,
        "high": 8.0,
    }

    DEFAULT_MET = 5.0

    def estimate_calories(
        self,
        *,
        weight_kg: float,
        activity_type: str,
        duration_minutes: float,
        intensity: Optional[str] = None,
    ) -> float:
        met = self.METS_BY_INTENSITY.get((intensity or "").lower(), self.DEFAULT_MET)
        # Fórmula clásica: kcal = MET * 3.5 * peso(kg) / 200 * minutos
        calories = met * 3.5 * weight_kg / 200 * duration_minutes
        return round(calories, 2)
