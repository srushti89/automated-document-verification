import re
import json
from extract_text import extract_text

# Load DB
def load_pan_db():
    try:
        with open("pan_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading PAN DB: {e}")
        return []

# Match result with DB
def match_with_db(result, db):
    for record in db:
        if (
            record["pan_number"] == result["pan_number"]
            and record["dob"] == result["dob"]
            and record["name"] == result["name"]
            and record["father_name"] == result["father_name"]
        ):
            return {
                "matched": True,
                "record": record
            }
    return {"matched": False}

# PAN validation logic
def validate_text(text):
    result = {
        "pan_number": None,
        "name": None,
        "father_name": None,
        "dob": None,
        "valid": False,
        "message": ""
    }

    if not text:
        result["message"] = "No text extracted"
        return result

    # PAN Number
    pan_match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)
    if pan_match:
        result["pan_number"] = pan_match.group()
    else:
        result["message"] = "PAN number not found"
        return result

    # DOB
    dob_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
    if dob_match:
        result["dob"] = dob_match.group()
    else:
        result["message"] = "Date of Birth not found"
        return result

    # Name
    name_match = re.search(r"नाम\s*/\s*Name\s*\n(.*)", text)
    if name_match:
        result["name"] = name_match.group(1).strip()
    else:
        # Try fallback line-based search
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "Name" in line and i + 1 < len(lines):
                result["name"] = lines[i + 1].strip()
                break

    # Father's Name
    father_match = re.search(r"पिता का नाम\s*/\s*Father's Name\s*\n(.*)", text)
    if father_match:
        result["father_name"] = father_match.group(1).strip()
    else:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "Father" in line and i + 1 < len(lines):
                result["father_name"] = lines[i + 1].strip()
                break

    if not result["name"] or not result["father_name"]:
        result["message"] = "Name or Father's Name not found"
        return result

    result["valid"] = True
    result["message"] = "PAN details valid"
    return result

# Direct script run
if __name__ == "__main__":
    img_path = "data/sample_pan.jpg"

    print("\n📄 Step 2: Extracting text...")
    extracted_text = extract_text(img_path)
    print("Extracted Text:\n", extracted_text)

    print("\n📁 Step 3: Loading DB...")
    pan_db = load_pan_db()

    print("\n✅ Step 4: Validating PAN...")
    result = validate_text(extracted_text)
    print("Validation Result:\n", json.dumps(result, indent=4, ensure_ascii=False))

    if result["valid"]:
        print("\n🔍 Step 5: Matching with DB...")
        match_result = match_with_db(result, pan_db)
        print("Match Result:\n", json.dumps(match_result, indent=4, ensure_ascii=False))
    else:
        print("\n❌ PAN not valid.")
