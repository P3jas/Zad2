from flask import Flask, render_template_string, request, send_from_directory
import requests
import os
import datetime

app = Flask(__name__)

@app.route('/tlo.jpg')
def background_image():
    return send_from_directory('.', 'tlo.jpg')

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"=================================\nAplikacja uruchomiona o: {current_time}")
print("Kacper Koźliński\nGr. 6.4\n101603\nPort: 8501\n=================================")

APIKey = os.getenv("API_KEY")

data_dict = {
    "Polska": ["Warszawa", "Kraków", "Łódź", "Wrocław", "Poznań"],
    "Niemcy": ["Berlin", "Hamburg", "Monachium", "Kolonia", "Frankfurt"],
    "Francja": ["Paryż", "Marsylia", "Lyon", "Tuluza", "Nicea"],
    "Hiszpania": ["Madryt", "Barcelona", "Walencja", "Sewilla", "Zaragoza"],
    "Włochy": ["Rzym", "Mediolan", "Neapol", "Turyn", "Palermo"]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Giga Pogodynka</title>
    <style>
        body {
            font-family: 'Source Sans Pro', sans-serif;
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/tlo.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
            padding: 1rem 5rem;
            margin: 0;
        }
        .container { 
            max-width: 700px; 
            margin: auto; 
            background: rgba(14, 17, 23, 0.8);
            padding: 30px;
            border-radius: 15px;
        }
        select, button {
            width: 100%; padding: 10px; margin: 10px 0;
            border-radius: 5px; border: 1px solid #444;
            background: #262730; color: white;
        }
        button { background-color: #6155F5; cursor: pointer; font-weight: bold; border: none; }
        hr { border: 0; height: 1px; background: #333; margin: 20px 0; }
    </style>
    <script>
        const cityData = {{ data_json | safe }};
        function updateCities() {
            const country = document.getElementById("country").value;
            const citySelect = document.getElementById("city");
            citySelect.innerHTML = "";
            cityData[country].forEach(city => {
                const opt = document.createElement("option");
                opt.value = city;
                opt.innerHTML = city;
                citySelect.appendChild(opt);
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>MEGA SUPER GIGA APLIKACJA POGODOWA!</h1>
        <form method="GET">
            <label>Wybierz kraj:</label>
            <select name="country" id="country" onchange="updateCities()">
                {% for c in countries %}
                <option value="{{ c }}" {% if selected_country == c %}selected{% endif %}>{{ c }}</option>
                {% endfor %}
            </select>
            
            <label>Wybierz miasto:</label>
            <select name="city" id="city">
                {% for city in cities %}
                <option value="{{ city }}" {% if selected_city == city %}selected{% endif %}>{{ city }}</option>
                {% endfor %}
            </select>
            
            <button type="submit">Pokaż pogodę</button>
        </form>

        {% if weather %}
        <hr>
        <div style="text-align: center; margin-top: 20px;">
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 0;">{{ selected_country }}, {{ selected_city }}</p>
            <img src="http://openweathermap.org/img/wn/{{ weather.icon }}@4x.png" style="width: 150px;">
            <p style="font-size: 60px; font-weight: bold; margin: 0; line-height: 1;">{{ weather.temp | round }} °C</p>
            <p style="font-size: 18px; color: #aaa; margin-top: 10px;">
                <b>Wilgotność:</b> {{ weather.humidity }}% | <b>Stan:</b> {{ weather.desc.capitalize() }}
            </p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    selected_country = request.args.get('country', 'Polska')
    selected_city = request.args.get('city', data_dict[selected_country][0])
    weather = None

    if request.args.get('city'):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={APIKey}&units=metric&lang=pl"
        r = requests.get(url)
        if r.status_code == 200:
            d = r.json()
            weather = {
                'temp': d['main']['temp'],
                'humidity': d['main']['humidity'],
                'icon': d['weather'][0]['icon'],
                'desc': d['weather'][0]['description']
            }

    import json
    return render_template_string(
        HTML_TEMPLATE, 
        countries=list(data_dict.keys()), 
        cities=data_dict[selected_country],
        data_json=json.dumps(data_dict),
        selected_country=selected_country,
        selected_city=selected_city,
        weather=weather
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)