from pydantic import BaseModel
from typing import Optional, List, Union
from enum import Enum

class Item(BaseModel):
    title: str
    description: Optional[str] = None
    qty: Optional[int] = None
    price: Optional[Union[float, int]] = None
    note: Optional[str] = None

class RestaurantCategory(str, Enum):
    restaurant = "restaurant"
    room_service = "room_service"

class RestaurantOrder(BaseModel):
    category: Optional[RestaurantCategory]
    items: List[Item]
    note: Optional[str] = None
    additional_note: Optional[str] = None

class RestaurantTicket(BaseModel):
    orders: List[RestaurantOrder]
