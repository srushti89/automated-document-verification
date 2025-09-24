import re
import json
from extract_text import extract_text

# Load DB
def load_dl_db():
    try:
        with open("driving_license_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading DL DB: {e}")
        return []

# Match result with DB
def match_with_db(result, db):
    for record in db:
        if (
            record["dl_number"] == result["dl_number"]
            and record["dob"] == result["dob"]
            and record["name"] == result["name"]
            and record["father_name"] == result["father_name"]
        ):
            return {
                "matched": True,
                "record": record
            }
    return {"matched": False}

# DL validation logic
def validate_text(text):
    result = {
        "dl_number": None,
        "name": None,
        "father_name": None,
        "dob": None,
        "valid": False,
        "message": ""
    }

    if not text:
        result["message"] = "No text extracted"
        return result

    # DL Number (MH52 20240000332 or similar)
    dl_match = re.search(r"\b[A-Z]{2}[0-9]{2}\s?\d{11}\b", text)
    if dl_match:
        result["dl_number"] = dl_match.group().strip()
    else:
        result["message"] = "DL number not found"
        return result

    # DOB
    dob_match = re.search(r"Date of Birth[:\s]*([0-9]{2}-[0-9]{2}-[0-9]{4})", text)
    if dob_match:
        result["dob"] = dob_match.group(1).strip()
    else:
        result["message"] = "Date of Birth not found"
        return result

    # Name
    name_match = re.search(r"Name[:\s]*([A-Z\s]+)", text)
    if name_match:
        result["name"] = name_match.group(1).strip()
    else:
        result["message"] = "Name not found"
        return result

    # Father's Name
    father_match = re.search(r"Son/Daughter/Wife of[:\s]*([A-Z\s]+)", text)
    if father_match:
        result["father_name"] = father_match.group(1).strip()
    else:
        result["message"] = "Father's Name not found"
        return result

    result["valid"] = True
    result["message"] = "Driving License details valid"
    return result

# Direct script run
if __name__ == "__main__":
    img_path = "data/sample_dl.jpg"

    print("\n📄 Step 2: Extracting text...")
    extracted_text = extract_text(img_path)
    print("Extracted Text:\n", extracted_text)

    print("\n📁 Step 3: Loading DB...")
    dl_db = load_dl_db()

    print("\n✅ Step 4: Validating DL...")
    result = validate_text(extracted_text)
    print("Validation Result:\n", json.dumps(result, indent=4, ensure_ascii=False))

    if result["valid"]:
        print("\n🔍 Step 5: Matching with DB...")
        match_result = match_with_db(result, dl_db)
        print("Match Result:\n", json.dumps(match_result, indent=4, ensure_ascii=False))
    else:
        print("\n❌ Driving License not valid.")
