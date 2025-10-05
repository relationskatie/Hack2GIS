from typing import Optional, Literal
from pydantic import BaseModel, Field

class Range(BaseModel):
    from_: float | None = Field(alias="from", default=None)
    to: float | None = None

class Price(BaseModel):
    currency: str = "RUB"
    from_: float | None = Field(alias="from", default=None)
    to: float | None = None

class Filters(BaseModel):
    deal_type: Literal["Продажа","Аренда"]
    market_type: Literal["Вторичка","Новостройка","Не указано"]
    property_type: Literal["Квартира","Дом","Участок","Комната","Таунхаус","Доля в квартире","Часть дома"]
    rooms: str  # "Студия","1","2","3","4","5+"
    price: Price
    area_total: Range
    walk_to_metro: Optional[int] = None  # 5|10|20|null
    floor: Range
    floors_total: Range

class Output(BaseModel):
    weights: dict
    filters: Filters
    # почему такая конфигурация подходит: краткие пункты с привязкой к исходному тексту
    why: list[str] = []
