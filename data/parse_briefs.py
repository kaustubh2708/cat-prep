import re, csv, io, json

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"

with open(f"{base_dir}/DILR_Knowledge_Brief.txt") as f:
    dilr_txt = f.read()

# Clean page breaks
dilr_lines = [l.strip() for l in dilr_txt.split("\n") if l.strip() and l.strip() != "--- PAGE ---"]

dilr_topics = {
    "2.": "Charts, Graphs & Visual DI",
    "3.": "Quant-Based LR & Numerical Optimization",
    "4.": "Grids, Matrices & Conditional Distribution",
    "5.": "Scheduling, Queues & Dynamic Processes",
    "6.": "Networks, Routes & Spatial Geometry",
    "7.": "Games, Tournaments, Set Theory & Logic"
}

cur_topic = None
in_table = False
raw_rows = []

for l in dilr_lines:
    for prefix, tname in dilr_topics.items():
        if l.startswith(prefix) and ("Sets)" in l or "Logic" in l or "Processes" in l):
            cur_topic = tname
            in_table = False
    if l.startswith("Year & Slot,Questions,Set Theme"):
        in_table = True
        continue
    if l.startswith("Prerequisite Knowledge") or l.startswith("8. Study"):
        in_table = False
        continue
    if in_table and cur_topic:
        if re.match(r"^202[1-5]\s+Slot\s+[123I]+,", l):
            raw_rows.append([cur_topic, l])
        elif raw_rows:
            raw_rows[-1][1] += " " + l

dilr_sets = []
for topic, line in raw_rows:
    reader = csv.reader(io.StringIO(line))
    row = next(reader)
    if len(row) >= 6:
        ys, qrange, theme, diff, exp_time, mechanic = row[0], row[1], row[2], row[3], row[4], ",".join(row[5:])
        m_ys = re.match(r"(202[1-5])\s+Slot\s+(\d+)", ys)
        yr = int(m_ys.group(1))
        slot = int(m_ys.group(2))
        m_qr = re.search(r"Q(\d+)[–-](\d+)", qrange)
        q_start, q_end = int(m_qr.group(1)), int(m_qr.group(2))
        dilr_sets.append({
            "year": yr,
            "slot": slot,
            "qStart": q_start,
            "qEnd": q_end,
            "topic": topic,
            "theme": theme.strip(),
            "difficulty": diff.strip(),
            "expectedTime": exp_time.strip(),
            "coreMechanic": mechanic.strip()
        })

print(f"Parsed {len(dilr_sets)} DILR sets across 15 slots!")
by_ys = {}
for s in dilr_sets:
    by_ys.setdefault((s["year"], s["slot"]), []).append((s["qStart"], s["qEnd"], s["difficulty"]))
for ys in sorted(by_ys.keys()):
    print(f"  {ys[0]} S{ys[1]}: {sorted(by_ys[ys])}")

with open(f"{base_dir}/dilr_sets_meta.json", "w") as f:
    json.dump(dilr_sets, f, indent=2)
