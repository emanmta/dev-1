from pydantic import BaseModel, Field
from typing import Optional, List, Union
from enum import Enum

class Item(BaseModel):
    title: str
    description: Optional[str] = None
    qty: Optional[int] = None
    price: Optional[Union[float, int]] = None
    note: Optional[str] = None

class ComplaintCategory(str, Enum):
    housekeeping = "housekeeping"
    maintenance = "maintenance"
    concierge = "concierge"

class ComplaintOrder(BaseModel):
    category: ComplaintCategory
    items: List[Item]
    note: Optional[str] = None
    additional_note: Optional[str] = None

class ComplaintTicket(BaseModel):
    orders: List[ComplaintOrder]
    x_session_token: str