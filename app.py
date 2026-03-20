from flask import Flask, render_template, request

app = Flask(__name__)

DRUG_DB = {
    "metformin": {
        "class": "Antidiabetic (Biguanide)",
        "ckd_warning": "Avoid if eGFR < 30",
        "interaction": "Avoid in severe renal impairment"
    },
    "ibuprofen": {
        "class": "NSAID",
        "ckd_warning": "Avoid in CKD patients",
        "interaction": "Risk of kidney injury with ACE inhibitors"
    },
    "lisinopril": {
        "class": "ACE inhibitor",
        "ckd_warning": "Monitor kidney function",
        "interaction": "Risk of high potassium"
    }
}

INTERACTIONS = {
    ("ibuprofen", "lisinopril"): {
        "severity": "High",
        "message": "Risk of kidney injury",
        "advice": "Avoid or monitor closely"
    },
    ("ibuprofen", "metformin"): {
        "severity": "Moderate",
        "message": "Reduced kidney function risk",
        "advice": "Use cautiously"
    }
}

def analyze_prescription(text):
    text = text.lower()
    response = []
    found = []

    for drug in DRUG_DB:
        if drug in text:
            found.append(drug)
            info = DRUG_DB[drug]
            response.append(f"{drug.title()} - {info['ckd_warning']}")

    for (d1, d2), info in INTERACTIONS.items():
        if d1 in found and d2 in found:
            response.append(f"⚠️ {d1} + {d2}: {info['message']} ({info['severity']})")

    if not response:
        return "No drug found"

    return "\n".join(response)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data.get("message", "")
    return {"response": analyze_prescription(user_input)}

if __name__ == "__main__":
    app.run(debug=True)
