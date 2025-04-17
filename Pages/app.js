// app.js

// Leaflet map setup
let map = L.map('map').setView([39.8283, -98.5795], 4);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const hospitals = [
  {
    name: "Johns Hopkins Hospital",
    location: "Baltimore, MD",
    coordinates: [39.2964, -76.5926],
    description: "World-renowned center for sickle cell research and treatment"
  },
  {
    name: "Duke University Hospital",
    location: "Durham, NC",
    coordinates: [36.0087, -78.9387],
    description: "Leading comprehensive sickle cell center"
  },
  {
    name: "St. Jude Children's Research Hospital",
    location: "Memphis, TN",
    coordinates: [35.1516, -90.0409],
    description: "Pioneering pediatric sickle cell treatment"
  },
  {
    name: "Children's Hospital of Philadelphia",
    location: "Philadelphia, PA",
    coordinates: [39.9480, -75.1932],
    description: "Excellence in pediatric sickle cell care"
  },
  {
    name: "Mayo Clinic",
    location: "Rochester, MN",
    coordinates: [44.0225, -92.4669],
    description: "Comprehensive sickle cell treatment center"
  }
];

// Add hospitals to list
const hospitalList = document.getElementById('hospital-list');
hospitals.forEach(hospital => {
  const li = document.createElement('li');
  li.textContent = `${hospital.name} - ${hospital.location}`;
  li.onclick = () => handleHospitalClick(hospital);
  hospitalList.appendChild(li);

  L.marker(hospital.coordinates).addTo(map)
    .bindPopup(`
      <strong>${hospital.name}</strong><br>
      ${hospital.location}<br>
      ${hospital.description}
    `);
});

// Handle hospital selection
function handleHospitalClick(hospital) {
  map.setView(hospital.coordinates, 13);
  document.getElementById('route-summary').style.display = 'none';
}

// Search Location
const searchForm = document.getElementById('search-form');
searchForm.addEventListener('submit', async function (e) {
  e.preventDefault();
  const query = document.getElementById('search-location').value;
  const coords = await searchLocation(query);
  if (coords) {
    map.setView(coords, 13);
  }
});

// Fetch coordinates from OpenStreetMap Nominatim API
async function searchLocation(query) {
  const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
  const data = await res.json();
  if (data.length > 0) {
    return [parseFloat(data[0].lat), parseFloat(data[0].lon)];
  }
  alert('Location not found');
  return null;
}

// Route calculation
document.getElementById('calculate-route').addEventListener('click', function() {
  const source = document.getElementById('source').value;
  const destination = document.getElementById('destination').value;

  if (!source || !destination) {
    alert('Please enter both source and destination locations');
    return;
  }

  calculateRoute(source, destination);
});

async function calculateRoute(source, destination) {
  const sourceCoords = await searchLocation(source);
  const destCoords = await searchLocation(destination);

  if (!sourceCoords || !destCoords) return;

  const routeData = await fetch(`https://router.project-osrm.org/route/v1/driving/${sourceCoords[1]},${sourceCoords[0]};${destCoords[1]},${destCoords[0]}?overview=full&geometries=geojson&steps=true`);
  const route = await routeData.json();

  if (route.routes && route.routes.length > 0) {
    const polyline = L.geoJSON(route.routes[0].geometry).addTo(map);
    map.fitBounds(polyline.getBounds());
    
    const steps = route.routes[0].legs[0].steps.map(step => step.maneuver.instruction);
    
    displayRouteSummary(route.routes[0].distance, route.routes[0].duration, steps);
  }
}

function displayRouteSummary(distance, duration, steps) {
  const summary = document.getElementById('route-summary');
  summary.innerHTML = `
    <h3>Route Summary</h3>
    <p><strong>Total Distance:</strong> ${formatDistance(distance)}</p>
    <p><strong>Estimated Time:</strong> ${formatDuration(duration)}</p>
    <h4>Turn-by-Turn Directions:</h4>
    <ul>
      ${steps.map(step => `<li>${step}</li>`).join('')}
    </ul>
  `;
  summary.style.display = 'block';
}

function formatDistance(meters) {
  return meters < 1000 ? `${Math.round(meters)} m` : `${(meters / 1000).toFixed(1)} km`;
}

function formatDuration(seconds) {
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return `${hours}h ${remainingMinutes} min`;
}
