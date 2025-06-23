# 🏋️ FitBuddy Voice Assistant

**FitBuddy** is a voice-controlled workout assistant built using **Streamlit**. It helps you start your workout sessions, guides you through sets with timers, and logs your history — all with voice commands.

### 🔧 Tech Stack

- **Frontend & App UI**: Streamlit  
- **Voice Recognition**: SpeechRecognition (Google Speech API)  
- **Voice Output**: pyttsx3 (Text-to-Speech)  
- **Charts**: Altair  
- **Data**: Stored in Streamlit session state (in-memory)

---

## 🚀 Features

- 🎙️ **Voice-Driven UI**: Start workouts with commands like _"chest"_ or _"okay start"_
- 📋 **Auto-Generated Workout Plans** (3 random exercises per muscle group)
- ⏱️ **30s Set Timers** with countdown and vocal cues
- 📊 **Workout History** with duration, frequency, and interactive charts
- 💬 **Text-to-Speech** guidance using `pyttsx3`


## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/FitBuddy.git
cd FitBuddy
pip install -r requirements.txt
streamlit run app.py
```

