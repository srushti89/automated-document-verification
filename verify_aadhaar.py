import re
import json
from extract_text import extract_text

# Load DB
def load_aadhaar_db():
    try:
        with open("aadhaar_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading DB: {e}")
        return []

# Match result with DB
def match_with_db(result, db):
    for record in db:
        if (
            record["aadhaar_number"] == result["aadhaar_number"]
            and record["dob"] == result["dob"]
            and (
                result["name_english"] == record.get("name_english") or
                result["name_marathi"] == record.get("name_marathi")
            )
        ):
            return {
                "matched": True,
                "record": record
            }
    return {"matched": False}

# Aadhaar validation logic
def validate_text(text):
    result = {
        "aadhaar_number": None,
        "dob": None,
        "name_marathi": None,
        "name_english": None,
        "valid": False,
        "message": ""
    }

    if not text:
        result["message"] = "No text extracted"
        return result

    # Aadhaar Number
    uid_match = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
    if uid_match:
        result["aadhaar_number"] = uid_match.group()
    else:
        result["message"] = "Aadhaar number not found"
        return result

    # DOB (only when labeled)
    dob_line = next((line for line in text.splitlines() if 'DOB' in line.upper()), None)
    if dob_line:
        dob_match = re.search(r"\d{2}/\d{2}/\d{4}", dob_line)
        if dob_match:
            result["dob"] = dob_match.group()
    if not result["dob"]:
        result["message"] = "Date of Birth not found"
        return result

    # Name: extract lines between "Government of India" and DOB line
    lines = text.splitlines()
    name_lines = []
    capture = False
    for line in lines:
        if any(x in line for x in ["भारत सरकार", "Government of India"]):
            capture = True
            continue
        if "DOB" in line:
            break
        if capture and line.strip():
            name_lines.append(line.strip())

    if name_lines:
        result["name_marathi"] = name_lines[0] if len(name_lines) > 0 else None
        result["name_english"] = name_lines[1] if len(name_lines) > 1 else None

    if not result["name_marathi"] and not result["name_english"]:
        result["message"] = "Name not found"
        return result

    result["valid"] = True
    result["message"] = "Aadhaar details valid"
    return result

# Direct script run
if __name__ == "__main__":
    img_path = "data/sample_aadhaar.jpg"

    print("\n📄 Step 2: Extracting text...")
    extracted_text = extract_text(img_path)
    print("Extracted Text:\n", extracted_text)

    print("\n📁 Step 3: Loading DB...")
    aadhaar_db = load_aadhaar_db()

    print("\n✅ Step 4: Validating Aadhaar...")
    result = validate_text(extracted_text)
    print("Validation Result:\n", json.dumps(result, indent=4, ensure_ascii=False))

    if result["valid"]:
        print("\n🔍 Step 5: Matching with DB...")
        match_result = match_with_db(result, aadhaar_db)
        print("Match Result:\n", json.dumps(match_result, indent=4, ensure_ascii=False))
    else:
        print("\n❌ Aadhaar not valid.")
