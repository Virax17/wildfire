let map = L.map('map').setView([20.5937, 78.9629], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

function uploadImage() {
    let input = document.getElementById("imageUpload").files[0];
    if (!input) {
        alert("Please select an image!");
        return;
    }

    let formData = new FormData();
    formData.append("file", input);

    fetch('http://127.0.0.1:5000/predict', {  // Ensure backend runs on this address
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("predictionResult").innerText = 
            `🔥 Prediction: ${data.prediction} (${data.confidence.toFixed(2)}%)`;

        if (data.location) {
            let { lat, lon } = data.location;
            L.marker([lat, lon]).addTo(map)
            .bindPopup(`<h3>🔥 Fire Detected</h3><p>Location: (${lat}, ${lon})</p>`);
        }
    })
    .catch(error => console.error("Error:", error));
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

function showAllFires() {
    let recentFires = [
        { title: "Forest Fire in California", lat: 36.7783, lon: -119.4179 },
        { title: "Warehouse Fire in Texas", lat: 31.9686, lon: -99.9018 }
    ];
    recentFires.forEach(fire => {
        L.marker([fire.lat, fire.lon]).addTo(map)
        .bindPopup(`<h3>🔥 ${fire.title}</h3>`);
    });
}

