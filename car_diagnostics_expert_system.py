"""
====================================================================
 CAR DIAGNOSTICS EXPERT SYSTEM
====================================================================

WHAT PROBLEM DOES IT SOLVE?
----------------------------
Normal car owners aksar nahi jaante ke unki gaadi mein aane wali
alag alag "symptoms" (jaise strange noise, warning lights, smoke)
ka matlab kya hai aur kitni urgency hai. Ye system un symptoms ko
input le kar, ek "virtual mechanic expert" ki tarah possible
diagnosis, confidence level, urgency aur suggested action batata
hai — bina mechanic ke paas jaaye pehli understanding dene ke liye.

WHAT INFORMATION DOES IT USE?
-------------------------------
- User se input: car ke symptoms (jaise "engine won't start",
  "clicking sound", "temperature warning light", etc.)
- Ek pehle se defined "Knowledge Base" (rules list) jo real
  automotive experts ki knowledge par based hai — har rule mein
  symptoms, diagnosis, confidence score, urgency aur recommended
  action diya gaya hai.

WHAT DECISION DOES IT MAKE?
-----------------------------
System input symptoms ko knowledge base ke rules se match karta
hai aur decide karta hai:
  1. Kaunsi diagnosis (problem) sabse zyada possible hai
  2. Kitni confidence (%) hai us diagnosis par
  3. Kitni urgency hai (Low / Medium / High / Critical)
  4. User ko kya action leni chahiye (e.g. mechanic ko dikhana,
     turant gaadi rokna, part check karna)

WHERE IS EXPERT KNOWLEDGE USED?
----------------------------------
Expert knowledge is system ki "rules" list (self.rules) mein
encode ki gayi hai. Har rule ek real mechanic/automotive expert
ki experience ko represent karta hai: "agar ye symptoms saath
mein aayen, to yeh problem hone ka strong chance hai, is
confidence ke saath, aur yeh action lo." Ye Inference Engine
(diagnose function) rules ko symptoms se match karke "reasoning"
karta hai, jaise koi expert insaan sochta.

IS IT RULE-BASED, ML-BASED, OR HYBRID?
------------------------------------------
Ye purely RULE-BASED expert system hai:
  - Koi machine learning model nahi hai (koi training data se
    "seekhna" nahi ho raha).
  - Sari knowledge fixed IF-THEN type rules mein hardcoded hai
    (symptom match -> diagnosis + confidence + action).
  - Confidence scores bhi expert opinion se manually diye gaye
    hain, statistically calculate nahi kiye gaye.
  - Isliye ye Traditional Expert System hai, ML-based ya
    Hybrid nahi.
====================================================================
"""


class CarDiagnosticSystem:
    def __init__(self):
        # ---------------- KNOWLEDGE BASE ----------------
        # Ye rules automotive experts ki knowledge represent karte hain.
        self.rules = [
            {
                'condition': ["engine won't start", 'clicking sound'],
                'diagnosis': 'Dead Battery or Faulty Starter',
                'confidence': 0.90,
                'action': 'Check battery voltage. Try jump-start. If still fails, test starter motor.',
                'urgency': 'Medium'
            },
            {
                'condition': ["engine won't start", 'no sound'],
                'diagnosis': 'Dead Battery or Blown Fuse',
                'confidence': 0.85,
                'action': 'Check battery terminals for corrosion. Inspect main fuses.',
                'urgency': 'Medium'
            },
            {
                'condition': ['engine overheating', 'temperature warning light'],
                'diagnosis': 'Coolant Leak or Thermostat Failure',
                'confidence': 0.88,
                'action': 'Check coolant level. Inspect for leaks. Replace thermostat if stuck closed.',
                'urgency': 'High'
            },
            {
                'condition': ['engine overheating', 'steam from hood'],
                'diagnosis': 'Severe Coolant Loss or Radiator Failure',
                'confidence': 0.92,
                'action': 'STOP DRIVING IMMEDIATELY. Check radiator and hoses. Do not open hot radiator cap.',
                'urgency': 'Critical'
            },
            {
                'condition': ['brake pedal feels soft', 'spongy brakes'],
                'diagnosis': 'Air in Brake Lines or Low Brake Fluid',
                'confidence': 0.87,
                'action': 'Check brake fluid level. Bleed brake lines to remove air.',
                'urgency': 'High'
            },
            {
                'condition': ['brake pedal vibrates', 'pulsation when braking'],
                'diagnosis': 'Warped Brake Rotors',
                'confidence': 0.85,
                'action': 'Inspect brake rotors. Resurface or replace if warped.',
                'urgency': 'Medium'
            },
            {
                'condition': ['check engine light on', 'rough idle'],
                'diagnosis': 'Faulty Spark Plugs or Oxygen Sensor',
                'confidence': 0.80,
                'action': 'Scan for OBD-II codes. Replace spark plugs or oxygen sensor as needed.',
                'urgency': 'Medium'
            },
            {
                'condition': ['check engine light on', 'reduced fuel efficiency'],
                'diagnosis': 'Faulty Oxygen Sensor or MAF Sensor',
                'confidence': 0.83,
                'action': 'Scan for OBD-II codes. Clean or replace MAF sensor. Replace O2 sensor.',
                'urgency': 'Low'
            },
            {
                'condition': ['car pulls to one side', 'uneven tire wear'],
                'diagnosis': 'Wheel Alignment Issue or Tire Pressure Imbalance',
                'confidence': 0.86,
                'action': 'Check tire pressure. Get wheel alignment done.',
                'urgency': 'Medium'
            },
            {
                'condition': ['strange noise when turning', 'clicking sound'],
                'diagnosis': 'Worn CV Joints',
                'confidence': 0.84,
                'action': 'Inspect CV joints and boots. Replace if damaged.',
                'urgency': 'Medium'
            },
            {
                'condition': ['excessive exhaust smoke', 'blue smoke'],
                'diagnosis': 'Oil Burning – Worn Piston Rings or Valve Seals',
                'confidence': 0.88,
                'action': 'Check oil consumption. Engine overhaul may be needed.',
                'urgency': 'High'
            },
            {
                'condition': ['excessive exhaust smoke', 'black smoke'],
                'diagnosis': 'Rich Fuel Mixture – Faulty Fuel Injector or MAF Sensor',
                'confidence': 0.82,
                'action': 'Clean fuel injectors. Check MAF sensor. Scan for codes.',
                'urgency': 'Medium'
            },
            {
                'condition': ['ac not cooling', 'weak airflow'],
                'diagnosis': 'Low Refrigerant or Clogged Cabin Filter',
                'confidence': 0.79,
                'action': 'Check cabin air filter. Recharge AC system if low on refrigerant.',
                'urgency': 'Low'
            },
            {
                'condition': ['transmission slipping', 'delayed gear shift'],
                'diagnosis': 'Low Transmission Fluid or Worn Clutch',
                'confidence': 0.85,
                'action': 'Check transmission fluid level and condition. Inspect clutch (manual) or solenoid (auto).',
                'urgency': 'High'
            },
            {
                'condition': ['steering wheel shakes', 'vibration at high speed'],
                'diagnosis': 'Unbalanced Wheels or Worn Suspension',
                'confidence': 0.81,
                'action': 'Get wheels balanced. Inspect suspension components.',
                'urgency': 'Medium'
            }
        ]

        # Symptom menu mapping (user-friendly numbered list)
        self.symptom_map = {
            1: ["engine won't start", 'clicking sound'],
            2: ["engine won't start", 'no sound'],
            3: ['engine overheating', 'temperature warning light'],
            4: ['engine overheating', 'steam from hood'],
            5: ['brake pedal feels soft', 'spongy brakes'],
            6: ['brake pedal vibrates', 'pulsation when braking'],
            7: ['check engine light on', 'rough idle'],
            8: ['check engine light on', 'reduced fuel efficiency'],
            9: ['car pulls to one side', 'uneven tire wear'],
            10: ['strange noise when turning', 'clicking sound'],
            11: ['excessive exhaust smoke', 'blue smoke'],
            12: ['excessive exhaust smoke', 'black smoke'],
            13: ['ac not cooling', 'weak airflow'],
            14: ['transmission slipping', 'delayed gear shift'],
            15: ['steering wheel shakes', 'vibration at high speed']
        }

    # ---------------- USER INPUT (INTERFACE) ----------------
    def show_menu(self):
        print("\n" + "=" * 60)
        print("🚗 Car Diagnostics Expert System")
        print("=" * 60)
        print("\nCommon Symptoms (enter numbers separated by comma):")
        print("1.  Engine won't start + clicking sound")
        print("2.  Engine won't start + no sound")
        print("3.  Engine overheating + temperature warning light")
        print("4.  Engine overheating + steam from hood")
        print("5.  Brake pedal feels soft + spongy brakes")
        print("6.  Brake pedal vibrates + pulsation when braking")
        print("7.  Check engine light on + rough idle")
        print("8.  Check engine light on + reduced fuel efficiency")
        print("9.  Car pulls to one side + uneven tire wear")
        print("10. Strange noise when turning + clicking sound")
        print("11. Excessive exhaust smoke + blue smoke")
        print("12. Excessive exhaust smoke + black smoke")
        print("13. AC not cooling + weak airflow")
        print("14. Transmission slipping + delayed gear shift")
        print("15. Steering wheel shakes + vibration at high speed")
        print("0.  Exit")

    def get_user_symptoms(self):
        self.show_menu()
        while True:
            choice = input("\nEnter symptom number(s) (e.g., 1,3,7): ").strip()
            if choice == '0':
                return []
            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                if all(1 <= i <= 15 for i in indices):
                    return indices
                print("❌ Please enter numbers between 1 and 15.")
            except ValueError:
                print("❌ Invalid input. Enter numbers only.")

    # ---------------- INFERENCE ENGINE ----------------
    def diagnose(self, symptom_indices):
        if not symptom_indices:
            print("\n👋 Thank you for using the Car Diagnostics Expert System!")
            return

        selected_symptoms = []
        for idx in symptom_indices:
            selected_symptoms.extend(self.symptom_map[idx])

        print("\n" + "=" * 60)
        print("🔍 DIAGNOSIS REPORT")
        print("=" * 60)
        print(f"\nReported Symptoms: {', '.join(selected_symptoms).title()}")
        print("-" * 60)

        matches = []
        for rule in self.rules:
            if any(sym in rule['condition'] for sym in selected_symptoms):
                match_score = len(set(rule['condition']) & set(selected_symptoms)) / len(rule['condition'])
                if match_score > 0.5:  # at least 50% match
                    matches.append({
                        'diagnosis': rule['diagnosis'],
                        'confidence': rule['confidence'],
                        'action': rule['action'],
                        'urgency': rule['urgency']
                    })

        matches.sort(key=lambda x: x['confidence'], reverse=True)

        if matches:
            print(f"\n✅ Found {len(matches)} possible issue(s):\n")
            urgency_emoji = {'Critical': '🚨', 'High': '⚠️', 'Medium': '⚡', 'Low': 'ℹ️'}
            for i, match in enumerate(matches, 1):
                print(f"{i}. {match['diagnosis']}")
                print(f"   Confidence: {match['confidence'] * 100:.0f}%")
                print(f"   Urgency: {urgency_emoji.get(match['urgency'], '')} {match['urgency']}")
                print(f"   Action: {match['action']}")
                print()
        else:
            print("\n❌ No matching diagnosis found.")
            print("💡 Tip: Try selecting more specific symptoms or consult a mechanic.")

        print("=" * 60)
        print("⚠️ DISCLAIMER: This is an AI assistant. Always verify with a certified mechanic.")
        print("=" * 60)

    # ---------------- MAIN LOOP ----------------
    def run(self):
        while True:
            symptoms = self.get_user_symptoms()
            if not symptoms:
                print("\n👋 Goodbye! Drive safe! 🚗")
                break
            self.diagnose(symptoms)

            again = input("\nRun another diagnosis? (y/n): ").strip().lower()
            if again != 'y':
                print("\n👋 Thank you for using the Car Diagnostics Expert System! Drive safe! 🚗")
                break


if __name__ == "__main__":
    system = CarDiagnosticSystem()
    system.run()
