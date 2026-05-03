# 🎣 Pesca App

App de pesca que combina clima, mareas, corrientes y pronóstico de pesca en una sola interfaz.

## Características

- 🌊 **Mareas**: Predicciones de mareas usando NOAA CO-OPS API
- 🌤️ **Clima**: Pronóstico del tiempo con Open-Meteo
- 🌙 **Solunar**: Cálculos de fases lunares y periodos de pesca óptimos
- 📍 **Ubicación**: Detección automática por IP o entrada manual de coordenadas
- 🗺️ **Mapa**: Visualización con Leaflet.js
- ⭐ **Score de Pesca**: Algoritmo 1-10 basado en múltiples factores

## APIs Utilizadas

| API | Propósito | Costo |
|-----|-----------|-------|
| NOAA CO-OPS | Mareas y corrientes | Gratis |
| Open-Meteo | Clima y datos marinos | Gratis |
| Skyfield | Cálculos astronómicos | Gratis (local) |
| ipapi.co | Geolocalización por IP | Gratis |

## Instalación

```bash
pip install -r requirements.txt
python app.py
```

La app estará disponible en `http://localhost:5000`

## Uso

1. La app detecta tu ubicación automáticamente por IP
2. Opcionalmente ingresa coordenadas manualmente (lat, lon)
3. Usa el botón "Mi ubicación" para geolocalización del navegador
4. Visualiza el score de pesca y condiciones detalladas

## Basado en

- [tidewise](https://github.com/AreteDriver/tidewise) - Scoring algorithm
- [solunarbass](https://github.com/bassfinity/solunarbass) - Solunar calculations
- [Fishing-Report-Analyzer](https://github.com/seang1121/Fishing-Report-Analyzer) - Multi-API approach

## Licencia

MIT
