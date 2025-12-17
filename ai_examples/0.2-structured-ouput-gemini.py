from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional


class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient.")
    quantity: str = Field(description="Quantity of the ingredient, including units.")


class Recipe(BaseModel):
    recipe_name: str = Field(description="The name of the recipe.")
    prep_time_minutes: Optional[int] = Field(
        description="Optional time in minutes to prepare the recipe."
    )
    ingredients: List[Ingredient]
    instructions: List[str]


# gemini-2.5-flash
# gemini-3-pro-preview
# config=types.GenerateContentConfig(
#     thinking_config=types.ThinkingConfig(thinking_level="low")
# ),


GOOGLE_MODEL_NAME = "gemini-3-pro-preview"

google_client = genai.Client()

prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
"""

# --- Response 1: Using plain dictionary for config ---
response = google_client.models.generate_content(
    model=GOOGLE_MODEL_NAME,
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)

# --- Response 2: Using types.GenerateContentConfig for config ---
response = google_client.models.generate_content(
    model=GOOGLE_MODEL_NAME,
    contents=prompt,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"),
        response_mime_type="application/json",
        response_json_schema=Recipe.model_json_schema(),
    ),
)

recipe = Recipe.model_validate_json(response.text)
print(recipe)

recipe.ingredients[0].name

from google import genai
from google.genai import types

google_client = genai.Client()

response = google_client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="How does AI work?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
)

print(response.text)
