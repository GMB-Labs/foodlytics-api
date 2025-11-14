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
        
        Debes identificar todos los alimentos presentes en la imagen.  
        Si el plato contiene múltiples componentes (por ejemplo: pollo a la brasa, papas fritas, ensalada), debes separarlos en elementos individuales dentro del arreglo "items".
        
        Por cada alimento detectado devuelve:
        
        - name: nombre del alimento en español.
        - approximate_weight: peso aproximado en gramos del alimento detectado.
        - kcal_per_gram: calorías por gramo (valor nutricional estándar).
        - protein_per_gram: gramos de proteína por gramo.
        - carbs_per_gram: gramos de carbohidratos por gramo.
        - fats_per_gram: gramos de grasa por gramo.
        
        Reglas:
        - Los valores nutricionales deben ser por gramo, no totales.
        - No incluyas unidades.
        - Todos los números deben ser valores numéricos puros.
        - El nombre debe estar siempre en español.
        - El JSON debe seguir exactamente esta estructura:
        
        {
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
