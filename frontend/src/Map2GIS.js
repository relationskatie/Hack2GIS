import React, { useEffect, useRef } from 'react';
import { load } from '@2gis/mapgl';

const API_KEY = '2d952543-cd26-4a9b-9aa9-ffa59a0000a3';
const GEOCODE_URL = 'https://catalog.api.2gis.com/3.0/items/geocode';

export const Map2GIS = ({ value }) => {
  const mapRef = useRef(null);
  const mapglAPIRef = useRef(null);
  const mainMarkerRef = useRef(null);
  const infraMarkersRef = useRef([]);

  // Инициализация карты
  useEffect(() => {
    let isMounted = true;

    load().then((mapglAPI) => {
      if (!isMounted) return;

      mapglAPIRef.current = mapglAPI;

      mapRef.current = new mapglAPI.Map('map-container', {
        center: [37.618423, 55.751244],
        zoom: 13,
        key: API_KEY,
      });
    });

    return () => {
      isMounted = false;
      mapRef.current && mapRef.current.destroy();
    };
  }, []);

  // Получение координат по адресу
  const fetchCoords = async (address) => {
    try {
      const query = `Москва, ${address}`;
      const url = `${GEOCODE_URL}?q=${encodeURIComponent(query)}&fields=items.point&key=${API_KEY}`;

      const response = await fetch(url);
      const data = await response.json();
      const point = data?.result?.items?.[0]?.point;

      if (point?.lat && point?.lon) {
        return [point.lon, point.lat];
      }
    } catch (err) {
      console.error('Ошибка геокодинга:', err);
    }
    return null;
  };

  useEffect(() => {
    if (!mapRef.current || !mapglAPIRef.current || !value) return;

    const mapInstance = mapRef.current;
    const mapglAPI = mapglAPIRef.current;

    // Удаляем предыдущие маркеры
    if (mainMarkerRef.current) mainMarkerRef.current.destroy();
    infraMarkersRef.current.forEach(marker => marker.destroy());
    infraMarkersRef.current = [];

    console.log('Infra Array:', value.infra);

    // Главный маркер
    if (value.address) {
      fetchCoords(value.address).then((coords) => {
        if (coords) {
          mainMarkerRef.current = new mapglAPI.Marker(mapInstance, {
            coordinates: coords,
            color: '#ff0000',
            icon: '/home.svg',
            size: [35, 35],
          });
          mapInstance.setCenter(coords);
        }
      });
    }

    // Инфраструктура
    if (value.map) {
      Object.entries(value.map).forEach(([key, places]) => {
        if (!Array.isArray(places)) return;

        places.forEach(async (place) => {
          const address = place?.address_name;
          if (!address) return;

          const coords = await fetchCoords(address);
          if (!coords) return;

          const icon = getIconByKey(key, value.infra);

          const marker = new mapglAPI.Marker(mapInstance, {
            coordinates: coords,
            color: '#0000ff',
            icon: icon,
            size: [35, 35],
          });
          infraMarkersRef.current.push(marker);
        });
      });
    }
  }, [value]);

  return (
    <div
      id="map-container"
      style={{ width: '100%', height: '600px' }}
    ></div>
  );
};

const getIconByKey = (key, infraArray) => {
  const baseIcons = {
    'Продукты': '/products.svg',
    'Школы': '/school.svg',
    'Детские сады': '/kindergarten.svg',
    'Медицина': '/hospital.svg',
    'Аптеки': '/farma.svg',
    'Спорт': '/sport.svg',
    'Культура': '/culture.svg',
    'Бары': '/bar.svg',
  };

  console.log('Infra Array:', infraArray, 'Key:', key);

  if (Array.isArray(infraArray) && infraArray.length > 0) {
    if (infraArray.includes(key)) {
      console.log(`${key} найден в массиве, используем иконку с "1"`);
      return baseIcons[key].replace('.svg', '1.svg');
    }
  }

  console.log(`${key} не найден в массиве, используем стандартную иконку`);
  return baseIcons[key] || null;
};


