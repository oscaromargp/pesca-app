# 🎣 Pesca App

![Docker](https://img.shields.io/docker/pulls/oscaromargp/pesca-app)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

App de pesca que combina clima, mareas, corrientes y pronóstico de pesca en una sola interfaz. Diseño Dark Premium con glassmorphism.

---

## 📸 Screenshots

### Homepage
![Pesca App Homepage](https://via.placeholder.com/800x450/000000/22D3EE?text=Pesca+App+Homepage)

### Dashboard - Pronóstico
![Dashboard](https://via.placeholder.com/800x450/000000/22D3EE?text=Dashboard+pron%C3%B3stico+de+pesca)

### Mapa
![Mapa](https://via.placeholder.com/800x450/000000/22D3EE?text=Mapa+de+mareas+y+corrientes)

---

## ✨ Características

- 🌊 **Mareas**: Predicciones de mareas usando NOAA CO-OPS API
- 🌤️ **Clima**: Pronóstico del tiempo con Open-Meteo
- 🌙 **Solunar**: Cálculos de fases lunares y periodos de pesca óptimos
- 📍 **Ubicación**: Detección automática por IP o entrada manual de coordenadas
- 🗺️ **Mapa**: Visualización con Leaflet.js
- ⭐ **Score de Pesca**: Algoritmo 1-10 basado en múltiples factores
- 🎨 **Diseño Dark Premium**: Glassmorphism, animaciones, gradientes

---

## 🛠️ Tecnologías

| Tecnología | Propósito |
|------------|----------|
| Flask | Servidor backend |
| JavaScript | Frontend e interactividad |
| Leaflet.js | Mapas interactivos |
| NOAA CO-OPS API | Mareas y corrientes |
| Open-Meteo | Clima |
| Skyfield | Cálculos astronómicos |
| ipapi.co | Geolocalización |

---

## 🚀 Deployment

### Render (Recomendado)

部署 a Render con un clic:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/oscaromargp/pesca-app)

O manual:

1. Ir a [dashboard.render.com](https://dashboard.render.com)
2. Crear nuevo **Web Service**
3. Conectar repositorio GitHub
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Python Version: 3.12
5. Deploy

### Local

```bash
# Clonar
git clone https://github.com/oscaromargp/pesca-app.git
cd pesca-app

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

Acceder a: `http://localhost:5000`

### Docker

```bash
docker build -t pesca-app .
docker run -p 5000:5000 pesca-app
```

---

## 📡 APIs

### Endpoint Principal

```
GET /api/forecast?lat=25.7617&lon=-80.1918
```

**Respuesta:**

```json
{
  "location": {
    "lat": 25.7617,
    "lon": -80.1918,
    "city": "Miami",
    "country": "United States"
  },
  "fishing_score": 7.5,
  "tides": {
    "station": "Virginia Key",
    "tides": [
      {"time": "2024-01-15 06:42", "type": "high", "height": 2.1},
      {"time": "2024-01-15 13:15", "type": "low", "height": 0.3}
    ]
  },
  "weather": {
    "temperature": 24,
    "wind_speed": 12,
    "humidity": 65,
    "pressure": 1015
  },
  "solunar": {
    "moon_phase": 0.72,
    "solunar_rating": 4,
    "major_periods": ["06:30-08:30", "18:45-20:45"]
  }
}
```

### Otros Endpoints

| Endpoint | Descripción |
|---------|------------|
| `/api/tides?lat=&lon=` | Solo mareas |
| `/api/weather?lat=&lon=` | Solo clima |
| `/` |Página principal |

---

## 📁 Estructura

```
pesca/
├── app.py              # Servidor Flask
├── requirements.txt   # Dependencias Python
├── Procfile           # Render config
├── render.yaml        # Render YAML
├── runtime.txt        # Python version
├── README.md         # Este archivo
├── static/
│   ├── index.html   # Frontend
│   ├── app.js      # JavaScript
│   └── style.css   # Estilos
└── src/
    ├── __init__.py
    ├── utils.py      # Ubicación y score
    ├── tides.py     # NOAA API
    ├── weather.py  # Open-Meteo
    └── solunar.py  # Cálculos lunares
```

---

## 📊 Algoritmo de Score

El score de pesca (1-10) se calcula considerando:

### Factores de Marea (0-3 puntos)
- Marea entrante: +1.5 puntos
- Altura > 0.5m: +1.0 punto

### Factores de Clima (0-3 puntos)
- Viento < 10 km/h: +1.5 puntos
- Viento < 20 km/h: +0.5 puntos
- Precipitación < 0.5mm: +1.0 punto
- Nubosidad 30-70%: +0.5 puntos

### Factores Solunares (0-4 puntos)
- Rating solunar: (rating - 3) * 0.8
- Iluminación lunar 40-60%: +0.5 puntos

---

## 🔧 Desarrollo

### Scripts útiles

```bash
# Debug local
flask run --debug

# Test API
curl http://localhost:5000/api/forecast

# Test con coordenadas
curl "http://localhost:5000/api/forecast?lat=25.7617&lon=-80.1918"
```

### Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| PORT | 5000 | Puerto del servidor |
| FLASK_ENV | development | Modo Flask |

---

## 📝 Licencia

MIT License - Voir [LICENSE](LICENSE)

---

## 🙏 Créditos

Inspirado en:
- [tidewise](https://github.com/AreteDriver/tidewise) - Algoritmo de scoring
- [solunarbass](https://github.com/bassfinity/solunarbass) - Cálculos solunares
- [Fishing-Report-Analyzer](https://github.com/seang1121/Fishing-Report-Analyzer) - Multi-API approach