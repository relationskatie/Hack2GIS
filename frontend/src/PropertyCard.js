import React from 'react';
import './PropertyCard.css'; 

export const PropertyCard = ({ property, onClick }) => {
  return (
    <div className="property-card" onClick={onClick}>
      <h2 className="property-name">{property.name}</h2>
      <p className="property-description">{property.description}</p>
      <p>
  <strong>Комнат:</strong>{" "}
  {property.cntrooms === 1
    ? "1 комната"
    : property.cntrooms >= 2 && property.cntrooms <= 4
    ? `${property.cntrooms} комнаты`
    : "5+ комнат"}
</p>
      <p><strong>Площадь:</strong> {property.square} м²</p>
      <p><strong>Этаж:</strong> {property.floor}</p>
      <p><strong>Адрес:</strong> {property.address}</p>
      <p><strong>Ближайшая станция метро:</strong> {property.station}</p>
      <p><strong>Цена:</strong> {property.price.toLocaleString()} ₽</p>
      <p><strong>Цена за м²:</strong> {property.priceForMetr.toLocaleString()} ₽/м²</p>

      <div className="images">
        {property.images.map((img, idx) => (
          <img key={idx} src={img} alt={`Фото ${idx + 1}`} />
        ))}
      </div>

  

      <p>
        <a className="property-link" href={property.url} target="_blank" rel="noopener noreferrer">
          Смотреть на сайте
        </a>
      </p>
    </div>
  );
};
