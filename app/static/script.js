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
var marker = L.marker([51.505, -0.09]).addTo(map)
    .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
    .openPopup();

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

    // Toggle dark mode for the news container
    document.getElementById('news-container').classList.toggle('light-mode');
    document.getElementById('single-news-container').classList.toggle('light-mode');
});

// Function to update map and marker
function updateMapAndMarker(lat, lon) {
    map.setView([lat, lon], 10);
    marker.setLatLng([lat, lon]).update();
}

// Function to fetch and display weather data
function fetchWeather(city = 'London') {
    const apiKey = 'b710ebc3b9e2b171a89cdae316167899';
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const weatherContainer = document.getElementById('weather-container');
            const weatherInfo = `
                <p>City: ${data.name}</p>
                <p>Temperature: ${data.main.temp} °C</p>
                <p>Weather: ${data.weather[0].description}</p>
            `;
            weatherContainer.innerHTML = weatherInfo;
            // Update the map and marker based on the new city's coordinates
            const lat = data.coord.lat;
            const lon = data.coord.lon;
            updateMapAndMarker(lat, lon);
        })
        .catch(error => console.error('Error fetching weather data:', error));
}

// Function to fetch and display news headlines
function fetchNews() {
    const apiKey = '93fe34b301c4496ab82738f821b76915';
    const apiUrl = `https://newsapi.org/v2/top-headlines?country=gb&apiKey=${apiKey}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const singleNewsContainer = document.getElementById('single-news-container');
            const newsContainer = document.getElementById('news-articles');
            newsContainer.innerHTML = ''; // Clear any previous news articles

            if (data.articles.length > 0) {
                const firstArticle = data.articles[0];
                singleNewsContainer.innerHTML = `
                    <h3>${firstArticle.title}</h3>
                    <p>${firstArticle.description}</p>
                    <a href="${firstArticle.url}" target="_blank">Read more</a>
                `;

                // Display remaining articles in the news container
                data.articles.slice(1).forEach(article => {
                    const newsArticle = document.createElement('div');
                    newsArticle.classList.add('news-article');
                    newsArticle.innerHTML = `
                        <h3>${article.title}</h3>
                        <p>${article.description}</p>
                        <a href="${article.url}" target="_blank">Read more</a>
                    `;
                    newsContainer.appendChild(newsArticle);
                });
            }
        })
        .catch(error => console.error('Error fetching news data:', error));
}

// Call fetchNews on page load
window.onload = function() {
    fetchWeather();
    fetchNews();
};

// Example: Update the map and marker when a new city is searched
// Assuming there's an input field with id 'city-input' and a button to trigger the search
document.getElementById('search-button').addEventListener('click', () => {
    const city = document.getElementById('city-input').value;
    fetchWeather(city);
});
