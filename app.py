from flask import Flask, render_template, request

app = Flask(__name__)

# Simple clinical drug knowledge base (starter version)
DRUG_DB = {
    "metformin": {
        "class": "Antidiabetic (Biguanide)",
        "ckd_warning": "Avoid if eGFR < 30 (risk of lactic acidosis)",
        "interaction": "Avoid with contrast media and severe renal impairment"
    },
    INTERACTIONS = {
    ("ibuprofen", "lisinopril"): {
        "severity": "High",
        "message": "Increased risk of acute kidney injury (AKI)",
        "advice": "Avoid combination or monitor renal function closely"
    },
    ("ibuprofen", "metformin"): {
        "severity": "Moderate",
        "message": "Risk of reduced kidney function affecting metformin clearance",
        "advice": "Use cautiously in CKD patients"
    }
} = {
    ("ibuprofen", "lisinopril"): {
        "severity": "High",
        "message": "Increased risk of acute kidney injury (AKI)",
        "advice": "Avoid combination or monitor renal function closely"
    },
    ("ibuprofen", "metformin"): {
        "severity": "Moderate",
        "message": "Risk of reduced kidney function affecting metformin clearance",
        "advice": "Use cautiously in CKD patients"
    }
} = {
    ("ibuprofen", "lisinopril"): {
        "severity": "High",
        "message": "Increased risk of acute kidney injury (AKI)",
        "advice": "Avoid combination or monitor renal function closely"
    },
    ("ibuprofen", "metformin"): {
        "severity": "Moderate",
        "message": "Risk of reduced kidney function affecting metformin clearance",
        "advice": "Use cautiously in CKD patients"
    }
}
    "ibuprofen": {
        "class": "NSAID",
        "ckd_warning": "Avoid in CKD patients (reduces renal blood flow)",
        "interaction": "Increases risk of AKI when combined with ACE inhibitors/diuretics"
    },
    "lisinopril": {
        "class": "ACE inhibitor",
        "ckd_warning": "Use cautiously in CKD; monitor creatinine & potassium",
        "interaction": "Risk of hyperkalemia with potassium supplements"
    }
}

def analyze_prescription(text):
    text = text.lower()
    response = []
    found_drugs = []

    # Detect drugs
    for drug, info in DRUG_DB.items():
        if drug in text:
            found_drugs.append(drug)
            response.append(f"""
Drug: {drug.title()}
Class: {info['class']}
CKD Alert: {info['ckd_warning']}
Interactions: {info['interaction']}
""")

    # Check interactions
    if len(found_drugs) >= 2:
        for (d1, d2), info in INTERACTIONS.items():
            if d1 in found_drugs and d2 in found_drugs:
                response.append(f"""
⚠️ INTERACTION DETECTED
Drugs: {d1.title()} + {d2.title()}
Severity: {info['severity']}
Risk: {info['message']}
Advice: {info['advice']}
""")

    if not response:
        return "No known drug found. Try: metformin, ibuprofen, lisinopril"

    return "\n".join(response)

    for drug, info in DRUG_DB.items():
        if drug in text:
            response.append(f"""
Drug: {drug.title()}
Class: {info['class']}
CKD Alert: {info['ckd_warning']}
Interactions: {info['interaction']}
""")

    if not response:
        return "No known drug found. Try: metformin, ibuprofen, lisinopril"

    return "\n".join(response)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def get_response():
    data = request.get_json()

    user_input = data.get("message", "")

    reply = analyze_prescription(user_input)

    return {"response": reply}


if __name__ == "__main__":
    app.run(debug=True)
