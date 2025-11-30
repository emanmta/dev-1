from pydantic import BaseModel, validator
from typing import Optional, List, Union

class Item(BaseModel):
    title: str
    description: Optional[str] = None
    qty: Optional[int] = None
    price: Optional[Union[float, int]] = None
    note: Optional[str] = None

class RestaurantOrder(BaseModel):
    category: str = "restaurant"
    items: List[Item]
    note: Optional[str] = None
    additional_note: Optional[str] = None

    @validator("category", pre=True, always=True)
    def set_category_default(cls, v):
        """Set default category if None or not provided."""
        return v or "restaurant"

class RestaurantTicket(BaseModel):
    orders: List[RestaurantOrder]