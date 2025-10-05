import re
from typing import Optional

# — извлекаем максимум сигналов, чтобы снизить одинаковость ответов
_BUDGET_RE = re.compile(
    r"(?:до|не более|<=|в пределах)\s*([\d\s]+)(?:\s*тыс|\s*т\.?р\.?|k)?|\b([\d]{2,3})\s*к\b",
    re.IGNORECASE
)

def _parse_budget(text: str) -> Optional[int]:
    """
    Извлекает верхнюю границу бюджета в RUB/мес. для аренды: «до 40 тыс», «в пределах 35к», «<= 45 000».
    Возвращает число в рублях, если найдено.
    """
    t = text.lower().replace(" ", " ").replace("\u00A0", " ")
    m = _BUDGET_RE.search(t)
    if not m:
        return None
    num = m.group(1) or m.group(2)
    if not num:
        return None
    num = re.sub(r"[^\d]", "", num)
    if not num:
        return None
    val = int(num)
    # эвристика: если похоже на "к" (тыс) — домножим
    if val < 1000:
        val *= 1000
    return val

def preparse_hints(text: str) -> dict:
    """
    Собираем богатый набор подсказок (persona, бюджет, интересы, WFH, метро, продукты, медицина).
    Это уменьшает «одинаковость» ответов и даёт модели больше контекста.
    """
    t = text.lower()
    hints = {}

    # сделка
    if any(w in t for w in ["купить","покупк","приобрест"]): hints["deal_type"]="Продажа"
    if any(w in t for w in ["снять","аренд","рент"]): hints["deal_type"]="Аренда"

    # пешком до метро
    if "5 минут пешком" in t: hints["walk_to_metro"]=5
    elif "10 минут пешком" in t or "рядом с метро" in t or "в пешей доступности" in t: hints["walk_to_metro"]=10
    elif "20 минут пешком" in t: hints["walk_to_metro"]=20
    else:
        # t минут → 5/10/20
        m = re.search(r"(\d{1,2})\s*мин(ут|)\b", t)
        if m:
            mins = int(m.group(1))
            if mins <= 7: hints["walk_to_metro"] = 5
            elif 8 <= mins <= 14: hints["walk_to_metro"] = 10
            elif 15 <= mins <= 25: hints["walk_to_metro"] = 20

    # бюджет (для аренды)
    budget = _parse_budget(t)
    if budget:
        hints["price_to"] = budget

    # профили/персоны
    if re.search(r"(молод(ая|ые)\s+семь|молодожен)", t):
        hints["persona"] = "young_family"
    elif re.search(r"(школьник|школьниками|школьного возраста)", t):
        hints["persona"] = "family_school"
    elif re.search(r"(детский сад|садик|дошкол)", t):
        hints["persona"] = "family_preschool"
    elif re.search(r"(студент|стажер|интернат|учусь|университет|вуз|магистр|бакалавр)", t):
        hints["persona"] = "student"
    elif re.search(r"(дедушк|бабушк|пенсионер|пожил(ая|ые|ой))", t):
        hints["persona"] = "elderly"
    elif re.search(r"(it|айти|программист|разработчик|data|аналитик|работаю из дома|удаленк)", t):
        hints["persona"] = hints.get("persona","it_remote")

    # интересы/факторы (влияют на weights + объяснения)
    interests = []
    if re.search(r"(спорт|тренаж|фитнес|бассейн|зал)", t): interests.append("sport")
    if re.search(r"(музе|театр|выстав|культур)", t): interests.append("culture")
    if re.search(r"(бар|пив|кафе|ночн|развлечен)", t): interests.append("bars")
    if re.search(r"(продукт|магазин|супермаркет)", t): interests.append("groceries")
    if re.search(r"(поликлиник|больниц|здоров|кардио|сердц|аптек)", t): interests.append("medical")
    if re.search(r"(работаю из дома|удаленк|home\s*office|wfh)", t): interests.append("wfh")

    if interests:
        hints["interests"] = interests

    # размер жилья (одно/небольшое)
    if re.search(r"(небольш(ая|ое)|компактн|для одного|одному|сам)", t):
        hints["pref_small"] = True

    return hints
