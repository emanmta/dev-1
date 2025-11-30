from pydantic import BaseModel
from typing import Optional, List, Union

class Item(BaseModel):
    title: str
    description: Optional[str] = None
    qty: Optional[int] = None
    price: Optional[Union[float, int]] = None
    note: Optional[str] = None

class RestaurantOrder(BaseModel):
    category: str = "room_service"
    items: List[Item]
    note: Optional[str] = None
    additional_note: Optional[str] = None

class RestaurantTicket(BaseModel):
    orders: List[RestaurantOrder]
    x_session_token: str