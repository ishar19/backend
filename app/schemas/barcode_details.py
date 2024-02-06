from pydantic import BaseModel

class BarcodeDetails(BaseModel):
  #Main Fields
  id: int
  name: str

  #Other Fields
  allergens: str | None
  brands: str | None
  categories: str | None
  countries: str | None
  ecoscore_grade: str | None
  ecoscore_score: int | None
  image_url: str | None
  ingredients: str | None
  nova_group: int | None
  nutrient_levels: dict
  nutriscore_grade: str | None
  nutriscore_score: int | None
  nutriments: dict
  packaging: str | None
  warnings: list[str]
