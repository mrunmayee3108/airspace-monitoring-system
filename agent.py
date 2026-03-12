import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env")
else:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

try:
    df = pd.read_csv("final_airspace_data.csv")
    print("✅ Dataset loaded successfully")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    df = pd.DataFrame() 

def build_airspace_context():
    total_objects = len(df)
    
    anomalies = 0
    if "anomaly" in df.columns:
        anomalies = df["anomaly"].astype(str).str.strip().eq("-1").sum()

    high_risk = 0
    if "risk_level" in df.columns:
        high_risk = df["risk_level"].astype(str).str.strip().str.lower().eq("high").sum()

    return f"""
    Airspace Summary:
    - Total objects: {total_objects}
    - Anomalies: {anomalies}
    - High risk: {high_risk}
    
    Capabilities: Anomaly Detection, Risk Scoring, Trajectory Prediction.
    """

def ask_agent(question, history):
    context = build_airspace_context()
    messages = [
        {"role": "user", "parts": [f"You are an airspace AI. Data:\n{context}"]},
        {"role": "model", "parts": ["Ready. How can I help with the airspace data?"]}
    ]

    for q, a in history:
        messages.append({"role": "user", "parts": [q]})
        messages.append({"role": "model", "parts": [a]})

    messages.append({"role": "user", "parts": [question]})

    try:
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"API Error: {e}"

if __name__ == "__main__":
    history = []
    print(f"\n🚀 Airspace AI Active (Using {MODEL_NAME})")
    
    while True:
        user_input = input("Ask: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        ans = ask_agent(user_input, history)
        history.append((user_input, ans))
        print(f"\nAI: {ans}\n")