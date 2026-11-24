import json, re
from PIL import Image
import numpy as np

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"
pub_pages_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/public/pages"
_page_img_cache = {}

def get_page_gray(yr, pnum):
    key = (yr, pnum)
    if key not in _page_img_cache:
        im = Image.open(f"{pub_pages_dir}/{yr}/page_{pnum}.webp").convert("L")
        _page_img_cache[key] = np.array(im)
    return _page_img_cache[key]

with open(f"{base_dir}/dilr_sets_meta.json") as f:
    dilr_sets_meta = json.load(f)

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

def is_section_line(txt):
    t = txt.strip()
    return bool(re.match(r"^(?:Section|SECTION)\s*[-:]", t))

def is_directions_line(txt):
    t = txt.strip()
    return bool(re.match(r"^(?:DIRECTIONS?|DIRECTION)\b", t)) or bool(re.match(r"^Passage\s*[-–]\s*[IVX]+$", t))

def parse_options_from_lines(lines_text, yr, section, qnum, pre_text=""):
    full = "\n".join(lines_text)
    full = re.sub(r"^(?:Question No\.\s*:\s*\d+\s*|\d{1,2}\.\s+)", "", full.strip())

    # If full starts immediately with "1. Option 1 2. Option 2..." (like 2022 S1 Q22, Q24 where paragraph was in pre_text)
    if re.match(r"^1\.\s*Option\s*1\s+2\.\s*Option\s*2", full):
        opts = [{"id": ["A", "B", "C", "D"][j], "text": f"Option {j+1}"} for j in range(4)]
        return pre_text, opts

    # Check if this is a Para Jumble or Odd One Out (TITA)
    d_comb = (pre_text + " " + full).lower()
    is_pj_or_ooo = any(k in d_comb for k in [
        "properly sequenced", "rearrange the statements", "sequence of four numbers",
        "sequence of the four numbers", "odd one out", "odd sentence"
    ])
    if is_pj_or_ooo:
        return full.strip(), []

    # 1) Standard A) B) C) D) or A. B. C. D. (allowing B.15 without space, empty text after D), or 2024-S2-Q3 A,B,C,A typo, or A,2,3,4 mixed typo)
    m_abcd = list(re.finditer(r"(?:^|(?<=[\s\n]))([A-D])[)\.](?=\s|\d|$)", full))
    if len(m_abcd) >= 4:
        idx_a = None
        for i in range(len(m_abcd) - 3):
            seq = [m_abcd[i+j].group(1) for j in range(4)]
            if seq == ["A", "B", "C", "D"] or seq == ["A", "B", "C", "A"]:
                idx_a = i
        if idx_a is not None:
            stem = full[:m_abcd[idx_a].start()].strip()
            opts = []
            for j in range(4):
                start_o = m_abcd[idx_a + j].end()
                end_o = m_abcd[idx_a + j + 1].start() if j < 3 else len(full)
                otxt = full[start_o:end_o].strip()
                if not otxt:
                    otxt = f"Option {['A','B','C','D'][j]} (see equation in visual view)"
                opts.append({"id": ["A", "B", "C", "D"][j], "text": otxt})
            return stem, opts

    # 2) Mixed typo: "A. ... 2. ... 3. ... 4. ..." or "A) ... 2. ... 3. ... 4. ..." (e.g. 2024-S3-Q56, Q61, 2025-S2-Q49)
    m_mixed = list(re.finditer(r"(?:^|(?<=[\s\n]))(A|[2-4])[)\.](?=\s|\d|$)", full))
    if len(m_mixed) >= 4:
        for i in range(len(m_mixed) - 3):
            if [m_mixed[i+j].group(1) for j in range(4)] == ["A", "2", "3", "4"]:
                stem = full[:m_mixed[i].start()].strip()
                opts = []
                for j in range(4):
                    start_o = m_mixed[i + j].end()
                    end_o = m_mixed[i + j + 1].start() if j < 3 else len(full)
                    otxt = full[start_o:end_o].strip() or f"Option {['A','B','C','D'][j]} (see visual view)"
                    opts.append({"id": ["A", "B", "C", "D"][j], "text": otxt})
                return stem, opts

    # 3) Numbered options: 1. ... 2. ... 3. ... 4. ...
    m_1234 = list(re.finditer(r"(?:^|(?<=[\s\n]))(?<!Day )([1-4])\.(?=\s|$)", full))
    if len(m_1234) >= 4:
        idx_1 = None
        for i in range(len(m_1234) - 3):
            if [m_1234[i+j].group(1) for j in range(4)] == ["1", "2", "3", "4"]:
                idx_1 = i
        if idx_1 is not None:
            after_4 = full[m_1234[idx_1 + 3].end():]
            if not re.search(r"(?:^|\s)5\.\s+", after_4):
                stem_candidate = full[:m_1234[idx_1].start()].strip()
                if len(stem_candidate) > 4:
                    opts = []
                    for j in range(4):
                        start_o = m_1234[idx_1 + j].end()
                        end_o = m_1234[idx_1 + j + 1].start() if j < 3 else len(full)
                        otxt = full[start_o:end_o].strip() or f"Option {['A','B','C','D'][j]} (see visual view)"
                        opts.append({"id": ["A", "B", "C", "D"][j], "text": otxt})
                    return stem_candidate, opts

    return full.strip(), []

print("Helper definitions syntax check OK")

def classify_qa_fallback(text):
    t = text.lower()
    if any(k in t for k in ["triangle", "circle", "rectangle", "trapezium", "rhombus", "hexagon", "octagon", "polygon", "chord", "tangent", "angle", "altitude", "median", "inscribed", "perimeter", "area of", "coordinates", "vertices", "parallelogram", "sphere"]):
        sub = "Triangles & Polygons"
        if "circle" in t or "chord" in t or "tangent" in t: sub = "Circles & Tangents"
        elif "coordinate" in t or "vertices" in t or "line" in t: sub = "Coordinate Geometry"
        elif "rhombus" in t or "trapezium" in t or "parallelogram" in t or "rectangle" in t: sub = "Quadrilaterals & Mensuration"
        return "Geometry & Mensuration", sub, "Medium", "1.75 min", "Draw a clean diagram and apply area-ratio, similarity, or standard right-triangle/rhombus properties."
    if any(k in t for k in ["log", "root", "equation", "sequence", "arithmetic progression", "geometric progression", "f(x)", "g(x)", "inequalit", "|x", "|n", "polynomial", "quadratic"]):
        sub = "Equations & Functions"
        if "log" in t: sub = "Logarithms & Exponents"
        elif "progression" in t or "sequence" in t or "group" in t: sub = "Sequences & Series"
        elif "|" in t or "inequalit" in t: sub = "Modulus & Inequalities"
        elif "root" in t or "quadratic" in t: sub = "Quadratic Equations"
        return "Algebra", sub, "Medium", "2.0 min", "Look for structural identities (Vieta's formulas, log base change, completing the square, or modulus distance)."
    if any(k in t for k in ["remainder", "divisible", "divisor", "factor", "three-digit", "four-digit", "4-digit", "3-digit", "natural number", "prime", "sum of digits", "hcf", "lcm"]):
        sub = "Divisibility & Factors"
        if "digit" in t: sub = "Digits & Place Value"
        elif "remainder" in t: sub = "Remainders & Modular Cyclicity"
        return "Number Systems", sub, "Easy", "1.5 min", "Use prime factorization, place-value expansion (100a+10b+c), or Euler/modular cyclicity."
    if any(k in t for k in ["ways of distributing", "chosen from", "how many numbers", "non-repeating", "onto", "sandwich", "identical balloons"]):
        return "Modern Math", "Combinatorics & Set Theory", "Easy", "1.5 min", "Apply standard counting templates: Stars-and-Bars for identical items, or complement counting for 'at least once'."
    # Default Arithmetic
    sub = "Percentages, Ratios & P&L"
    if any(k in t for k in ["work", "paint", "pipe", "tank", "days"]): sub = "Time, Work & Pipes"
    elif any(k in t for k in ["train", "speed", "km/h", "km/hr", "boat", "track", "escalator", "clock"]): sub = "Time, Speed & Distance"
    elif any(k in t for k in ["interest", "compounded", "invest", "loan"]): sub = "Simple & Compound Interest"
    elif any(k in t for k in ["mixture", "alloy", "milk", "syrup", "acid", "indigo", "solution"]): sub = "Mixtures & Alligation"
    elif any(k in t for k in ["average", "mean"]): sub = "Averages & Alligation"
    return "Arithmetic", sub, "Medium", "1.75 min", "Translate multi-stage wording into a clean ratio, weighted average (alligation), or efficiency-unit equation."

def classify_varc(qnum, directions_txt, q_txt, set_passage_txt):
    d_low = (directions_txt + " " + q_txt).lower()
    if ("summary" not in d_low and "captures the essence" not in d_low and "jumbled" not in d_low and "properly sequenced" not in d_low and "missing in the paragraph" not in d_low and "odd sentence" not in d_low and "odd one out" not in d_low) and ((qnum <= 16 and "four sentences" not in d_low and "five sentences" not in d_low) or "based on the passage" in d_low or "from the passage" in d_low or "in the passage" in d_low or "read the passage" in directions_txt.lower()):
        if "summary" in d_low or "captures the essence" in d_low:
            pass
        elif "jumbled" in d_low or "properly sequenced" in d_low or "missing in the paragraph" in d_low or "odd sentence" in d_low or "odd one out" in d_low:
            pass
        else:
            # RC question
            qt = q_txt.lower()
            if "except" in qt or "not true" in qt or "cannot be inferred" in qt or "false" in qt:
                sub = "RC - Inference & Elimination (EXCEPT)"
                mech = "Eliminate options directly supported by the text; watch for scope shifts or extreme quantifiers."
            elif "weaken" in qt or "strengthen" in qt or "invalidate" in qt or "undermine" in qt or "complement" in qt or "assumption" in qt:
                sub = "RC - Critical Reasoning (Strengthen/Weaken)"
                mech = "Identify the author's core causal claim first, then test which option breaks or reinforces that link."
            elif "main" in qt or "central" in qt or "purpose" in qt or "summar" in qt or "gist" in qt or "keywords" in qt or "tone" in qt:
                sub = "RC - Main Idea, Purpose & Tone"
                mech = "Track the author's thesis across paragraph transitions; avoid options that focus on a single paragraph's example."
            else:
                sub = "RC - Direct & Contextual Inference"
                mech = "Locate the specific anchor paragraph and verify every clause of the option against the author's qualifiers."
            return "Reading Comprehension", sub, "Medium", "1.75 min", mech

    # Verbal Ability (VA)
    if "odd one out" in d_low or "odd sentence" in d_low or "five jumbled" in d_low or "five sentences" in d_low:
        return "Verbal Ability", "VA - Odd Sentence Out (TITA)", "Medium", "1.5 min", "Find the mandatory pair and overarching theme of 4 sentences first; the odd sentence usually shifts timeframe, scope, or angle."
    if "missing in the paragraph" in d_low or "blank (option" in d_low or "decide where" in d_low:
        return "Verbal Ability", "VA - Sentence Insertion (Para Completion)", "Easy", "1.25 min", "Use pronoun referents ('this', 'these', 'such') and contrast markers ('however', 'yet') before and after each blank."
    if "properly sequenced" in d_low or "four sentences" in d_low or "rearrange the statements" in d_low:
        return "Verbal Ability", "VA - Para Jumbles (TITA)", "Medium", "1.75 min", "Lock the independent opening sentence and mandatory pronoun/chronological pairs before typing the 4-digit sequence."
    return "Verbal Ability", "VA - Para Summary", "Easy", "1.5 min", "Capture the author's main claim + primary support; eliminate options that add new claims, distort tone, or are too narrow."

# Index DILR sets by (year, slot, qNum)
dilr_lookup = {}
for idx_s, s in enumerate(dilr_sets_meta):
    for q in range(s["qStart"], s["qEnd"] + 1):
        dilr_lookup[(s["year"], s["slot"], q)] = s

# Index QA items by (year, slot, qNum) and unnumbered list per (year, slot)
qa_explicit = {}
qa_unnumbered = {}
for it in qa_items_meta:
    if it["qNum"] is not None:
        qa_explicit[(it["year"], it["slot"], it["qNum"])] = it
    else:
        qa_unnumbered.setdefault((it["year"], it["slot"]), []).append(it)

dataset = []

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
                    if qn == next_q and l["x0"] < 75:
                        found_qs[qn] = idx
                        next_q += 1

        q_bounds = {}
        for qn in range(1, max_q + 1):
            start_idx = found_qs[qn]
            if qn < max_q:
                next_start = found_qs[qn + 1]
                end_idx = next_start
                for k in range(start_idx + 1, next_start):
                    if is_section_line(slot_lines[k]["text"]) or is_directions_line(slot_lines[k]["text"]):
                        end_idx = k
                        break
            else:
                end_idx = len(slot_lines)
            q_bounds[qn] = (start_idx, end_idx)

        # Build contiguous visual slices for each question block
        # Note: if an equation image is below the text of qLines, extending the bottom of qLines on its last page up to the next line's top (if on the same page) guarantees capturing it!
        def get_contiguous_slices(start_i, end_i):
            if start_i >= end_i:
                return []
            first_l = slot_lines[start_i]
            p_s = first_l["page"]
            h_s = first_l["height"]
            y_s_pct = max(6.8, (first_l["top"] - 6) / h_s * 100)

            if end_i < len(slot_lines):
                next_l = slot_lines[end_i]
                p_e = next_l["page"]
                h_e = next_l["height"]
                y_e_pct = max(6.8, (next_l["top"] - 3) / h_e * 100)
            else:
                last_l = slot_lines[end_i - 1]
                p_e = last_l["page"]
                y_e_pct = 93.2

            slices = []
            for p in range(p_s, p_e + 1):
                t_pct = y_s_pct if p == p_s else 6.8
                b_pct = y_e_pct if p == p_e else 93.2
                if b_pct - t_pct < 1.2:
                    continue
                arr = get_page_gray(yr, p)
                ih, iw = arr.shape
                r0 = max(0, int(ih * t_pct / 100))
                r1 = min(ih, int(ih * b_pct / 100))
                if r1 <= r0 + 4:
                    continue
                sub_img = arr[r0:r1, int(iw * 0.04):int(iw * 0.96)]
                non_white = np.where((sub_img < 245).sum(axis=1) > 3)[0]
                if len(non_white) == 0:
                    continue
                actual_t = max(4.5, round(((r0 + non_white[0]) / ih * 100) - 0.8, 1))
                actual_b = min(95.5, round(((r0 + non_white[-1]) / ih * 100) + 1.0, 1))
                if actual_b - actual_t >= 1.5:
                    slices.append({"page": p, "topPct": actual_t, "bottomPct": actual_b})
            return slices

        # Track current shared context (for RC passages and DILR sets)
        cur_context_text = ""
        cur_context_slices = []
        cur_directions = ""
        cur_set_id = None
        cur_set_range = None

        for qn in range(1, max_q + 1):
            sec = get_section(yr, qn)
            s_idx, e_idx = q_bounds[qn]
            prev_e_idx = q_bounds[qn - 1][1] if qn > 1 else 0
            pre_lines = [l for l in slot_lines[prev_e_idx:s_idx] if not is_section_line(l["text"])]
            q_lines = slot_lines[s_idx:e_idx]

            q_slices = get_contiguous_slices(s_idx, e_idx)
            pre_slices = get_contiguous_slices(prev_e_idx, s_idx) if pre_lines else []

            pre_text = "\n".join(l["text"] for l in pre_lines).strip()
            raw_q_lines_text = [l["text"] for l in q_lines]
            stem, opts = parse_options_from_lines(raw_q_lines_text, yr, sec, qn, pre_text)

            # Handle RC and DILR shared context
            if sec == "DILR":
                d_meta = dilr_lookup.get((yr, slot, qn))
                if d_meta:
                    q_start, q_end = d_meta["qStart"], d_meta["qEnd"]
                    cur_set_id = f"{yr}-S{slot}-DILR-{q_start}"
                    cur_set_range = f"Q{q_start}–Q{q_end}"
                    if qn == q_start:
                        if yr in [2021, 2023]:
                            # In 2021 & 2023, the DILR set intro + chart is inside Q_start!
                            # Split stem into set intro + actual question sentence (last paragraph/line)
                            stem_lines = [x.strip() for x in stem.split("\n") if x.strip()]
                            if len(stem_lines) > 2:
                                cur_context_text = "\n".join(stem_lines[:-1])
                                stem = stem_lines[-1]
                            else:
                                cur_context_text = stem
                            cur_context_slices = pre_slices + q_slices
                            cur_directions = pre_text
                        else:
                            cur_context_text = pre_text
                            cur_context_slices = pre_slices
                            cur_directions = pre_text.split("\n")[0] if pre_text else ""
            elif sec == "VARC":
                # Check if this question starts a new RC passage or VA question
                if pre_text:
                    cur_directions = pre_text
                if yr in [2021, 2023] and qn in [1, 5, 9, 13]:
                    rc_num = (qn - 1) // 4 + 1
                    cur_set_id = f"{yr}-S{slot}-RC{rc_num}"
                    cur_set_range = f"Q{qn}–Q{qn+3}"
                    # In 2021 & 2023, RC passage is inside Q1, Q5, Q9, Q13 before the last question sentence!
                    stem_lines = [x.strip() for x in stem.split("\n") if x.strip()]
                    # Find where the question prompt starts at the end of stem_lines (usually last 1 or 2 lines)
                    q_prompt_start = len(stem_lines) - 1
                    if len(stem_lines) >= 2 and len(stem_lines[-1]) < 95 and not stem_lines[-2].endswith("."):
                        q_prompt_start = len(stem_lines) - 2
                    cur_context_text = "\n".join(stem_lines[:q_prompt_start])
                    stem = " ".join(stem_lines[q_prompt_start:])
                    cur_context_slices = q_slices
                elif yr in [2021, 2023] and qn <= 16:
                    # Continues current RC passage
                    pass
                elif yr == 2022 and qn <= 16:
                    if qn in [1, 5, 9, 13]:
                        rc_num = (qn - 1) // 4 + 1
                        cur_set_id = f"{yr}-S{slot}-RC{rc_num}"
                        cur_set_range = f"Q{qn}–Q{qn+3}"
                        cur_context_text = pre_text
                        cur_context_slices = pre_slices
                elif yr in [2024, 2025]:
                    # In 2024 and 2025, RC passages and VA questions are mixed! Check if pre_text has "questions X to Y" or "questions X-Y"
                    m_range = re.search(r"questions?\s+(\d+)\s*(?:to|[-–])\s*(\d+)", pre_text, re.I)
                    if m_range and len(pre_text) > 400:
                        q_s, q_e = int(m_range.group(1)), int(m_range.group(2))
                        cur_set_id = f"{yr}-S{slot}-RC-{q_s}"
                        cur_set_range = f"Q{q_s}–Q{q_e}"
                        cur_context_text = pre_text
                        cur_context_slices = pre_slices
                    elif pre_text and ("DIRECTIONS" in pre_text or "DIRECTION" in pre_text):
                        # Standalone VA question (or 2 VA questions sharing a 1-line direction)
                        if len(pre_text) < 400:
                            cur_set_id = None
                            cur_set_range = None
                            cur_context_text = pre_text
                            cur_context_slices = []
                else:
                    # 2021, 2022, 2023 Q17..24 are standalone VA questions
                    cur_set_id = None
                    cur_set_range = None
                    cur_context_text = pre_text
                    cur_context_slices = []
            else:
                # QA
                cur_set_id = None
                cur_set_range = None
                cur_context_text = ""
                cur_context_slices = []

            # Determine question type (MCQ vs TITA)
            q_type = "MCQ" if len(opts) == 4 else "TITA"

            # Attach metadata (Topic, Subtopic, Difficulty, Expected Time, Hook, Core Mechanic)
            if sec == "DILR":
                d_meta = dilr_lookup.get((yr, slot, qn))
                topic = d_meta["topic"]
                subtopic = d_meta["theme"]
                diff = d_meta["difficulty"]
                exp_time = d_meta["expectedTime"]
                hook = d_meta["theme"]
                mechanic = d_meta["coreMechanic"]
            elif sec == "QA":
                q_meta = qa_explicit.get((yr, slot, qn))
                if not q_meta and (yr, slot) in qa_unnumbered:
                    # Try fuzzy matching against unnumbered hooks for this (yr, slot)
                    best_it = None
                    best_score = 0
                    STOP = {"the","and","for","with","that","this","from","are","was","were","has","have","had","not","all","its","his","her","can","will","one","two","three","four","five","six","find","then","when","if","in","on","at","to","of","is","be","by","as","or","an","equal","equals","value","number","total"}
                    s_words = set(re.findall(r"[a-zA-Z0-9]+", stem.lower())) - STOP
                    for it in qa_unnumbered[(yr, slot)]:
                        h_words = set(re.findall(r"[a-zA-Z0-9]+", it["hook"].lower())) - STOP
                        overlap = len(s_words & h_words)
                        if overlap > best_score:
                            best_score = overlap
                            best_it = it
                    if best_it and best_score >= 2:
                        q_meta = best_it
                if q_meta:
                    topic = q_meta["domain"]
                    subtopic = q_meta["subtopic"]
                    diff = q_meta["difficulty"]
                    exp_time = q_meta["expectedTime"]
                    hook = q_meta["hook"]
                    _, _, _, _, mechanic = classify_qa_fallback(stem + " " + subtopic)
                else:
                    topic, subtopic, diff, exp_time, mechanic = classify_qa_fallback(stem)
                    hook = stem[:90] + ("..." if len(stem) > 90 else "")
            else:
                # VARC
                topic, subtopic, diff, exp_time, mechanic = classify_varc(qn, cur_directions, stem, cur_context_text)
                if cur_set_id:
                    hook = f"Reading Comprehension ({cur_set_range})"
                else:
                    hook = subtopic.replace("VA - ", "")

            if diff == "Easy":
                role = "Round 1 Priority (Must-Solve Anchor)"
            elif diff == "Medium":
                role = "Round 2 Core (Score Differentiator)"
            else:
                role = "Round 3 / Strategic Skip"

            dataset.append({
                "id": f"{yr}-S{slot}-Q{qn}",
                "year": yr,
                "slot": slot,
                "qNum": qn,
                "section": sec,
                "type": q_type,
                "setId": cur_set_id,
                "setQRange": cur_set_range,
                "topic": topic,
                "subtopic": subtopic,
                "difficulty": diff,
                "expectedTime": exp_time,
                "strategyRole": role,
                "hook": hook,
                "coreMechanic": mechanic,
                "directions": cur_directions,
                "contextText": cur_context_text if cur_set_id else "",
                "contextSlices": cur_context_slices if cur_set_id else [],
                "questionText": stem,
                "options": opts,
                "questionSlices": q_slices,
                "page": q_slices[0]["page"] if q_slices else p_start
            })

with open(f"{base_dir}/questions_1002.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"Successfully built questions_1002.json with {len(dataset)} questions!")
by_sec = {}
by_type = {}
by_diff = {}
for q in dataset:
    by_sec[q["section"]] = by_sec.get(q["section"], 0) + 1
    by_type[q["type"]] = by_type.get(q["type"], 0) + 1
    by_diff[q["difficulty"]] = by_diff.get(q["difficulty"], 0) + 1
print("By Section:", by_sec)
print("By Type:", by_type)
print("By Difficulty:", by_diff)
