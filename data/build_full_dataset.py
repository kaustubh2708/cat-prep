import json, re

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"

with open(f"{base_dir}/dilr_sets_meta.json") as f:
    dilr_sets_meta = json.load(f)

# Fix 2021 S3 question ranges to match actual CAT 2021 Slot 3 PDF
for s in dilr_sets_meta:
    if s["year"] == 2021 and s["slot"] == 3:
        if "Amal, Bimal, Komal" in s["theme"]:
            s["qStart"], s["qEnd"] = 31, 36
        elif "Four Employees" in s["theme"]:
            s["qStart"], s["qEnd"] = 37, 40
        elif "Testing 50 ml" in s["theme"]:
            s["qStart"], s["qEnd"] = 41, 44

with open(f"{base_dir}/qa_items_meta.json") as f:
    qa_items_meta = json.load(f)

SLOT_RANGES = {
    2021: {1: (1, 15, 66), 2: (16, 30, 66), 3: (31, 45, 66)},
    2022: {1: (1, 16, 66), 2: (17, 33, 66), 3: (34, 49, 66)},
    2023: {1: (1, 13, 66), 2: (14, 26, 66), 3: (27, 41, 66)},
    2024: {1: (2, 18, 68), 2: (21, 38, 68), 3: (41, 57, 68)},
    2025: {1: (2, 19, 68), 2: (21, 38, 68), 3: (39, 55, 68)},
}

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

def is_section_line(txt):
    t = txt.strip()
    return bool(re.match(r"^(?:Section|SECTION)\s*[-:]", t))

def is_directions_line(txt):
    t = txt.strip()
    return bool(re.match(r"^(?:DIRECTIONS?|Passage)\b", t))

def compute_slices(lines_subset):
    if not lines_subset:
        return []
    by_page = {}
    for l in lines_subset:
        p = l["page"]
        if p not in by_page:
            by_page[p] = {"min_top": l["top"], "max_bottom": l["bottom"], "height": l["height"]}
        else:
            by_page[p]["min_top"] = min(by_page[p]["min_top"], l["top"])
            by_page[p]["max_bottom"] = max(by_page[p]["max_bottom"], l["bottom"])
    slices = []
    pages_sorted = sorted(by_page.keys())
    for idx, p in enumerate(pages_sorted):
        info = by_page[p]
        h = info["height"]
        # Add generous padding for embedded diagrams/equations
        top_pad = 12
        bot_pad = 24
        t_pct = max(4.0, round((info["min_top"] - top_pad) / h * 100, 1))
        b_pct = min(96.0, round((info["max_bottom"] + bot_pad) / h * 100, 1))
        slices.append({"page": p, "topPct": t_pct, "bottomPct": b_pct})
    return slices

all_questions = []

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
                m = re.match(r"^(\d{1,2})\.\s+(.*)", txt)
                if m:
                    qn = int(m.group(1))
                    if qn == next_q and l["x0"] < 95:
                        found_qs[qn] = idx
                        next_q += 1

        # Determine boundary of each question (before next question or directions/section header that precedes next question)
        q_bounds = {}
        for qn in range(1, max_q + 1):
            start_idx = found_qs[qn]
            if qn < max_q:
                next_start = found_qs[qn + 1]
                # Walk backwards from next_start to see if there are DIRECTIONS/Section/Passage lines belonging to next question
                end_idx = next_start
                scan = next_start - 1
                # In 2022/2024/2025, a passage or DILR set intro sits between DIRECTIONS and next_start!
                # Let's find the earliest DIRECTIONS or Section header between start_idx and next_start
                for k in range(start_idx + 1, next_start):
                    if is_section_line(slot_lines[k]["text"]) or is_directions_line(slot_lines[k]["text"]):
                        end_idx = k
                        break
            else:
                end_idx = len(slot_lines)
            q_bounds[qn] = (start_idx, end_idx)

        for qn in range(1, max_q + 1):
            s_idx, e_idx = q_bounds[qn]
            q_lines = slot_lines[s_idx:e_idx]
            # Also check pre-question lines (between previous question's e_idx and this question's s_idx)
            prev_e_idx = q_bounds[qn - 1][1] if qn > 1 else 0
            pre_lines = slot_lines[prev_e_idx:s_idx]
            all_questions.append({
                "year": yr,
                "slot": slot,
                "qNum": qn,
                "preLines": pre_lines,
                "qLines": q_lines
            })

print("Total extracted raw questions:", len(all_questions))
