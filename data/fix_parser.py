import json, re

with open("/Users/kaustubhsingh/Developer/Cat exam prep/data/process_all_questions.py") as f:
    code = f.read()

# Replace parse_options_from_lines and classify_varc and fuzzy matcher with improved versions
new_parse_opts = '''def parse_options_from_lines(lines_text, yr, section, qnum, pre_text=""):
    full = "\\n".join(lines_text)
    full = re.sub(r"^(?:Question No\\.\\s*:\\s*\\d+\\s*|\\d{1,2}\\.\\s+)", "", full.strip())

    # If full starts immediately with "1. Option 1 2. Option 2..." (like 2022 S1 Q22, Q24 where paragraph was in pre_text)
    if re.match(r"^1\\.\\s*Option\\s*1\\s+2\\.\\s*Option\\s*2", full):
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
    m_abcd = list(re.finditer(r"(?:^|\\s|\\n)([A-D])[)\\.](?:\\s+|(?=\\d)|$)", full))
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
    m_mixed = list(re.finditer(r"(?:^|\\s|\\n)(A|[2-4])[)\\.](?:\\s+|$)", full))
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
    m_1234 = list(re.finditer(r"(?:^|\\s|\\n)([1-4])\\.(?:\\s+|$)", full))
    if len(m_1234) >= 4:
        idx_1 = None
        for i in range(len(m_1234) - 3):
            if [m_1234[i+j].group(1) for j in range(4)] == ["1", "2", "3", "4"]:
                idx_1 = i
        if idx_1 is not None:
            after_4 = full[m_1234[idx_1 + 3].end():]
            if not re.search(r"(?:^|\\s)5\\.\\s+", after_4):
                stem_candidate = full[:m_1234[idx_1].start()].strip()
                if len(stem_candidate) > 4:
                    opts = []
                    for j in range(4):
                        start_o = m_1234[idx_1 + j].end()
                        end_o = m_1234[idx_1 + j + 1].start() if j < 3 else len(full)
                        otxt = full[start_o:end_o].strip() or f"Option {['A','B','C','D'][j]} (see visual view)"
                        opts.append({"id": ["A", "B", "C", "D"][j], "text": otxt})
                    return stem_candidate, opts

    return full.strip(), []'''

# Update process_all_questions.py
start_marker = "def parse_options_from_lines("
end_marker = "print(\"Helper definitions syntax check OK\")"
s_pos = code.index(start_marker)
e_pos = code.index(end_marker)
code = code[:s_pos] + new_parse_opts + "\n\n" + code[e_pos:]
code = code.replace("stem, opts = parse_options_from_lines(raw_q_lines_text, yr, sec, qn)", "stem, opts = parse_options_from_lines(raw_q_lines_text, yr, sec, qn, pre_text)")

# Also fix classify_varc so 2024/2025 VA questions interleaved in Q1..Q16 are classified as VA, not RC!
old_varc_check = 'if qnum <= 16 or "based on the passage" in d_low or "from the passage" in d_low or "in the passage" in d_low or "read the passage" in directions_txt.lower():'
new_varc_check = 'if ("summary" not in d_low and "captures the essence" not in d_low and "jumbled" not in d_low and "properly sequenced" not in d_low and "missing in the paragraph" not in d_low and "odd sentence" not in d_low and "odd one out" not in d_low) and ((qnum <= 16 and "four sentences" not in d_low and "five sentences" not in d_low) or "based on the passage" in d_low or "from the passage" in d_low or "in the passage" in d_low or "read the passage" in directions_txt.lower()):'
code = code.replace(old_varc_check, new_varc_check)

# Also fix fuzzy matching stop words for unnumbered QA items in 2021 S2/S3 and 2023 S2/S3
old_fuzzy = '''                    s_words = set(re.findall(r"[a-zA-Z0-9]+", stem.lower()))
                    for it in qa_unnumbered[(yr, slot)]:
                        h_words = set(re.findall(r"[a-zA-Z0-9]+", it["hook"].lower()))
                        overlap = len(s_words & h_words)'''
new_fuzzy = '''                    STOP = {"the","and","for","with","that","this","from","are","was","were","has","have","had","not","all","its","his","her","can","will","one","two","three","four","five","six","find","then","when","if","in","on","at","to","of","is","be","by","as","or","an","equal","equals","value","number","total"}
                    s_words = set(re.findall(r"[a-zA-Z0-9]+", stem.lower())) - STOP
                    for it in qa_unnumbered[(yr, slot)]:
                        h_words = set(re.findall(r"[a-zA-Z0-9]+", it["hook"].lower())) - STOP
                        overlap = len(s_words & h_words)'''
code = code.replace(old_fuzzy, new_fuzzy)

with open("/Users/kaustubhsingh/Developer/Cat exam prep/data/process_all_questions.py", "w") as f:
    f.write(code)

print("Updated process_all_questions.py")
