import React from 'react';
import './MapSize.css'; // подключаем CSS
import PropertyCard from './PropertyCard';
import { Map2GIS } from './Map2GIS';


function MapSize() {
  return (
    <div className="container">
      
     
        <Map2GIS className="map"/>
      
      <PropertyCard property={testProperty}/>
    </div>
  );
}

export default MapSize;
