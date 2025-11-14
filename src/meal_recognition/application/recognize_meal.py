from openai import OpenAI
import base64
import json
from src.shared.infrastructure.settings import settings


def clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
    return text.strip()


class MealRecognitionService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.GPT_API_KEY)

    def analyze_meal(self, image_bytes: bytes) -> dict:
        b64 = base64.b64encode(image_bytes).decode()

        prompt = """
            Return strictly raw JSON without markdown fences.

            Keep this EXACT schema:

            {
              "name": string,
              "approximate_weight": number,
              "kcal": number,
              "protein": number,
              "carbs": number,
              "fats": number
            }

            Rules:
            - "name" MUST be the food name in SPANISH.
            - approximate_weight MUST ALWAYS be 1.
            - kcal, protein, carbs and fats MUST be nutritional values PER 1 GRAM.
            - Do NOT estimate total weight.
            - Do NOT include units.
            - All numeric values must be plain numbers.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/webp;base64,{b64}"
                                }
                            }
                        ]
                    }
                ]
            )

            content = response.choices[0].message.content

            if isinstance(content, str):
                raw = content
            else:
                raw = "".join(
                    block.text for block in content
                    if hasattr(block, "type") and block.type == "text"
                )

            raw = clean_json(raw)
            return json.loads(raw)

        except json.JSONDecodeError:
            return {"error": "Invalid JSON returned", "raw": raw}
        except Exception as e:
            return {"error": str(e)}
