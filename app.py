from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Basic clinical knowledge base (fallback)
drug_db = {
    "paracetamol": "Used for pain and fever. Safe in CKD at normal doses.",
    "metformin": "Used for diabetes. Avoid if eGFR < 30.",
    "ibuprofen": "NSAID. Avoid in CKD due to kidney risk.",
    "amoxicillin": "Antibiotic. Dose adjustment may be needed in CKD."
}

# 🧠 AI-style response generator (rule + intelligence hybrid)
def ai_pharmacy_engine(message):

    msg = message.lower()

    # 1. Direct drug match
    for drug in drug_db:
        if drug in msg:
            return f"""
💊 Drug: {drug.title()}
📘 Info: {drug_db[drug]}
⚠️ Clinical Note: Always consider patient kidney function before dosing.
"""

    # 2. CKD-related query
    if "ckd" in msg or "kidney" in msg:
        return """
🧠 CKD Pharmacology Insight:
- Avoid nephrotoxic drugs (e.g., NSAIDs like ibuprofen)
- Adjust doses based on eGFR
- Monitor creatinine and electrolytes regularly
"""

    # 3. General greeting
    if "hello" in msg or "hi" in msg:
        return "Hello 👋 I am your AI Pharmacy Assistant. Ask me about any drug or CKD dosing."

    # 4. Default AI response
    return """
🤖 AI Pharmacy Assistant:
I can help with:
- Drug information
- CKD dose adjustments
- Safety warnings

Try asking: "metformin in CKD" or "ibuprofen safety"
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    user_message = request.json["message"]

    response = ai_pharmacy_engine(user_message)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)