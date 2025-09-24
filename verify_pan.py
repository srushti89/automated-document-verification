# verify_pan.py

import json
import re

def validate_text(text):
    result = {
        "valid": False,
        "pan_number": None,
        "name": None,
        "father_name": None,
        "dob": None,
    }

    # PAN format: 5 letters, 4 digits, 1 letter
    pan_match = re.search(r'\b([A-Z]{5}[0-9]{4}[A-Z])\b', text)
    if pan_match:
        result["pan_number"] = pan_match.group(1).strip()

    # Name
    name_match = re.search(r'Name[:\s]*([A-Z\s]+)', text)
    if name_match:
        result["name"] = name_match.group(1).strip()

    # Father's Name
    father_match = re.search(r"Father['’]?[s ]+Name[:\s]*([A-Z\s]+)", text)
    if father_match:
        result["father_name"] = father_match.group(1).strip()

    # DOB
    dob_match = re.search(r'Date of Birth[:\s]*(\d{2}/\d{2}/\d{4})', text)
    if dob_match:
        result["dob"] = dob_match.group(1).strip()

    if result["pan_number"] and result["name"] and result["father_name"] and result["dob"]:
        result["valid"] = True

    return result

def load_pan_db():
    with open("pan_db.json", "r") as f:
        return json.load(f)

def match_with_db(extracted, db):
    for person in db:
        if (
            person["pan_number"] == extracted["pan_number"] and
            person["name"].lower() == extracted["name"].lower() and
            person["father_name"].lower() == extracted["father_name"].lower() and
            person["dob"] == extracted["dob"]
        ):
            return {"matched": True, "details": person}
    return {"matched": False}
