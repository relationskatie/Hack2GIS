import re
from .heuristics import preparse_hints
from .groq_api import call_groq
from .normalize import renorm_weights, sanitize_filters, validate_and_fix_data
from .schemas import Output

def parse_user(user_text: str) -> Output:
    hints = preparse_hints(user_text)
    data = call_groq(user_text, hints)

    # нормализация весов и фильтров
    data["weights"] = renorm_weights(data.get("weights", {}))
    data = sanitize_filters(data, hints)

    # неявное правило: школьники → rooms >= 3
    if re.search(r"школьник", user_text.lower()):
        rooms = str(data["filters"]["rooms"])
        if rooms.isdigit() and int(rooms) < 3:
            data["filters"]["rooms"] = "3"

    data = validate_and_fix_data(data)

    if data["filters"]["walk_to_metro"] not in (5,10,20,None):
        data["filters"]["walk_to_metro"] = None

    return Output(**data)
