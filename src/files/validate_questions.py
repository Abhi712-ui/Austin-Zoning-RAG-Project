import json
import sys
from config import EVAL_DIR, RAW_DIR

VALID_CATEGORIES = set([
    "single_section", 
    "multi_hop", 
    "distractor_adjacent", 
    "unanswerable"
])

with open(EVAL_DIR / "questions.json", encoding="utf-8") as file:
    questions = json.load(file)
    
raw_ids = set(p.stem for p in RAW_DIR.glob("*.html"))
problems = []

for q in questions:
    n = q.get("number", "?")
    
    for section in q.get("expected_sections", []):
        if section not in raw_ids:
            problems.append(f"#{n}: section id not in corpus -> {section}")
            
    if q.get("category") not in VALID_CATEGORIES:
        problems.append(f"#{n}: bad category -> {q.get('category')!r}")
        
    if q.get("answerable"):
        if not q.get("expected_sections"):
            problems.append(f"#{n}: answerable but no expected_sections")
            
    else:
        if q.get("expected_sections"):
            problems.append(f"#{n}: unanswerable but has expected_sections")
            
numbers = [q.get("number") for q in questions]
if len(set(numbers)) != len(numbers):
    problems.append("duplicate question numbers")

for p in problems: print(p)

print(f"\n{len(questions)} questions checked, {len(problems)} problems")
sys.exit(1 if problems else 0)
