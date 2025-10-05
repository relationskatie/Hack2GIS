import React from 'react';
import {PropertyCard} from './PropertyCard';
import { Map2GIS } from './Map2GIS';
import { useState } from "react";
import './Static.css';




export const testProperties = [
    {
      name: "Квартира мечты",
      description: "Просторная квартира с видом на город, свежий ремонт.",
      cntrooms: 3,
      square: 85,
      floor: 5,
      images: [
        "https://images.cdn-cian.ru/images/2653186249-1.jpg",
        "https://images.cdn-cian.ru/images/2653186278-1.jpg",
                "https://images.cdn-cian.ru/images/2653186249-1.jpg",

      ],
      url: "https://example.com/property/1",
      price: 15000000,
      priceForMetr: 176470,
      address: "г. Москва, 2 кабельный проезд 4",
      station: "м. Парк Культуры",
      lat: 55.749212,
      lon: 37.714183,
      map: {
        "Продукты": [
          { name: "Пятёрочка", address: "ул. Ленина, 5", coords: [37.718388, 55.749504] }
        ],
        "Школы": [
          { name: "Школа №12", address: "ул. Ленина, 12", coords: [37.712168,55.749897] }
        ],
        "Детские сады": [],
        "Медицина": [],
        "Аптеки": [],
        "Спорт": [],
        "Культура": [],
        "Бары": [
          { name: "Бар Пятница", address: "ул. Ленина, 15", coords: [37.71643, 55.753461] }
        ]
      }
    },
    {
      name: "Современная студия",
      description: "Уютная студия в центре города, рядом метро и парки.",
      cntrooms: 1,
      square: 42,
      floor: 3,
      images: [
        "https://images.cdn-cian.ru/images/2653186290-1.jpg",
        "https://images.cdn-cian.ru/images/2653186312-1.jpg"
      ],
      url: "https://example.com/property/2",
      price: 8000000,
      priceForMetr: 190476,
      address: "г. Москва, ул. Новая, д. 7",
      station: "м. Тверская",
      lat: 55.750555,
      lon: 37.694254,
      map: {
        "Продукты": [
          { name: "Магнит", address: "ул. Новая, 5", coords: [37.615000, 55.756000] }
        ],
        "Школы": [],
        "Детские сады": [
          { name: "Детский сад №3", address: "ул. Новая, 8", coords: [37.616500, 55.757500] }
        ],
        "Медицина": [],
        "Аптеки": [
          { name: "Аптека Здоровье", address: "ул. Новая, 6", coords: [37.615500, 55.756500] }
        ],
        "Спорт": [
          { name: "Фитнес клуб Центр", address: "ул. Новая, 10", coords: [37.617000, 55.758000] }
        ],
        "Культура": [],
        "Бары": []
      }
    },
    {
      name: "Семейная квартира",
      description: "Просторная квартира для большой семьи, с детской комнатой и балконом.",
      cntrooms: 4,
      square: 110,
      floor: 8,
      images: [
        "https://images.cdn-cian.ru/images/2653186330-1.jpg",
        "https://images.cdn-cian.ru/images/2653186350-1.jpg"
      ],
      url: "https://example.com/property/3",
      price: 22000000,
      priceForMetr: 200000,
      address: "г. Москва, ул. Солнечная, д. 20",
      station: "м. Академическая",
      lat: 55.750555,
      lon: 37.694254,
      map: {
        "Продукты": [
          { name: "Перекрёсток", address: "ул. Солнечная, 18", coords: [37.630000, 55.740000] }
        ],
        "Школы": [
          { name: "Школа №45", address: "ул. Солнечная, 22", coords: [37.631000, 55.741000] }
        ],
        "Детские сады": [
          { name: "Детский сад №8", address: "ул. Солнечная, 21", coords: [37.630500, 55.740500] }
        ],
        "Медицина": [
          { name: "Поликлиника №12", address: "ул. Солнечная, 19", coords: [37.631500, 55.741500] }
        ],
        "Аптеки": [],
        "Спорт": [
          { name: "Спортзал Олимп", address: "ул. Солнечная, 23", coords: [37.632000, 55.742000] }
        ],
        "Культура": [
          { name: "ДК Солнечный", address: "ул. Солнечная, 25", coords: [37.632500, 55.742500] }
        ],
        "Бары": [
          { name: "Кафе Бар", address: "ул. Солнечная, 24", coords: [37.633000, 55.743000] }
        ]
      }
    }
  ];
  





  export function Static({ properties, infra }) {
    const [mapValue, setMapValue] = useState(null);
  
    const handlePropertyClick = (property) => {
      setMapValue({ ...property, infra });
    };
  
    return (
      <div className="static-container">
        <div className="properties-list scrollable">
          {properties.map((property, idx) => (
            <PropertyCard 
              key={idx} 
              property={property} 
              onClick={() => handlePropertyClick(property)} 
            />
          ))}
        </div>
        <div className="map-wrapper">
          <Map2GIS value={mapValue} />
        </div>
      </div>
    );
  }
  