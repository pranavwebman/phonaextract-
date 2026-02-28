import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type
import json
import sys
import time
from datetime import datetime

# ==============================
# Tool Info
# ==============================
TOOL_NAME = "phonaextract"
AUTHOR = "Pranav Krishna (pranavwebman)"

# ==============================
# Typing Animation
# ==============================
def type_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ==============================
# Banner
# ==============================
type_print("\n" + TOOL_NAME + " made by " + AUTHOR)
type_print("=" * 55)

# ==============================
# Input
# ==============================
number_input = input("\nEnter phone number with country code: ")

result = {}
result["input"] = number_input
result["scan_time"] = str(datetime.now())

try:
    parsed = phonenumbers.parse(number_input)

    result["valid"] = phonenumbers.is_valid_number(parsed)
    result["possible"] = phonenumbers.is_possible_number(parsed)

    result["country"] = geocoder.description_for_number(parsed, "en")
    result["carrier"] = carrier.name_for_number(parsed, "en")

    result["timezone"] = list(timezone.time_zones_for_number(parsed))

    type_map = {
        0: "Fixed Line",
        1: "Mobile",
        2: "Fixed Line or Mobile",
        3: "Toll Free",
        4: "Premium Rate",
        5: "Shared Cost",
        6: "VOIP",
        7: "Personal Number",
        8: "Pager",
        9: "UAN",
        10: "Voicemail"
    }

    nt = number_type(parsed)
    result["line_type"] = type_map.get(nt, "Unknown")

    result["international_format"] = phonenumbers.format_number(
        parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )
    result["national_format"] = phonenumbers.format_number(
        parsed, phonenumbers.PhoneNumberFormat.NATIONAL
    )
    result["e164_format"] = phonenumbers.format_number(
        parsed, phonenumbers.PhoneNumberFormat.E164
    )

except Exception as e:
    type_print("\nError parsing number.")
    exit()

# ==============================
# Smart Scoring Logic
# ==============================
score = 0

if result["valid"]:
    score += 40
if result["carrier"]:
    score += 20
if result["line_type"] == "Mobile":
    score += 20
if result["timezone"]:
    score += 20

result["confidence_score"] = str(score) + " / 100"

# ==============================
# Output Animation
# ==============================
type_print("\nScanning...")
time.sleep(1)

type_print("\nScan Complete")
type_print("=" * 55)

for key, value in result.items():
    type_print(f"{key} : {value}")

# ==============================
# Save JSON
# ==============================
output_file = "phonaextract_result.json"
with open(output_file, "w") as f:
    json.dump(result, f, indent=4)

type_print(f"\nResults saved to {output_file}")
