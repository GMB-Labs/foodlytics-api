from openai import OpenAI
import json
from src.shared.infrastructure.settings import settings

class MealRecognitionService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.GPT_API_KEY)

    def analyze_meal(self, image_url: str) -> dict:
        prompt = (
            "Analyze the following meal image and estimate its macronutrients.\n\n"
            "Respond STRICTLY in JSON.\n"
            "All numeric fields MUST contain ONLY numbers (no units, no text, no labels).\n"
            "Do NOT include 'g', 'grams', 'kcal', or any other units.\n\n"
            "Required JSON structure:\n"
            "{\n"
            '  "name": string,\n'
            '  "approximate_weight in grams": number,\n'
            '  "kcal": number,\n'
            '  "protein": number,\n'
            '  "carbs": number,\n'
            '  "fats": number\n'
            "}\n\n"
            f"Image: {image_url}"
        )

        result = self.client.responses.create(
            model="gpt-5-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": image_url}
                    ],
                }
            ],
        )
        print(json.dumps(result, indent=2))
        try:
            return json.loads(result.output_text)
        except Exception:
            return {"error": "Invalid JSON returned", "raw": result.output_text}
