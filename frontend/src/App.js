import React, { useState } from 'react';
import { Static } from './Static';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [properties, setProperties] = useState([]);
  const [infra, setInfra] = useState([]); // добавили infra
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/find_homes?promt=${encodeURIComponent(query)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ promt: query }),
      });

      if (!response.ok) throw new Error(`Ошибка: ${response.status}`);

      const data = await response.json();

      const homesArray = Array.isArray(data.aparts) ? data.aparts : [];
      setProperties(homesArray);

      const infraArray = Array.isArray(data.infra) ? data.infra : [];
      setInfra(infraArray); // сохраняем infra

      setSubmitted(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="header" style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '20px', fontWeight: '600', color: '#333', margin: '0', fontFamily: 'Poppins, sans-serif', lineHeight: '1.4', paddingTop: '15px', paddingBottom: '10px', paddingLeft: '15px', backgroundColor: 'white', marginBottom: '20px' }}>
        <img src="/logo.svg" alt="Логотип" className="logo" style={{ width: '70px', height: '40px' }} />
        <span>Ассистент по подбору недвижимости</span>
      </div>

      {!submitted && (
        <form onSubmit={handleSubmit} style={{ padding: '0 15px', marginBottom: '20px' }}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Введите запрос..."
            style={{
              padding: '10px 15px',
              width: '300px',
              border: '1px solid #ccc',
              borderRadius: '6px',
              outline: 'none',
              fontSize: '16px',
              transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
            }}
            onFocus={(e) => {
              e.currentTarget.style.borderColor = '#00B14F';
              e.currentTarget.style.boxShadow = '0 0 5px rgba(0, 177, 79, 0.5)';
            }}
            onBlur={(e) => {
              e.currentTarget.style.borderColor = '#ccc';
              e.currentTarget.style.boxShadow = 'none';
            }}
          />

          <button
            type="submit"
            style={{
              backgroundColor: '#00B14F', 
              color: '#ffffff',           
              fontWeight: 600,
              fontSize: '16px',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '6px',        
              cursor: 'pointer',
              transition: 'background-color 0.2s ease',
            }}
            onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#009D44')} 
            onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#00B14F')}
          >
            Найти
          </button>
        </form>
      )}

      {loading && <p style={{ padding: '0 15px' }}>Загрузка...</p>}
      {error && <p style={{ padding: '0 15px', color: 'red' }}>{error}</p>}

      {submitted && !loading && properties.length > 0 && (
        <Static properties={properties} infra={infra} />
      )}
      {submitted && !loading && properties.length === 0 && <p style={{ padding: '0 15px' }}>Нет квартир по вашему запросу</p>}
    </div>
  );
}

export default App;
