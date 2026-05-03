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
        const score = data.fishing_score;
        document.getElementById('score').textContent = score;
        document.getElementById('score').style.color = getScoreColor(score);
        document.getElementById('scoreLabel').textContent = getScoreLabel(score);
        
        // Update tides
        const tidesHtml = data.tides.tides.slice(0, 6).map(t => `
            <div class="tide-item tide-${t.type}">
                <span>${t.type === 'high' ? '🌊' : '🔵'} ${t.type === 'high' ? 'Pleamar' : 'Bajamar'}</span>
                <span>${formatTime(t.time)} (${t.height}m)</span>
            </div>
        `).join('');
        document.getElementById('tidesInfo').innerHTML = `
            <div class="info-row"><span class="label">Estación</span><span class="value">${data.tides.station || 'N/A'}</span></div>
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
        const s = data.solunar;
        document.getElementById('solunarInfo').innerHTML = `
            <div class="info-row"><span class="label">Fase lunar</span><span class="value">${(s.moon_phase * 100).toFixed(0)}%</span></div>
            <div class="info-row"><span class="label">Rating</span><span class="value">${'⭐'.repeat(s.solunar_rating)}</span></div>
            <div class="info-row"><span class="label">Major</span><span class="value">${s.major_periods.join(', ')}</span></div>
            <div class="info-row"><span class="label">Minor</span><span class="value">${s.minor_periods.join(', ')}</span></div>
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
    fetch('/api/forecast')
        .then(r => r.json())
        .then(d => loadForecast(d.location.lat, d.location.lon))
        .catch(err => {
            // Default to Miami
            loadForecast(25.7617, -80.1918);
        });
};
