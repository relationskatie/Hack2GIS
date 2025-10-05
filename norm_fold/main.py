from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model_parse_promt.parse_promt import parse_promt_to_filters
from http_tools import build_realty_urls, fetch_data
from api_tools import count_nearby_places
from llm_service.model.response_model import main_parse
from llm_service.sort_function import sort_function
from llm_service.model.convert import convert_filters


app = FastAPI(title="Simple FastAPI Server")


origins = [
    "http://localhost:3000",  # React
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",
    "*"  # ⚠️ Можно разрешить все (но не рекомендуется в продакшне)
]

# Подключаем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # откуда разрешены запросы
    allow_credentials=True,         # разрешить куки и авторизацию
    allow_methods=["*"],            # разрешить все методы (GET, POST, и т.д.)
    allow_headers=["*"],            # разрешить все заголовки
)



@app.get("/")
def root():
    return {"message": "Сервер работает!"}


@app.post("/find_homes")
def find_homes(promt: str):
    out_parse = main_parse(promt)
    out_dict = out_parse.model_dump()

    weights = out_dict.get("weights", out_dict)
    filters = convert_filters(out_dict)

    print(weights, filters)

    urls = build_realty_urls(filters)
    for url in urls:
        print(url)
    homes = fetch_data(urls)
    homes_for_front = homes["homes_for_front"]
    homes = homes["homes"]
    #print(homes)

    mapa = count_nearby_places(homes, homes_for_front)
    homes_for_front = mapa["homes_for_front"]
    mapa = mapa["result_map"]
    print(filters)

    sorted_homes = sort_function(weights, mapa)
    weights_sorted = sorted_homes["weights_sorted"]
    print(weights_sorted, "###")

    print(sorted_homes["sorted_housing"])


    return {
        "infra": [weights_sorted[0], weights_sorted[1], weights_sorted[2]],
        "filters": out_dict.get("filters", out_dict),
        "aparts": homes_for_front
    }


# Пример POST-запроса
@app.post("/sum")
def calculate_sum(data: dict):
    a = data.get("a", 0)
    b = data.get("b", 0)
    return {"result": a + b}
