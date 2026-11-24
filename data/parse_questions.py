import json, re

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"

SLOT_RANGES = {
    2021: {1: (1, 15, 66), 2: (16, 30, 66), 3: (31, 45, 66)},
    2022: {1: (1, 16, 66), 2: (17, 33, 66), 3: (34, 49, 66)},
    2023: {1: (1, 13, 66), 2: (14, 26, 66), 3: (27, 41, 66)},
    2024: {1: (2, 18, 68), 2: (21, 38, 68), 3: (41, 57, 68)},
    2025: {1: (2, 19, 68), 2: (21, 38, 68), 3: (39, 55, 68)},
}

def get_section(yr, qnum):
    if qnum <= 24:
        return "VARC"
    if yr <= 2023:
        return "DILR" if qnum <= 44 else "QA"
    else:
        return "DILR" if qnum <= 46 else "QA"

def is_header_line(txt):
    t = txt.strip()
    if re.match(r"^(?:Actual CAT \d{4}|Slot\s*[-–]?\s*I{1,3}|\d+)$", t):
        return True
    if re.match(r"^Actual CAT \d{4}\s+Slot\s*[-–]?\s*I{1,3}", t):
        return True
    if re.match(r"^Slot\s*[-–]?\s*I{1,3}\s+\d+$", t):
        return True
    if re.match(r"^Actual CAT \d{4}\s+\d+$", t):
        return True
    return False

for yr in [2021, 2022, 2023, 2024, 2025]:
    with open(f"{base_dir}/CAT_{yr}_lines.json") as f:
        pages = json.load(f)
    for slot, (p_start, p_end, max_q) in SLOT_RANGES[yr].items():
        slot_lines = []
        for p in pages[p_start-1:p_end]:
            pnum = p["page"]
            ph = p["height"]
            for l in p["lines"]:
                if is_header_line(l["text"]):
                    continue
                slot_lines.append({
                    "page": pnum,
                    "top": l["top"],
                    "bottom": l["bottom"],
                    "x0": l["x0"],
                    "height": ph,
                    "text": l["text"].strip()
                })
        # Find question starts sequentially 1..max_q
        found_qs = {}
        next_q = 1
        for idx, l in enumerate(slot_lines):
            txt = l["text"]
            if yr in [2021, 2023]:
                m = re.match(r"^Question No\.\s*:\s*(\d+)\b", txt)
                if m:
                    qn = int(m.group(1))
                    found_qs[qn] = idx
            else:
                # In 2022, 2024, 2025, question numbers are at left margin (x0 < 85) formatted as "1. " or "25. "
                # Wait: inside jumbled sentences (1. 2. 3. 4.) or options (1. 2. 3. 4.), x0 is usually indented (> 85)
                # EXCEPT when question header itself is "18. 1. Fish skin..."
                m = re.match(r"^(\d{1,2})\.\s+(.*)", txt)
                if m:
                    qn = int(m.group(1))
                    if qn == next_q and l["x0"] < 95:
                        found_qs[qn] = idx
                        next_q += 1

        missing = [q for q in range(1, max_q+1) if q not in found_qs]
        print(f"CAT {yr} Slot {slot}: Found {len(found_qs)}/{max_q} questions. Missing: {missing}")
