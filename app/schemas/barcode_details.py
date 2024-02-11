from ..crud import Product
from pydantic import BaseModel
from uuid import UUID
import ast
import re

class BarcodeDetails(BaseModel):
  id: int
  name: str | None
  allergens: list[str]
  brands: list[str]
  carbon_footprint: int | None
  categories: list[str]
  countries: list[str]
  ecoscore_grade: str | None
  ecoscore_score: int | None
  image_url: str | None
  ingredients: list[str]
  nova_group: int | None
  nutrient_levels: dict
  nutriscore_grade: str | None
  nutriscore_score: int | None
  nutriments: dict
  packaging: str | None
  warnings: list[str]
  
class BarcodeLookupHistory(BarcodeDetails):
  history_id: UUID

  def from_product_history_id(product: Product, history_id: UUID):
    kwargs = product.__dict__
    for (key, value) in kwargs.copy().items():
      if type(value) is str:
        middle_regex_str = '[a-z]+:'
        value = re.sub(rf'^{middle_regex_str}', '', value)
        value = re.sub(rf',{middle_regex_str}', ',', value)
        kwargs[key] = value
      if key in [ 'nutrient_levels', 'nutriments', 'warnings']:
        kwargs[key] = ast.literal_eval(value)
      elif key in ['allergens', 'brands', 'categories', 'countries', 'ingredients']:
        kwargs[key] = [] if value is None else [value.strip() for value in value.split(',')]
    return BarcodeLookupHistory(
      **kwargs,
      history_id=history_id
    ) 

class BarcodeRequestDetails(BaseModel):
  user_id : int
  barcode : int
