<p align="center">
  <img src="https://via.placeholder.com/1200x400/0F172A/0EA5E9?text=Pesca+App+-+Tabla+de+Mareas+y+Pron%C3%B3stico+de+Pesca" alt="Banner" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.0-blue?style=for-the-badge" alt="Flask"/>
  <img src="https://img.shields.io/badge/PRs-welcome-orange?style=for-the-badge" alt="PRs Welcome"/>
</p>

## 🌊 Descripción

**Pesca App** es una aplicación web de tablas de mareas, clima y pronóstico de pesca diseñado para pescadores recreativos y profesionales. Permite consultar las mejores condiciones de pesca basadas en mareas, fases lunares, clima y temperatura del mar.

### 🌐 Demo en Vivo

👉 **[pesca-app.onrender.com](https://pesca-app.onrender.com)** (En proceso de deployment)

> Nota: Si el enlace no funciona, ejecutar localmente (ver instrucciones abajo).

---

## 📸 Capturas de Pantalla

### Página Principal - Pronóstico de Hoy
<p align="center">
  <img src="https://via.placeholder.com/800x500/1E293B/0EA5E9?text=Principal+-+Pron%C3%B3stico+de+Pesca" alt="Principal" width="100%"/>
</p>

### Tabla Semanal de Mareas
<p align="center">
  <img src="https://via.placeholder.com/800x500/1E293B/0EA5E9?text=Tabla+Semanal+de+Mareas" alt="Semanal" width="100%"/>
</p>

### Mejores Horarios de Pesca
<p align="center">
  <img src="https://via.placeholder.com/800x500/1E293B/0EA5E9?text=Mejores+Horarios+de+Pesca" alt="Horarios" width="100%"/>
</p>

### Clima y Mapa
<p align="center">
  <img src="https://via.placeholder.com/800x500/1E293B/0EA5E9?text=Clima+y+Mapa+Interactivo" alt="Clima" width="100%"/>
</p>

---

## ✨ Características

| Característica | Descripción |
|----------------|------------|
| 🌊 **Tabla de Mareas** | Predicciones de pleamar y bajamar con horas y alturas |
| 🌤️ **Clima** | Temperatura, viento, humedad y presión atmosférica |
| 🌡️ **Temperatura del Mar** | Datos de temperatura marina en tiempo real |
| 🌙 **Fase Lunar** | Iluminación lunar y tipo de luna actual |
| 🎣 **Score de Pesca** | Algoritmo 1-10 basado en múltiples factores |
| ⭐ **Mejores Horarios** | Periodos óptimos de pesca (major/minor) |
| 📍 **Búsqueda** | Por ciudad, coordenadas o GPS |
| 🗺️ **Mapa Interactivo** | Visualización de ubicación con Leaflet |
| 📱 **Diseño Responsive** | Adaptado para móvil, tablet y desktop |

---

## 🛠️ Tecnologías

- **Backend**: Python 3.12 + Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Mapas**: Leaflet.js + OpenStreetMap
- **APIs**: NOAA CO-OPS, Open-Meteo, Nominatim, ipapi.co
- **Astronomía**: Skyfield (cálculos lunares)

---

## 🚀 Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/oscaromargp/pesca-app.git
cd pesca-app

# 2. Crear entorno virtual (opcional)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python app.py
```

Acceder a: **http://localhost:5000**

---

## 📡 API Endpoints

| Endpoint | Descripción | Ejemplo |
|----------|------------|---------|
| `/` | Página principal | - |
| `/api/forecast?lat=&lon=` | Pronóstico completo | [Link](https://pesca-app.onrender.com/api/forecast?lat=24.142&lon=-110.310) |
| `/api/geocode?q=` | Geocodificar ciudad | `/api/geocode?q=La+Paz` |
| `/api/tides?lat=&lon=` | Solo mareas | `/api/tides?lat=24.142&lon=-110.310` |
| `/api/weather?lat=&lon=` | Solo clima | `/api/weather?lat=24.142&lon=-110.310` |

### Respuesta de `/api/forecast`

```json
{
  "location": {
    "lat": 24.142,
    "lon": -110.31,
    "city": "La Paz",
    "country": "México"
  },
  "fishing_score": 7.5,
  "fishing_context": "Excelentes condiciones para pesca hoy.",
  "tide_coefficient": 75,
  "tides": {
    "station": "La Paz",
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
  "marine": {
    "water_temperature": 22,
    "wave_height": 0.5
  },
  "solunar": {
    "moon_illumination": 0.72,
    "major_periods": ["06:30-08:30", "18:45-20:45"]
  }
}
```

---

## 🌍 Ciudades Soportadas

### México
- La Paz, BCS
- Mazatlán, Sinaloa
- Cabo San Lucas, BCS
- Ensenada, BC
- San Felipe, BC
- Guaymas, Sonora
- Manzanillo, Colima
- Cancún, QRoo
- Progreso, Yucatán
- Tampico, Tamaulipas
- Veracruz, Veracruz
- Tijuana, BC
- Acapulco, Guerrero

### Estados Unidos
- Miami, Florida
- Key West, Florida
- San Diego, California
- Santa Barbara, California

---

## 📊 Algoritmo de Score

El score de pesca (1-10) considera:

### Factores de Marea (0-3 puntos)
- Coeficiente de marea alto (>70): +2 puntos
- Amplitud de marea moderada: +1 punto

### Factores de Clima (0-3 puntos)
- Viento calma (<10 km/h): +1.5 puntos
- Sin precipitación: +1 punto
- Nubosidad 30-70%: +0.5 puntos

### Factores Solunares (0-4 puntos)
- Rating solunar: (rating - 3) * 0.8
- Iluminación lunar 40-60%: +0.5 puntos

---

## 🤝 Contribuir

1. Fork del repositorio
2. Crear branch (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agrega nueva característica'`)
4. Push al branch (`git push origin feature/nueva-caracteristica`)
5. Abrir Pull Request

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

Inspirado y basado en el trabajo de:

| Proyecto | Descripción |
|----------|--------------|
| [tidewise](https://github.com/AreteDriver/tidewise) | Algoritmo de scoring de pesca |
| [solunarbass](https://github.com/bassfinity/solunarbass) | Cálculos solunares |
| [Fishing-Report-Analyzer](https://github.com/seang1121/Fishing-Report-Analyzer) | Multi-API approach |
| [tablademareas.com](https://tablademareas.com) | Referencia de UX/UI |
| [tideschart.com](https://es.tideschart.com) | Referencia de tablas de mareas |
| [fishingpoints.app](https://fishingpoints.app) | Referencia de pronósticos |

### APIs Utilizadas

- **NOAA CO-OPS** - Mareas y corrientes
- **Open-Meteo** - Clima y datos marinos
- **OpenStreetMap/Nominatim** - Mapas y geocodificación
- **ipapi.co** - Geolocalización por IP
- **Skyfield** - Cálculos astronómicos

---

## 👤 Autor

**Oscar Omar Gómez Peña**

- GitHub: [@oscaromargp](https://github.com/oscaromargp)
- Email: oscaromargp@gmail.com

### XRP (Donaciones)
```
Ripple: rM viEmN7yLnQt4CokKzXNBHmz5qL5tN5jW
BTC: 1F1z1j7Lq3W7K3K3K3K3K3K3K3K3K3K3K
ETH: 0x... (contactar para dirección)
```

---

<p align="center">
  <img src="https://img.shields.io/badge/hecho-con-❤️-por-oscaromargp-red?style=for-the-badge" alt="Hecho con ❤️"/>
</p>