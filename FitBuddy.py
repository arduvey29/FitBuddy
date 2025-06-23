import streamlit as st
import speech_recognition as sr
import random
from datetime import datetime
import pandas as pd
import altair as alt
import threading
import subprocess
import sys
import time

# === Function to speak text using pyttsx3 in a separate subprocess ===
def speak(text: str):
    def tts_process(t):
        cmd = f"import pyttsx3; engine=pyttsx3.init(); engine.say({t!r}); engine.runAndWait()"
        subprocess.Popen([sys.executable, "-c", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    threading.Thread(target=tts_process, args=(text,), daemon=True).start()

# === Utility: Speech Recognition ===
def listen_for_command(timeout=5, phrase_time_limit=7):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            with st.spinner("Listening... Please speak now."):
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except Exception as e:
        st.error("Microphone not accessible or timeout. Ensure your microphone is on and try again.")
        print("Microphone/listen error:", e)
        return None
    try:
        command = recognizer.recognize_google(audio).lower()
        st.success(f"You said: '{command}'")
        return command
    except Exception as e:
        st.error("Could not understand audio. Please try again.")
        print("Recognition error:", e)
        return None

# === Session State Setup ===
st.set_page_config(page_title="FitBuddy Voice Assistant", layout="wide", page_icon="🏋️")

# Inject demo logs every time (for screenshot/LinkedIn)
st.session_state.phase = st.session_state.get("phase", "idle")
st.session_state.selected_group = None
st.session_state.plan = None
st.session_state.exercise_idx = 0
st.session_state.set_idx = 0
st.session_state.workout_start_time = None
st.session_state.workout_log = [
    {
        "date": "2025-06-21 18:30",
        "muscle": "chest",
        "plan": [
            {"exercise": "Push-ups", "sets": 3, "reps": 12},
            {"exercise": "Bench Press", "sets": 3, "reps": 10},
            {"exercise": "Incline Dumbbell Press", "sets": 3, "reps": 15}
        ],
        "total_duration": 360
    },
    {
        "date": "2025-06-20 19:00",
        "muscle": "legs",
        "plan": [
            {"exercise": "Squats", "sets": 3, "reps": 15},
            {"exercise": "Lunges", "sets": 3, "reps": 12},
            {"exercise": "Leg Press", "sets": 3, "reps": 10}
        ],
        "total_duration": 420
    }
]

# === Exercise Data ===
exercises_dict = {
    "chest": ["Push-ups", "Bench Press", "Incline Dumbbell Press"],
    "legs": ["Squats", "Lunges", "Leg Press"],
    "back": ["Pull-ups", "Deadlifts", "Lat Pulldown"],
    "shoulders": ["Overhead Press", "Lateral Raises", "Shrugs"],
    "arms": ["Bicep Curls", "Tricep Dips", "Hammer Curls"],
    "core": ["Plank", "Crunches", "Russian Twists"],
    "full body": ["Burpees", "Jump Squats", "Mountain Climbers"]
}

# === Custom CSS Styling ===
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stInfobox, .stWarning, .stError, .stSuccess {
        border-left: 4px solid #FF4B4B;
        padding-left: 0.5em;
    }
    </style>
""", unsafe_allow_html=True)

# === Sidebar Summary ===
with st.sidebar:
    st.header("📊 Summary Stats")
    total = len(st.session_state.workout_log)
    st.metric("Total Workouts", total)
    if total > 0:
        df_stats = pd.DataFrame(st.session_state.workout_log)
        freq = df_stats["muscle"].value_counts()
        favorite = freq.idxmax()
        count_fav = freq.max()
        st.metric("Favorite Muscle", f"{favorite.title()} ({count_fav} times)")
    st.markdown("---")
    st.markdown("FitBuddy Voice Assistant")
    st.markdown("Use the **Workout** tab to start a session, and **History** tab to review logs.")

# === Tabs ===
tabs = st.tabs(["🏋️ Workout", "📜 History"])

# === Workout Tab ===
with tabs[0]:
    st.header("🏋️ Workout Session")
    st.info("Demo Mode: Start buttons will work, but logs are already loaded for screenshots.")

# === History Tab ===
with tabs[1]:
    st.header("📜 Workout History")
    df_log = pd.DataFrame([
        {"Date": e["date"], "Muscle": e["muscle"].title(), "Duration (s)": e["total_duration"]}
        for e in st.session_state.workout_log
    ])
    st.subheader("Recent Sessions")
    for entry in reversed(st.session_state.workout_log[-5:]):
        with st.expander(f"{entry['date']} – {entry['muscle'].title()}"):
            for idx, item in enumerate(entry["plan"], start=1):
                st.write(f"{idx}. {item['exercise']}: {item['sets']}×{item['reps']} reps")
            st.write(f"Total Duration: {entry['total_duration']} seconds")

    df = pd.DataFrame([
        {"muscle": e["muscle"], "total_duration": e["total_duration"]}
        for e in st.session_state.workout_log
    ])
    freq = df.groupby("muscle").size().reset_index(name="sessions")
    st.subheader("📊 Workout Frequency")
    chart1 = alt.Chart(freq).mark_bar().encode(
        x=alt.X("muscle:N", title="Muscle Group"),
        y=alt.Y("sessions:Q", title="Number of Sessions"),
        color="muscle:N"
    ).properties(width=600)
    st.altair_chart(chart1, use_container_width=True)

    avgd = df.groupby("muscle").agg(avg_duration=("total_duration", "mean")).reset_index()
    st.subheader("⏱️ Average Duration per Muscle")
    chart2 = alt.Chart(avgd).mark_bar(color="#FF4B4B").encode(
        x=alt.X("muscle:N", title="Muscle Group"),
        y=alt.Y("avg_duration:Q", title="Avg Duration (s)")
    ).properties(width=600)
    st.altair_chart(chart2, use_container_width=True)

    # Optional: Clear Button
    if st.button("🗑️ Clear Workout History"):
        st.session_state.workout_log = []
        st.success("Cleared workout history.")
