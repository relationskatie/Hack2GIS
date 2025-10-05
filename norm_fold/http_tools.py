import requests
import random
import time
def clean_filters(filters: dict) -> dict:
    cleaned = {}
    for key, value in filters.items():
        # убираем None, пустые строки и строки вида "," или ",,"
        if value and str(value).strip(",") != "":
            cleaned[key] = value
    return cleaned

def build_realty_urls(filters):
    """
    Формирует URL для запроса недвижимости по районам Москвы используя geo_id

    Args:
        filters (dict): Словарь с параметрами фильтрации
    """
    # Районы Москвы с geo_id
    moscow_districts = [
        "geo_id=4504385606390700",  # Люблино
        "geo_id=4504385606385733",  # Китай-город
        "geo_id=4504235282734895",  # Тверской район
        "geo_id=4504209512726634",  # Кунцево
        "geo_id=4504209512726615",  # Чертаново
        "geo_id=4504209520926899",  # Комунарка
        "geo_id=4504209512726620",  # Ясенево
        "geo_id=4504209512726555",  # Ховрино
        "geo_id=4504235282961042",  # Митино
        "geo_id=4504235282573467",  # Коньково
    ]

    filters = clean_filters(filters)



    urls = []

    for district in moscow_districts:
        # Базовые параметры по умолчанию
        required_filters = {
            "platform_code": "34",
            "page": "1",
            "locale": "ru_RU",
            "page_size": "20",
            "point1": "37.49627352524681,55.6601232496663",
            "point2": "37.56688047475319,55.62146669509174"
        }

        # Добавляем geo_id района
        district_param = district.split('=')
        required_filters[district_param[0]] = district_param[1]

        # Объединяем с пользовательскими фильтрами
        params = {**required_filters, **filters}

        # Формируем строку запроса, исключая параметры со значением None
        query_params = []
        for key, value in params.items():
            if value is not None:
                query_params.append(f"{key}={value}")

        # Собираем конечный URL
        base_url = "https://market-backend.api.2gis.ru/5.0/realty/items"
        query_string = "&".join(query_params)

        urls.append(f"{base_url}?{query_string}")

    return urls


def fetch_data(urls: list[str]) -> list[dict]:
    """
    Делает запросы к 2GIS API, получает данные и возвращает случайные объявления.
    """
    homes = []
    homes_for_front = []

    for url in urls:
        # Пауза, чтобы не спамить API
        time.sleep(1)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # выбросит исключение при ошибке HTTP
        except requests.RequestException as e:
            print(f"⚠ Ошибка при запросе {url}: {e}")
            continue  # пропускаем неудачный запрос

        data = response.json()
        result = data.get("result", {})
        items = result.get("items", [])

        if not items:
            print(f"⚠ Нет данных для {url}")
            continue

        # Берём случайный элемент из списка
        random_item = random.choice(items)

        product = random_item.get("product", {})
        offer = random_item.get("offer", {})
        building = random_item.get("building", {})

        lat = building.get("lat")
        lon = building.get("lon")

        homes.append({
            "id": product.get("id"),
            "name": product.get("name"),
            "description": product.get("description"),
            "attributes": product.get("attributes", []),
            "images": product.get("images", []),
            "lat": lat,
            "lon": lon,
            "url": offer.get("url")
        })


        name = product.get("name")
        description = product.get("description")
        attributes = product.get("attributes", [])
        for attr in attributes:
            caption = attr.get("caption", "")
            value = attr.get("value", "")
            cntrooms = ""
            square = ""
            floor = ""

            if caption == "Количество комнат":
                cntrooms = value
            elif caption == "Общая площадь":
                square = value
            elif caption == "Этаж":
                floor = value
        images = product.get("images", [])
        url = offer.get("url")
        price = offer.get("price_value").get("fixed").get("value")
        price_per_meter_value = offer.get("price_per_meter_value").get("fixed").get("value")

        address = building.get("address_name")
        station =building.get("links").get("nearest_stations")[0].get("name")
        lat = building.get("lat")
        lon = building.get("lon")

        home_for_front = {
            "name": name,
            "description": description,
            "cntrooms": cntrooms,
            "square": square,
            "floor": floor,
            "images": images,
            "url": url,
            "price": price,
            "priceForMetr": price_per_meter_value,
            "address": address,
            "station": station,
            "lat": lat,
            "lon": lon,
            "map": {
                "Продукты": [],
                "Школы": [],
                "Детские сады": [],
                "Медицина": [],
                "Аптеки": [],
                "Спорт": [],
                "Культура": [],
                "Бары": []
            }
        }

        homes_for_front.append(home_for_front)



    return {"homes": homes, "homes_for_front": homes_for_front}
