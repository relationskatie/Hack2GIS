def convert_filters(model_output: dict) -> dict:
    """
    Конвертирует JSON модели (весь объект или только model_output['filters'])
    в формат, который ожидает backend (строковые ID и парные диапазоны).
    """

    # ---- Справочники соответствий (ключи — в нижнем регистре) ----
    ROOM_MAP = {
        "студия": "12131033236211716902",
        "1": "4181700697707238747",
        "2": "9052824901306559087",
        "3": "14883364286970164480",
        "4": "17507441855720051719",
        "5+": "4391054652267765575",
    }

    PROPERTY_MAP = {
        "квартира": "1067258717690367200",
        "дом": "1960994683134433681",
        "комната": "18041730938540801786",
    }

    MARKET_MAP = {
        "вторичка": "9675346827583075308",
        "новостройка": "9351055689598387066",
    }

    CATEGORY_MAP = {
        "продажа": "70241201812761646",
        "аренда": "70241201812768719",
    }

    # ---- Достаём секцию filters (поддержка обоих случаев входа) ----
    model_filters = model_output.get("filters", model_output)

    def _norm_s(s):
        if s is None:
            return None
        return str(s).strip().lower().replace("ё", "е")

    def _pair_str(r: dict | None) -> str:
        """
        Преобразует диапазон вида {"from_": X, "to": Y} или {"from": X, "to": Y}
        в строку "X,Y" (пустые значения заменяются на "").
        """
        r = r or {}
        f = r.get("from_", r.get("from"))
        t = r.get("to")
        f = "" if f is None else f
        t = "" if t is None else t
        return f"{f},{t}"

    filters: dict = {}

    # ---- Тип сделки -> category_ids ----
    deal_type = model_filters.get("deal_type")
    if deal_type:
        cat_id = CATEGORY_MAP.get(_norm_s(deal_type))
        if cat_id:
            filters["category_ids"] = cat_id

    # ---- Цена -> "price": "from,to" ----
    price = model_filters.get("price", {})
    filters["price"] = _pair_str(price) if price else " ,"

    # ---- Кол-во комнат -> "komnat": "id1,id2,..." ----
    rooms = model_filters.get("rooms")
    room_ids: list[str] = []
    if rooms:
        # Поддержка "1–2" / "1-2" / одиночных значений
        if isinstance(rooms, str):
            raw = rooms.replace("–", "-")  # en dash -> hyphen
            parts = [p.strip() for p in raw.split("-") if p.strip()]
        elif isinstance(rooms, (list, tuple)):
            parts = [str(p).strip() for p in rooms]
        else:
            parts = [str(rooms).strip()]

        for p in parts:
            key = _norm_s(p)
            rid = ROOM_MAP.get(key)
            if rid:
                room_ids.append(rid)

        if room_ids:
            filters["komnat"] = ",".join(room_ids)

    # ---- Тип недвижимости -> "tip_pomeshcheniya" ----
    property_type = model_filters.get("property_type")
    if property_type:
        prop_id = PROPERTY_MAP.get(_norm_s(property_type))
        if prop_id:
            filters["tip_pomeshcheniya"] = prop_id

    # ---- Тип рынка -> "new_building" ----
    market_type = model_filters.get("market_type")
    if market_type:
        market_id = MARKET_MAP.get(_norm_s(market_type))
        if market_id:
            filters["new_building"] = market_id

    # ---- Общая площадь -> "obshchaya_ploshchad": "from,to" ----
    filters["obshchaya_ploshchad"] = _pair_str(model_filters.get("area_total"))

    # ---- Этаж -> "etazh": "from,to" ----
    filters["etazh"] = _pair_str(model_filters.get("floor"))

    # ---- Этажей в доме -> "etazhey_v_dome": "from,to" ----
    filters["etazhey_v_dome"] = _pair_str(model_filters.get("floors_total"))

    # ---- Пешком до метро -> "metro_time": "0,<X>" (если известно), иначе дефолт "0,10"
    walk = model_filters.get("walk_to_metro")
    if isinstance(walk, (int, float)) and walk in (5, 10, 20):
        filters["metro_time"] = f"0,{int(walk)}"
    else:
        filters.setdefault("metro_time", "0,10")

    return filters
