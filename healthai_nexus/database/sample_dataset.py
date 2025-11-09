"""Sample medical dataset for testing and training"""

SAMPLE_CASES = [
    {
        "symptoms": "chest pain, shortness of breath, sweating",
        "category": "cardiac",
        "severity": "high"
    },
    {
        "symptoms": "severe headache, vision changes, nausea",
        "category": "neurological",
        "severity": "high"
    },
    {
        "symptoms": "fatigue, weight gain, feeling cold",
        "category": "endocrine",
        "severity": "medium"
    },
    {
        "symptoms": "persistent cough, fever, body aches",
        "category": "respiratory",
        "severity": "medium"
    },
    {
        "symptoms": "skin rash, itching, redness",
        "category": "dermatological",
        "severity": "low"
    }
]

MEDICAL_KNOWLEDGE = {
    "hypertension": {
        "definition": "High blood pressure >130/80 mmHg",
        "symptoms": ["headache", "dizziness", "chest pain"],
        "treatment": ["lifestyle changes", "ACE inhibitors", "diuretics"]
    },
    "diabetes": {
        "definition": "Elevated blood glucose levels",
        "symptoms": ["increased thirst", "frequent urination", "fatigue"],
        "treatment": ["diet control", "metformin", "insulin"]
    },
    "migraine": {
        "definition": "Severe recurring headaches",
        "symptoms": ["throbbing headache", "nausea", "light sensitivity"],
        "treatment": ["triptans", "NSAIDs", "rest"]
    }
}
