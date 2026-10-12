
# 🌿 AgroAI – Smart Crop Doctor

### AI-Powered Plant Disease Detection & Smart Farming Assistant

AgroAI is a smart farming web application designed to help farmers identify possible plant diseases, explore crop information, and receive helpful crop-care guidance.

The application combines **Django, Python, Machine Learning, HTML, CSS, and JavaScript** with a farmer-friendly interface.

It supports English, Kannada, and Hindi, making crop-care information more accessible.

> **Project Status:** Under development. The crop library, user interface, and rule-based farm assistant are implemented. AI disease prediction requires a compatible TensorFlow runtime and a trained model.

---

## 🌟 Features

### 🌱 1. Explore 24 Crops

Browse information about 24 crops across different categories.

**Vegetables**
- Tomato
- Potato
- Chilli
- Brinjal
- Okra
- Onion
- Carrot
- Cabbage

**Grains**
- Maize
- Rice
- Wheat
- Sorghum

**Fruits**
- Mango
- Banana
- Papaya
- Grapes
- Coconut
- Guava

**Commercial Crops**
- Cotton
- Groundnut
- Soybean
- Sugarcane
- Coffee
- Sunflower

Each crop guide provides basic growing conditions, common problems, and prevention information.

### 📸 2. AI Plant Disease Scanner

- Upload plant-leaf images.
- Capture photos using a supported mobile browser.
- Submit images to the Django prediction API.
- Display disease predictions and confidence scores when the trained model is available.
- Provide general plant-care guidance.

**Supported formats:** JPG, PNG, WEBP.

> Disease scanning depends on the availability and compatibility of the trained TensorFlow model. Predictions are not guaranteed to be accurate.

### 🤖 3. AgroAI Farm Assistant

An interactive, rule-based farming assistant that supports:

- Friendly greetings such as "Hi" and "Hello".
- Common farming questions.
- Crop watering advice.
- Yellow-leaf explanations.
- Soil and crop-care tips.
- Pest and disease-prevention guidance.
- Quick suggested questions.

The assistant uses programmed responses and keyword matching. It is not currently a generative AI model.

### 🎤 4. Voice Assistant

- Ask farming questions using speech recognition.
- Listen to spoken answers using text-to-speech.
- Support for English, Kannada, and Hindi where browser speech services are available.

### 🌐 5. Multilingual Support

- English
- ಕನ್ನಡ (Kannada)
- हिन्दी (Hindi)

Some interface text and assistant responses are translated. Full translation coverage is a future improvement.

### ☰ 6. Sidebar Navigation

An interactive menu provides access to:

- Home
- Explore Crops
- Disease Scanner
- Farm Tips
- About
- Farm Assistant

### 🔐 7. User Authentication

Django-based authentication endpoints for:

- User registration
- Login
- Logout
- Session verification
- CSRF protection

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| HTML5 | Website structure |
| CSS3 | Styling and responsive layout |
| JavaScript | Interactive frontend |
| Python | Backend programming |
| Django | Web framework |
| TensorFlow / Keras | Machine learning inference |
| SQLite | Database |
| Web Speech API | Voice input and output |
| Git & GitHub | Version control |

---

## 📁 Project Structure

```text
AgroAI/
│
├── backend/
│   ├── manage.py
│   │
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── detector/
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── models.py
│   │   ├── migrations/
│   │   └── static/
│   │       └── agroai_enhancements.js
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── home.html
│   │   ├── crops.html
│   │   ├── scanner.html
│   │   ├── about.html
│   │   ├── accounts.html
│   │   ├── contact.html
│   │   └── treatments.html
│   │
│   ├── plant_disease_model.keras
│   ├── classes.txt
│   └── db.sqlite3
│
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** The structure above is an example based on the project setup. Actual model-file locations and other files may vary.

---

## 💻 Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholders with your actual GitHub username and repository name.

### Step 2: Create a Virtual Environment

On Windows:

```bat
py -3.12 -m venv .venv312
```

Activate the environment:

```bat
.venv312\Scripts\activate
```

### Step 3: Install Dependencies

```bat
pip install django pillow tensorflow
```

Alternatively, if the repository includes an up-to-date requirements file:

```bat
pip install -r requirements.txt
```

TensorFlow installation and execution depend on OS compatibility and security policies.

### Step 4: Open the Backend Directory

```bat
cd backend
```

### Step 5: Apply Database Migrations

```bat
python manage.py migrate
```

### Step 6: Start the Django Server

```bat
python manage.py runserver 127.0.0.1:8000
```

### Step 7: Open the Website

Visit:

http://127.0.0.1:8000/

---

## 🔌 Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict/` | POST | Plant disease prediction |
| `/api/auth/csrf/` | GET | Get CSRF token |
| `/api/auth/register/` | POST | Register a user |
| `/api/auth/login/` | POST | User login |
| `/api/auth/me/` | GET | Current user details |
| `/api/auth/logout/` | POST | User logout |

The prediction endpoint expects a plant-leaf image in a multipart form field named `image`.

---

## 🧠 How AgroAI Works

1. The farmer opens the AgroAI website.
2. The farmer browses crop information or opens the disease scanner.
3. The farmer uploads a photo of an affected plant leaf.
4. Django receives the image and prepares it for the machine learning model.
5. If the model is available, it predicts a possible plant disease.
6. The website displays the prediction and general guidance.
7. The farmer can also ask common farming questions through the assistant.

---

## 🔮 Future Enhancements

- [ ] Connect a generative AI farming assistant.
- [ ] Improve Kannada and Hindi translation coverage.
- [ ] Expand the crop disease dataset.
- [ ] Improve model accuracy and validation.
- [ ] Add location-aware weather information.
- [ ] Add region-specific crop recommendations.
- [ ] Develop a Flutter mobile application.
- [ ] Add personalized farming dashboards.
- [ ] Improve accessibility and voice features.
- [ ] Deploy the application online.

---

## 🔒 Security

Before publishing the repository:

- Never upload Django secret keys or passwords.
- Keep `.env` files private.
- Disable `DEBUG` in production.
- Configure production `ALLOWED_HOSTS`.
- Do not upload the virtual environment.
- Review uploaded images and personal data carefully.

A sample `.gitignore`:

```gitignore
.venv/
.venv312/
venv/
__pycache__/
*.pyc
.env
db.sqlite3
media/
.idea/
.vscode/
```

---

## ⚠️ Disclaimer

AgroAI is an educational and decision-support project.

AI-generated disease predictions and crop-care suggestions may be incorrect.

Farmers should confirm plant diseases, pesticide choices, dosages, and treatments with qualified local agricultural experts before taking action.

---

## 🤝 Contributions

Contributions, bug reports, feature suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Commit your work.
5. Open a pull request.

---

## 📄 License

No license has been specified yet. Add a `LICENSE` file if you want to define how others may use or contribute to the project.

---

## 🌾 Project Vision

**"Healthy Crops. Better Harvests. Brighter Future."**

AgroAI aims to make practical crop-care knowledge and AI-assisted farming tools more accessible to farmers.

**Made with 💚 for smarter agriculture.**
