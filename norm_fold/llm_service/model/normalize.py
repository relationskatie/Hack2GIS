import json
import re
from .constants import INFRA

def _extract_json_block(s: str) -> dict:
    m = re.search(r"\{.*\}", s, re.S)
    if not m:
        raise ValueError("LLM не вернула JSON")
    return json.loads(m.group(0))

def renorm_weights(weights: dict) -> dict:
    w = {k: max(0.0, float(weights.get(k, 0.0))) for k in INFRA}
    s = sum(w.values()) or 1.0
    return {k: v/s for k,v in w.items()}

def sanitize_filters(data: dict, hints: dict) -> dict:
    """
    Если модель/пользователь не дали значения — умеренно додумываем по persona и подсказкам.
    """
    f = data.setdefault("filters", {})
    persona = hints.get("persona")

    # 1) deal_type
    if f.get("deal_type") not in ("Продажа", "Аренда"):
        if persona == "student":
            f["deal_type"] = "Аренда"
        else:
            f["deal_type"] = hints.get("deal_type", "Продажа")

    # 2) market_type
    allowed_mt = {"Вторичка","Новостройка","Не указано"}
    if f.get("market_type") not in allowed_mt:
        if persona == "young_family":
            f["market_type"] = "Новостройка"
        elif persona == "elderly":
            f["market_type"] = "Вторичка"
        else:
            f["market_type"] = "Не указано"

    # 3) property_type
    allowed_pt = {"Квартира","Дом","Участок","Комната","Таунхаус","Доля в квартире","Часть дома"}
    if f.get("property_type") not in allowed_pt:
        if persona == "student" and hints.get("pref_small"):
            # студент + «для одного/небольшая» → чаще Квартира-Студия
            f["property_type"] = "Квартира"
        elif persona == "student":
            f["property_type"] = "Комната"
        else:
            f["property_type"] = "Квартира"

    # 4) rooms
    allowed_rooms = {"Студия","1","2","3","4","5+"}
    rooms = f.get("rooms")
    if isinstance(rooms, int):
        rooms = str(rooms)
    if rooms not in allowed_rooms:
        # persona-based inference
        if persona in ("family_school","family_preschool"):
            rooms = "3"
        elif persona == "student" and hints.get("pref_small"):
            rooms = "Студия"
        elif persona == "student":
            rooms = "1"
        elif persona == "young_family":
            rooms = "2"
        else:
            rooms = "2"
    f["rooms"] = rooms

    # 5) price: учтём budget hint
    p = f.get("price")
    if not isinstance(p, dict):
        p = {}
    p.setdefault("currency", "RUB")
    if "from" not in p: p["from"] = None
    if "to" not in p: p["to"] = None
    if p.get("to") is None and hints.get("price_to"):
        p["to"] = int(hints["price_to"])
    f["price"] = p

    # 6) диапазоны
    def ensure_range(name):
        r = f.get(name)
        if not isinstance(r, dict):
            r = {}
        r.setdefault("from", None)
        r.setdefault("to", None)
        f[name] = r
    ensure_range("area_total")
    ensure_range("floor")
    ensure_range("floors_total")

    # 7) walk_to_metro
    if f.get("walk_to_metro") not in (5,10,20,None):
        f["walk_to_metro"] = None
    if f.get("walk_to_metro") is None and hints.get("walk_to_metro") in (5,10,20):
        f["walk_to_metro"] = hints["walk_to_metro"]

    return data

def validate_and_fix_data(data: dict) -> dict:
    # weights
    if "weights" not in data or not isinstance(data["weights"], dict):
        data["weights"] = {k: 1.0/len(INFRA) for k in INFRA}
    else:
        data["weights"] = renorm_weights(data["weights"])

    # filters
    if "filters" not in data or not isinstance(data["filters"], dict):
        data["filters"] = {
            "deal_type": "Продажа",
            "market_type": "Не указано",
            "property_type": "Квартира",
            "rooms": "2",
            "price": {"currency": "RUB", "from": None, "to": None},
            "area_total": {"from": None, "to": None},
            "walk_to_metro": None,
            "floor": {"from": None, "to": None},
            "floors_total": {"from": None, "to": None},
        }

    # why
    if "why" not in data or not isinstance(data["why"], list):
        data["why"] = []

    return data
