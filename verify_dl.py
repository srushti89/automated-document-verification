import json
import re

def validate_text(text):
    result = {
        "valid": False,
        "name": None,
        "dob": None,
        "dl_number": None,
    }

    # DL number (e.g., MH52 20240000332)
    match = re.search(r'([A-Z]{2}\d{2}\s?\d{11})', text)
    if match:
        result["dl_number"] = match.group(1).strip()

    # Name (assumes it's on line starting with "Name:")
    name_match = re.search(r'Name[:\s]*([A-Z\s]+)\n', text)

    if name_match:
        name = name_match.group(1).strip().replace('\n', ' ')
        result["name"] = re.sub(r'\s+', ' ', name)  # collapse multiple spaces

    # DOB
    dob_match = re.search(r'Date of Birth[:\s]*(\d{2}-\d{2}-\d{4})', text)
    if dob_match:
        result["dob"] = dob_match.group(1).strip()

    if result["dl_number"] and result["name"] and result["dob"]:
        result["valid"] = True

    return result

def load_dl_db():
    try:
        with open("driving_license_db.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading DB:", e)
        return []

def match_with_db(extracted, db):
    for person in db:
        if (
            person.get("dl_number", "").strip().upper() == extracted["dl_number"].strip().upper() and
            person.get("name", "").strip().lower() == extracted["name"].strip().lower() and
            person.get("dob", "").strip() == extracted["dob"].strip()
        ):
            return {"matched": True, "details": person}
    return {"matched": False}
