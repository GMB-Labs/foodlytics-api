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
        Devuelve únicamente JSON crudo, sin markdown y sin comentarios.

        Objetivo:
        Identificar el plato principal en la imagen y listar cada uno de sus componentes por separado.

        Estructura del JSON existente:

        {
          "dish_name": string,
          "items": [
            {
              "name": string,
              "approximate_weight": number,
              "kcal_per_gram": number,
              "protein_per_gram": number,
              "carbs_per_gram": number,
              "fats_per_gram": number
            }
          ]
        }

        Reglas:
        - "dish_name" debe ser el nombre del plato completo en español.
        - "items" debe contener cada componente separado.
        - approximate_weight es el peso estimado en gramos.
        - Valores nutricionales son por gramo.
        - No incluyas unidades.
        - Devuelve solo JSON limpio.
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
