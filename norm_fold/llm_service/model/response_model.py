import json
from .parser import parse_user
from .convert import convert_filters

def main_parse(promt: str):
    # пример: медицинские потребности + продукты рядом
    try:
        out = parse_user(promt)              # -> Output (Pydantic)
        #backend_filters = convert_filters(out.model_dump())  # <<< вот так
        #print(json.dumps(backend_filters, ensure_ascii=False, indent=2))
        return out

        # print(json.dumps(out.model_dump(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ Ошибка: {e}")
