<p align="center">
  <img src="https://via.placeholder.com/1200x400/0F172A/0EA5E9?text=Pesca+App+-+Tabla+de+Mareas+y+Pron%C3%B3stico+de+Pesca" alt="Banner" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.0-blue?style=for-the-badge" alt="Flask"/>
  <img src="https://img.shields.io/badge/PRs-welcome-orange?style=for-the-badge" alt="PRs Welcome"/>
  <img src="https://img.shields.io/badge/hecho-con-%E2%9D%A4%EF%B8%8F-red?style=for-the-badge" alt="Made with love"/>
</p>

---

## 📖 Descripción

**Pesca App** es una aplicación web de tablas de mareas, clima y pronóstico de pesca diseñado para pescadores recreativos y profesionales en México y Latinoamérica.

### ¿Cuál fue mi motivación?
Cada vez que salía a pescar, tenía que consultar múltiples fuentes para saber si era buen día: tabelas de mareas en un sitio, clima en otro, fases lunares en otro más. Quería tener todo en un solo lugar, optimizado para móvil (para usar en el barco).

### ¿Qué problema resolve?
Consolida en una sola interfaz: mareas, clima, temperatura del mar, fases lunares y score de pesca. Solo buscas tu ubicación y tienes el pronóstico completo.

### ¿Qué aprendí?
A integrar múltiples APIs públicas (NOAA, Open-Meteo, Nominatim), calcular scores de pesca basados en factores reales, y construir un frontend minimalista centrado en la experiencia.mobile-first.

---

## 📋 Tabla de Contenido

- [Descripción](#-descripción)
- [Demo](#-demo)
- [Características](#-características)
- [stack](#-stack)
- [Comenzando](#-comenzando)
- [APIs y Endpoints](#-apis-y-endpoints)
- [Ciudades Soportadas](#-ciudades-soportadas)
- [Algoritmo de Score](#-algoritmo-de-score)
- [Cómo Contribuir](#-cómo-contribuir)
- [Licencia](#-licencia)
- [Contacto](#-contacto)
- [Agradecimientos](#-agradecimientos)

---

## 🎬 Demo

> **Nota:** El demo en vivo está en proceso de deployment en Render. Mientras tanto, ejecutar localmente.

[![Demo Principal](https://via.placeholder.com/800x500/1E293B/0EA5E9?text=Demo+Pesca+App)](https://via.placeholder.com/800x500)

**Enlace temporal:** [pesca-app.onrender.com](https://pesca-app.onrender.com) (en proceso)

---

## ✨ Características

| Característica | Descripción |
|----------------|------------|
| 🌊 **Tabla de Mareas** | Predicciones de pleamar y bajamar con horas y alturas |
| 🌤️ **Clima** | Temperatura, viento, humedad y presión atmosférica |
| 🌡️ **Temperatura del Mar** | Datos de temperatura marina en tiempo real |
| 🌙 **Fase Lunar** | Iluminación lunar, tipo de luna actual |
| 🎣 **Score de Pesca** | Algoritmo 1-10 basado en mareas, clima y lunares |
| ⭐ **Mejores Horarios** | Periodos óptimos de pesca (major/minor periods) |
| 📍 **Búsqueda** | Por ciudad, coordenadas o GPS del navegador |
| 🗺️ **Mapa Interactivo** | Visualización de ubicación con Leaflet |
| 📱 **Diseño Responsive** | Adaptado para móvil, tablet y desktop |
| 📊 **Coeficiente de Marea** | Cálculo basado en rango de mareas |
| 📝 **Contexto de Pesca** | Descripción contextual personalizada |
| 🔄 **Geocodificación** | Resuelve nombres de ciudades a coordenadas |

---

## 🛠️ Stack

[![Python](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-blue?style=for-the-badge)](https://flask.palletsprojects.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript)](https://javascript.com)
[![Leaflet](https://img.shields.io/badge/Leaflet.js-1.9-blue?style=for-the-badge)](https://leafletjs.com)
[![NOAA](https://img.shields.io/badge/NOAA-Co--Ops-blue?style=for-the-badge)](https://tidesandcurrents.noaa.gov)

---

## 🚀 Comenzando

### Prerrequisitos

- [Python](https://python.org/) `>= 3.12`
- Navegador moderno con JavaScript habilitado

### 1. Clonar e instalar

```bash
git clone https://github.com/oscaromargp/pesca-app.git
cd pesca-app
pip install -r requirements.txt
```

### 2. Ejecutar en local

```bash
python app.py
# Abre http://localhost:5000
```

### 3. Deployment a Render (opcional)

[![Deploy to Render](https://img.shields.io/badge/Deploy_to_Render-4.0-blue?style=for-the-badge)](https://render.com/deploy?repo=https://github.com/oscaromargp/pesca-app)

O manualmente:
1. Ir a [dashboard.render.com](https://dashboard.render.com)
2. Crear nuevo **Web Service**
3. Conectar repositorio GitHub
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Python Version: `3.12`

---

## 📡 APIs y Endpoints

### Endpoints Disponibles

| Endpoint | Descripción | Ejemplo |
|----------|------------|---------|
| `/` | Página principal | — |
| `/api/forecast?lat=&lon=` | Pronóstico completo | `/api/forecast?lat=24.142&lon=-110.310` |
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

| Ciudad | Estado | Coordenadas |
|--------|-------|-----------|
| La Paz | BCS | 24.142, -110.310 |
| Mazatlán | Sinaloa | 23.225, -106.420 |
| Cabo San Lucas | BCS | 22.891, -109.928 |
| Ensenada | BC | 31.866, -116.625 |
| San Felipe | BC | 31.024, -114.832 |
| Guaymas | Sonora | 27.919, -110.907 |
| Manzanillo | Colima | 19.054, -104.318 |
| Cancún | QRoo | 21.161, -86.851 |
| Progreso | Yucatán | 21.283, -89.667 |
| Tampico | Tamaulipas | 22.255, -97.868 |
| Veracruz | Veracruz | 19.189, -96.291 |
| Acapulco | Guerrero | 16.863, -99.883 |
| Tijuana | BC | 32.515, -117.069 |

### Estados Unidos

| Ciudad | Estado | Coordenadas |
|--------|-------|-----------|
| Miami | Florida | 25.762, -80.192 |
| Key West | Florida | 24.555, -81.808 |
| San Diego | California | 32.716, -117.161 |
| Santa Bárbara | California | 34.421, -119.702 |

---

## 📊 Algoritmo de Score

El score de pesca (1-10) considera múltiples factores:

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

**Fórmula:**
```
score = 5.0 + factores_marea + factores_clima + factores_solunares
clampeado entre 1 y 10
```

---

## 🤝 Cómo Contribuir

¡Las contribuciones son bienvenidas!

1. Haz fork del repositorio
2. Crea tu rama: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -m 'feat: describe el cambio'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Abre un Pull Request

---

## 💖 Apoya este Proyecto

Si Pesca App te fue útil, considera hacer una contribución. Me ayuda a seguir construyendo herramientas de código abierto.

**Donaciones en Criptomonedas — Red XRP**

> Dirección XRP: `rBthUCndKy3Xbb19Ln4xkZeMwusX9NrYfj`

---

## 📄 Licencia

Distribuido bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## 📬 Contacto

**Oscar Omar Gómez Peña**

[![Portafolio](https://img.shields.io/badge/Portafolio-web-blue?style=for-the-badge)](https://oscaromargp.github.io/Oscaromargp/)
[![GitHub](https://img.shields.io/badge/GitHub-oscaromargp-blue?style=for-the-badge&logo=github)](https://github.com/oscaromargp)

[![Email](https://img.shields.io/badge/Email-oscaromargp%40gmail.com-blue?style=for-the-badge)](mailto:oscaromargp@gmail.com)

---

## 👥 Contribuidores

[![oscaromargp](https://github.com/oscaromargp.png)](https://github.com/oscaromargp)

---

## 🙏 Agradecimientos

*"Porque Dios es el que en vosotros produce*  
*así el querer como el hacer,*  
*por su buena voluntad."*  
**— Filipenses 2:13**

Todo lo que aquí existe nació primero como un deseo en el corazón.  
Cada proyecto, cada línea, cada idea que toma forma —  
es un regalo de Aquel que nos dio tanto el sueño como la fuerza de alcanzarlo.  
**A Dios, toda la gloria.**

### Recursos y Referencias

| Recurso | Descripción |
|--------|------------|
| [tidewise](https://github.com/AreteDriver/tidewise) | Algoritmo de scoring de pesca |
| [solunarbass](https://github.com/bassfinity/solunarbass) | Cálculos solunares |
| [Fishing-Report-Analyzer](https://github.com/seang1121/Fishing-Report-Analyzer) | Multi-API approach |
| [tablademareas.com](https://tablademareas.com) | Referencia de UX/UI |
| [tideschart.com](https://es.tideschart.com) | Referencia de tablas |
| [fishingpoints.app](https://fishingpoints.app) | Referencia de pronósticos |

### APIs Utilizadas

- **NOAA CO-OPS** — Mareas y corrientes
- **Open-Meteo** — Clima y datos marinos
- **OpenStreetMap/Nominatim** — Mapas y geocodificación
- **ipapi.co** — Geolocalización por IP
- **Skyfield** — Cálculos astronómicos
- **Leaflet.js** — Mapas interactivos