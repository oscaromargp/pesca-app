let map;
let currentLat = null;
let currentLon = null;

function initMap(lat, lon) {
    if (map) map.remove();
    
    map = L.map('map').setView([lat, lon], 10);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    L.marker([lat, lon]).addTo(map)
        .bindPopup('📍 Tu ubicación')
        .openPopup();
}

function getScoreLabel(score) {
    if (score >= 9) return '¡Excelente para pescar!';
    if (score >= 7) return 'Muy bueno';
    if (score >= 5) return 'Bueno';
    if (score >= 3) return 'Regular';
    return 'No recomendado';
}

function getScoreColor(score) {
    if (score >= 9) return '#10b981';
    if (score >= 7) return '#667eea';
    if (score >= 5) return '#f59e0b';
    if (score >= 3) return '#f97316';
    return '#ef4444';
}

function formatTime(timeStr) {
    if (!timeStr) return '--:--';
    return timeStr.split(' ')[1] || timeStr;
}

async function loadForecast(lat, lon) {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
    
    try {
        const url = `/api/forecast?lat=${lat}&lon=${lon}`;
        const resp = await fetch(url);
        const data = await resp.json();
        
        currentLat = lat;
        currentLon = lon;
        
        // Update location
        document.getElementById('locationInfo').innerHTML = `
            <div class="info-row"><span class="label">Ciudad</span><span class="value">${data.location.city || 'N/A'}</span></div>
            <div class="info-row"><span class="label">País</span><span class="value">${data.location.country || 'N/A'}</span></div>
            <div class="info-row"><span class="label">Lat</span><span class="value">${lat.toFixed(4)}</span></div>
            <div class="info-row"><span class="label">Lon</span><span class="value">${lon.toFixed(4)}</span></div>
        `;
        
        // Update score
        const score = data.fishing_score || 0;
        document.getElementById('score').textContent = score;
        document.getElementById('score').style.color = getScoreColor(score);
        document.getElementById('scoreLabel').textContent = getScoreLabel(score);
        
        // Update tides
        const tidesData = data.tides?.tides || [];
        const tidesHtml = tidesData.slice(0, 6).map(t => `
            <div class="tide-item tide-${t.type}">
                <span>${t.type === 'high' ? '🌊' : '🔵'} ${t.type === 'high' ? 'Pleamar' : 'Bajamar'}</span>
                <span>${formatTime(t.time)} (${t.height}m)</span>
            </div>
        `).join('');
        document.getElementById('tidesInfo').innerHTML = `
            <div class="info-row"><span class="label">Estación</span><span class="value">${data.tides?.station || 'N/A'}</span></div>
            ${tidesHtml}
        `;
        
        // Update weather
        const w = data.weather;
        document.getElementById('weatherInfo').innerHTML = `
            <div class="info-row"><span class="label">Temp</span><span class="value">${w.temperature}°C</span></div>
            <div class="info-row"><span class="label">Viento</span><span class="value">${w.wind_speed} km/h</span></div>
            <div class="info-row"><span class="label">Humedad</span><span class="value">${w.humidity}%</span></div>
            <div class="info-row"><span class="label">Presión</span><span class="value">${w.pressure} hPa</span></div>
        `;
        
        // Update solunar
        const s = data.solunar || {};
        document.getElementById('solunarInfo').innerHTML = `
            <div class="info-row"><span class="label">Fase</span><span class="value">${s.moon_phase_name || '--'}</span></div>
            <div class="info-row"><span class="label">Iluminación</span><span class="value">${s.illumination_percent || 0}%</span></div>
            <div class="info-row"><span class="label">Rating</span><span class="value">${'⭐'.repeat(s.solunar_rating || 0)}</span></div>
        `;
        
        // Update map
        initMap(lat, lon);
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('dashboard').classList.remove('hidden');
        
    } catch (err) {
        alert('Error cargando datos: ' + err.message);
        document.getElementById('loading').classList.add('hidden');
    }
}

function searchLocation() {
    const input = document.getElementById('coords').value.trim();
    const parts = input.split(',').map(s => parseFloat(s.trim()));
    if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
        loadForecast(parts[0], parts[1]);
    } else {
        alert('Ingresa coordenadas válidas: lat, lon');
    }
}

function detectLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            pos => loadForecast(pos.coords.latitude, pos.coords.longitude),
            err => {
                alert('No se pudo detectar ubicación. Usando IP...');
                fetch('/api/forecast')
                    .then(r => r.json())
                    .then(d => loadForecast(d.location.lat, d.location.lon));
            }
        );
    } else {
        alert('Geolocalización no soportada. Usando IP...');
    }
}

// Load initial data
window.onload = function() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('content').classList.add('hidden');
    
    fetch('/api/forecast')
        .then(r => r.json())
        .then(d => renderData(d))
        .catch(err => {
            loadData(24.142, -110.310);
        });
};

function renderData(data) {
    const loc = data.location || {};
    document.getElementById('locationName').textContent = loc.city || 'La Paz';
    document.getElementById('locationCountry').textContent = loc.country || 'Baja California Sur, México';

    const score = data.fishing_score || 5;
    document.getElementById('scoreValue').textContent = score;
    document.getElementById('scoreValue').style.color = score >= 7 ? 'var(--success)' : score >= 5 ? 'var(--warning)' : 'var(--danger)';
    document.getElementById('scoreLabel').textContent = score >= 7 ? 'Excelente 🐟' : score >= 5 ? 'Bueno 🐠' : 'Regular 🐡';

    document.getElementById('tideCoeff').textContent = data.tide_coefficient || '--';
    document.getElementById('fishingContext').textContent = data.fishing_context || '';

    const tides = data.tides?.tides || [];
    if (tides.length > 0) {
        const formatTime = (t) => t?.split(' ')[1]?.substring(0, 5) || '--:--';
        document.getElementById('nextTide').textContent = formatTime(tides[0].time);
        document.getElementById('nextTideLabel').textContent = tides[0].type === 'high' ? 'Pleamar ▲' : 'Bajamar ▼';
    }

    const solunar = data.solunar || {};
    const illum = solunar.illumination_percent || 50;
    document.getElementById('moonVisual').textContent = illum > 60 ? '🌕' : illum > 30 ? '🌓' : '🌑';
    document.getElementById('moonName').textContent = solunar.moon_phase_name || 'Luna Creciente';
    document.getElementById('moonIllum').textContent = illum + '% iluminada';

    const w = data.weather || {};
    document.getElementById('waterTemp').textContent = (w.water_temperature || '--') + '°C';

    renderTideTable(tides);
    renderBestTimes(solunar);
    renderWeather(w);
    
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('content').classList.remove('hidden');
}

function renderTideTable(tides) {
    if (!tides || tides.length === 0) {
        document.getElementById('tideTableBody').innerHTML = '<div class="tide-row"><div>No hay datos</div></div>';
        return;
    }
    const rows = [];
    const formatTime = (t) => t?.split(' ')[1]?.substring(0, 5) || '--:--';
    for (let i = 0; i < Math.min(4, tides.length); i++) {
        const t = tides[i];
        rows.push(`
          <div class="tide-row">
            <div class="tide-day">${i === 0 ? 'Hoy' : formatTime(t.time)}</div>
            <div class="tide-time">
              <span class="${t.type === 'high' ? 'tide-high' : 'tide-low'}">
                ${t.type === 'high' ? '▲' : '▼'} ${formatTime(t.time)}
              </span>
              <div class="tide-value">${t.height || 0}m</div>
            </div>
            <div></div><div></div><div></div>
            <div class="fishing-rating fish-avg">
              <span class="fish-icon">🐠</span> Bueno
            </div>
          </div>
        `);
    }
    document.getElementById('tideTableBody').innerHTML = rows.join('');
}

function renderBestTimes(solunar) {
    document.getElementById('bestTimesGrid').innerHTML = `
        <div class="best-time-card">
          <div class="best-time-label">⭐ Mejor momento</div>
          <div class="best-time-value">06:30-08:30</div>
          <div class="best-time-desc">Amanecer</div>
        </div>
        <div class="best-time-card">
          <div class="best-time-label">⭐ Segundo mejor</div>
          <div class="best-time-value">18:45-20:45</div>
          <div class="best-time-desc">Atardecer</div>
        </div>
    `;
}

function renderWeather(w) {
    const wt = w || {};
    document.getElementById('weatherGrid').innerHTML = `
        <div class="weather-item">
          <div class="weather-icon">🌡️</div>
          <div class="weather-temp">${wt.temperature || '--'}°C</div>
          <div class="weather-label">Temperatura Aire</div>
        </div>
        <div class="weather-item">
          <div class="weather-icon">🌊</div>
          <div class="weather-temp">${wt.water_temperature || '--'}°C</div>
          <div class="weather-label">Temperatura Mar</div>
        </div>
        <div class="weather-item">
          <div class="weather-icon">💨</div>
          <div class="weather-temp">${wt.wind_speed || '--'}</div>
          <div class="weather-label">Viento km/h</div>
        </div>
        <div class="weather-item">
          <div class="weather-icon">💧</div>
          <div class="weather-temp">${wt.humidity || '--'}%</div>
          <div class="weather-label">Humedad</div>
        </div>
        <div class="weather-item">
          <div class="weather-icon">📊</div>
          <div class="weather-temp">${wt.pressure || '--'}</div>
          <div class="weather-label">Presión hPa</div>
        </div>
    `;
}
