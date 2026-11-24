import re, csv, io, json

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"

with open(f"{base_dir}/QA_Knowledge_Brief.txt") as f:
    qa_txt = f.read()

qa_lines = [l.strip() for l in qa_txt.split("\n") if l.strip() and l.strip() != "--- PAGE ---"]

qa_domains = {
    "2.2": "Arithmetic",
    "3.2": "Algebra",
    "4.2": "Geometry & Mensuration",
    "5.2": "Number Systems",
    "6.2": "Modern Math"
}

cur_domain = None
in_table = False
raw_rows = []

for l in qa_lines:
    for prefix, dname in qa_domains.items():
        if l.startswith(prefix) and "Breakdown" in l:
            cur_domain = dname
            in_table = False
    if l.startswith("Year & Slot,Q. No.,Subtopic"):
        in_table = True
        continue
    if re.match(r"^[234567]\.[13]\s+", l) or l.startswith("7. Phased"):
        in_table = False
        continue
    if in_table and cur_domain:
        if re.match(r"^202[1-5]\s+Slot\s+I{1,3},", l):
            raw_rows.append([cur_domain, l])
        elif raw_rows:
            raw_rows[-1][1] += " " + l

ROMAN = {"I": 1, "II": 2, "III": 3}
qa_items = []
for domain, line in raw_rows:
    reader = csv.reader(io.StringIO(line))
    row = next(reader)
    m_ys = re.match(r"(202[1-5])\s+Slot\s+(I{1,3})", row[0].strip())
    yr = int(m_ys.group(1))
    slot = ROMAN[m_ys.group(2)]
    q_str = row[1].strip()
    q_num = int(q_str[1:]) if q_str.startswith("Q") and q_str[1:].isdigit() else None
    subtopic = row[2].strip()
    # Find difficulty and est_time from the end or regex
    joined_rest = ",".join(row[3:])
    m_end = re.search(r",(Easy|Medium|Hard),([\d.]+\s*min)\s*$", joined_rest)
    if m_end:
        diff = m_end.group(1)
        est_time = m_end.group(2)
        hook = joined_rest[:m_end.start()].strip().strip('"')
    else:
        diff = "Medium"
        est_time = "2.0 min"
        hook = joined_rest.strip().strip('"')
    qa_items.append({
        "year": yr,
        "slot": slot,
        "qNum": q_num,
        "domain": domain,
        "subtopic": subtopic,
        "hook": hook,
        "difficulty": diff,
        "expectedTime": est_time
    })

print(f"Parsed {len(qa_items)} QA items from QA Knowledge Brief!")
by_ys = {}
for it in qa_items:
    by_ys.setdefault((it["year"], it["slot"]), []).append(it)
for ys in sorted(by_ys.keys()):
    with_q = sum(1 for x in by_ys[ys] if x["qNum"] is not None)
    print(f"  {ys[0]} S{ys[1]}: {len(by_ys[ys])} items ({with_q} with explicit Q#)")

with open(f"{base_dir}/qa_items_meta.json", "w") as f:
    json.dump(qa_items, f, indent=2)
