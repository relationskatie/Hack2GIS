import requests
import time

CATEGORIES = [
    "Продукты",
    "Школы",
    "Детские сады",
    "Медицина",
    "Аптеки",
    "Спорт",
    "Культура",
    "Бары",
]

API_URL = "https://catalog.api.2gis.com/3.0/items"
API_KEY = "8f104049-075f-4c47-817b-b8b450854d86"  # 🔑 сюда подставь свой ключ 2GIS


def count_nearby_places(homes: list[dict], homes_for_front):
    print(len(homes), len(homes_for_front), "%%%")
    print(homes_for_front)
    """
    Для каждой квартиры считает, сколько объектов каждой категории
    находится поблизости (радиус 1 км).
    """
    result_map = {}

    for i in range(len(homes)):
        home = homes[i]
        lat = home.get("lat")
        lon = home.get("lon")
        url = home.get("url") or "unknown"

        if not lat or not lon:
            print(f"⚠ Пропущены координаты для: {url}")
            continue

        category_counts = {}

        for category in CATEGORIES:
            params = {
                "q": category,
                "point": f"{lon},{lat}",  
                "radius": 1000,
                "location": f"{lon},{lat}",
                "sort": "distance",
                "key": API_KEY,
                "locale": "ru_RU"
            }

            try:
                response = requests.get(API_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                total = data.get("result", {}).get("total", 0)
                items = data.get("result", {}).get("items")
                print(items)

                category_counts[category] = total

                # Безопасно берем первый элемент если он есть
                if items:
                    catgrs = [item for item in items]
                    if len(catgrs) > 3:
                        homes_for_front[i]["map"][category] = [catgrs[0], catgrs[1], catgrs[2]]
                    elif len(catgrs) == 2:
                        homes_for_front[i]["map"][category] = [catgrs[0], catgrs[1]]
                    elif len(catgrs) == 1:
                        homes_for_front[i]["map"][category] = [catgrs[0]]
                    #homes_for_front[i]["map"][category]["points"] =

                else:
                    homes_for_front[i]["map"][category] = None  # или пустой словарь {}

            except requests.RequestException as e:
                print(f"⚠ Ошибка при запросе категории {category}: {e}")
                category_counts[category] = 0

            # Небольшая пауза, чтобы не попасть под rate limit
            time.sleep(0.3)

        result_map[url] = category_counts

    return {"result_map": result_map, "homes_for_front": homes_for_front}
