function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');
        botMessage.textContent = data.response;
        chatBox.appendChild(botMessage);
        document.getElementById('user-input').value = '';
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
    });
}

// Initialize the map
var map = L.map('map').setView([51.505, -0.09], 10);

var lightTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
});

var darkTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
});

// Add dark tile layer by default
darkTileLayer.addTo(map);

// Set dark mode as default
document.body.classList.add('dark-mode');

// Function to switch tile layers
function switchTileLayer(isDarkMode) {
    if (isDarkMode) {
        map.removeLayer(lightTileLayer);
        darkTileLayer.addTo(map);
    } else {
        map.removeLayer(darkTileLayer);
        lightTileLayer.addTo(map);
    }
}

// Dark mode toggle
document.getElementById('dark-mode-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
    switchTileLayer(document.body.classList.contains('dark-mode'));
});
