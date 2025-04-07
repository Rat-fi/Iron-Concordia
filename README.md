| NAME| GitHub NAME | STUDENT ID |

| ---- | -------- | --------- |

| Raphael deyo | Rat-fi | 40166562 |

| Kaiyu Nie | chemoautotroph | 40121808 |

| Li An | LI-AN-Morty | 40309778 |

  
  

CUFitness is a Django-based AI-powered virtual fitness & nutrition assistant designed to help users build personalized health plans using natural language. It leverages Google Gemini for intelligent conversation and interacts with multiple health, meal, and activity models to create and track goals.

  

---

  

## Features

  

- AI Chatbot powered by Google Gemini (Gemini 1.5 Flash)

- Personalized fitness plans & meal recommendations

- Plan confirmation with automatic GymGoal tracking

- Campus restaurant menu & dietary filtering

- Continuous conversation history

- User authentication

---

## Setup Instructions

  

### 1️⃣ Clone the Repository

  

```
git clone https://github.com/your-username/CUFitness.git

cd CUFitness
```

  

### 2️⃣ Create a Virtual Environment

  

```
python -m venv venv

source venv/bin/activate # or venv\Scripts\activate on Windows
```

  

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

  

### 4️⃣ Set up Environment Variables

  

Create a .env file and add your Google API Key:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

  

### 5️⃣ Apply Migrations

  

```
python manage.py makemigrations

python manage.py migrate
```

  

### 6️⃣ Create a Superuser

  

```
python manage.py createsuperuser
```

  

### 7️⃣ Run the Server

  

```
python manage.py runserver
```

  

---

  

## 💡 Usage

Open http://127.0.0.1:8000/chat/ to interact with the AI.

  

Provide your health data or goals.

  

Receive a full fitness + nutrition plan.

  

Reply with "confirm plan" to track it inside your GymGoal.

  

---