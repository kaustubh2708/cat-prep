import json, re

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"

with open(f"{base_dir}/questions_1002.json") as f:
    questions = json.load(f)

# 1. Build structured Knowledge Briefs (DILR, QA, and VARC) from the user's systematic plan PDFs
knowledge_briefs = {
    "DILR": {
        "title": "DILR 40-Minute Calibration & Topic Toolkit (66 Sets)",
        "overview": "Across CAT 2021–2025, DILR shifted from 4 sets (20 Qs) in 2021–2023 to 5 sets (22 Qs) in 2024–2025 under the same 40-minute clock. Solving 2 to 3 well-chosen sets with near-100% accuracy consistently yields 99+ percentile and outperforms attempting 4 sets partially.",
        "calibration": [
            {"tier": "Easy (7–9 min)", "role": "Mandatory Round-1 Pick", "desc": "Clear entry point, minimal branching cases, direct arithmetic or single-table deduction. Target 100% accuracy."},
            {"tier": "Medium (10–13 min)", "role": "Round-2 Core Differentiator", "desc": "Requires 2–3 logical steps, a clean visual/algebraic setup, or careful case elimination. Pair 1–2 Easy sets with 1–2 Medium sets."},
            {"tier": "Hard (14–18 min)", "role": "Strategic Skip / Last-Pick", "desc": "Multi-layered casework, non-obvious invariants, or heavy simulation across rounds. Skip during the first 30 minutes."}
        ],
        "categories": [
            {
                "name": "Charts, Graphs & Visual DI",
                "count": 13,
                "profile": "Mostly Easy–Medium; highest-ROI first-pick candidates",
                "rules": [
                    "Candlestick Plots (2024 S1): Green (bullish) means Close > Open (bottom = Open, top = Close); Red (bearish) means Close < Open (top = Open, bottom = Close). Wicks mark High and Low.",
                    "Gantt / Schedule Bars (2021 S2 & S3): Duration = Right Endpoint − Left Endpoint. Always verify whether endpoints are date-differences or inclusive.",
                    "Bubble & Scatter Plots (2022 S2, 2024 S2, 2025 S2): When bubble area is proportional to a variable, compare visually or via radius squared (A ∝ r²), never radius alone. Convert % change axes into fraction multipliers (+25% = ×5/4, -20% = ×4/5).",
                    "Step-Line Charts (2025 S3): A vertical jump at time t marks completion; horizontal plateau length before the jump equals time taken. Subtract Visual jumps from All jumps to isolate Number-based puzzles.",
                    "Stock-Flow Attrition Identity (2022 S2): Employees Lost in Year t = Start_t + New Hires_t − Start_{t+1}.",
                    "Relative Bases Trap (2024 S3): Population ∝ (GDP fraction) / (GDP per capita fraction); unknown base constants for Country 9 & 10 cancel out in cross-country comparisons."
                ]
            },
            {
                "name": "Quant-Based LR & Numerical Optimization",
                "count": 14,
                "profile": "Balanced Easy to Hard; largest category in 2023–2025 (11 sets)",
                "rules": [
                    "Mean ↔ Sum Conversion: Immediately convert means into integer sums (Sum = Mean × N). E.g., in 2023 S1, a mean of 3.4 across 5 ratings gives an exact sum of 17.",
                    "2-Day Moving Averages (2023 S2): S_{k-1} + S_k = 2A_k. Subtract consecutive equations: S_{k+1} − S_{k-1} = 2(A_{k+1} − A_k) to chain all odd/even days from a single anchor.",
                    "Median, Mode & Range of 5 Sorted Integers (x₁ ≤ x₂ ≤ x₃ ≤ x₄ ≤ x₅): Median is x₃, Range is x₅ − x₁. A unique mode must appear at least twice while all others appear fewer times.",
                    "Prime Factorization (2022 S1): Divide funding by 1,000 and factor into primes (2, 3, 5, 7, 11, 13) to reveal exact token subsets immediately.",
                    "Modular / Multiple Constraints (2024 S3 Food Grains): Carbs = multiples of 5, Protein/Fat/Other = multiples of 4 with row sum = 100 narrows every missing row to 1–2 valid tuples.",
                    "Flow Conservation (2025 S3 Calls & Trade): Total outgoing from Group X to Group Y must equal total incoming at Y from X. Build a directed matrix and place all zeros first."
                ]
            },
            {
                "name": "Grids, Matrices & Conditional Distribution",
                "count": 12,
                "profile": "Mostly Medium–Hard; structured deduction via anchor clues",
                "rules": [
                    "The Anchor-First Rule: Never process clues top-to-bottom. Scan first for universal exclusions ('never', 'none', 'only'), exact row/column totals, and extremes (10 and 1 in 2024 S2 grid).",
                    "Sub-Grid Partitioning (2021 S1 Journal): When 3+ dimensions exist (Author × Country × Area × Issue), build a static master profile table first before mapping onto the schedule grid.",
                    "Envy-Free Bundle Logic (2021 S2): If X does not envy Y, X's valuation of X's bundle ≥ X's valuation of Y's bundle. Each person must receive at least one of their top 2–3 valued items.",
                    "Partial Determinacy Trap: When two symmetric cells/people can swap without violating any rule, document the swap as (X/Y) and move directly to the questions—CAT specifically tests 'For how many slots can values be uniquely determined?'"
                ]
            },
            {
                "name": "Scheduling, Queues & Dynamic Processes",
                "count": 10,
                "profile": "Medium–Hard; requires strict time-indexed bookkeeping",
                "rules": [
                    "State-Transition Tables: Always draw a time-indexed table (columns = rounds/quarters/slots, rows = players/counters). Never track state changes mentally.",
                    "Minimum Fleet Size Formula (2022 S1 Metro): Track how many departures occur from Terminal A before the first 6:00 am train completes its trip (T_trip) + mandatory rest (15 min) at B and returns to A.",
                    "FIFO Counter Queues (2023 S1 VPO): Track counter free-times rather than applicant arrival times. Start time = max(arrival_time, next_counter_free_time).",
                    "Segment-Flow Accounting (2025 S1 Train): Occupancy(k → k+1) = Occupancy(k-1 → k) + Boardings at k − Alightings at k.",
                    "Tie-Break Direction Trap (2021 S3 Javelin vs 2025 S1 InnovateX): Underline whether ties preserve prevailing rank or favor the latest quarter's higher rating before simulating Round 1."
                ]
            },
            {
                "name": "Networks, Routes & Spatial Geometry",
                "count": 6,
                "profile": "Easy–Hard; graph degrees, Manhattan distances & modular circles",
                "rules": [
                    "Longest Simple Path (No Repeated Vertices, 2024 S2): Check degree-2 vertices and bottlenecks first; use Pythagoras (300-400-500 triangles) for diagonal walkways.",
                    "Longest Trail (No Repeated Edges, 2024 S2): Count vertex degrees. By Euler's theorem, any vertex with odd degree (except start/end) forces at least one incident path to go unused.",
                    "Manhattan Grid Distance (2024 S3 ATMs): Road distance between (R_i, V_j) and (R_m, V_n) is |R_i − R_m| + |V_j − V_n|. Use the 12 km clue to lock corners first.",
                    "Circular Seating & Modular Jumps (2025 S1 & S3): Label 7 seats 0..6 (mod 7). Immediate left/right = ±1, second left/right = ±2. Sum net displacement across rounds."
                ]
            },
            {
                "name": "Games, Tournaments, Set Theory & Logic",
                "count": 11,
                "profile": "High variance: Set-theory matrices are Easy 7-min wins; betting games are Hard",
                "rules": [
                    "3-Attribute Venn = 4×2 Matrix (2022 S2 Supermarket): For three binary attributes (Domestic/Foreign × Cosmetic/Nutrition × FDA/EU), never draw circles. Use a 4×2 table of mutually exclusive cells.",
                    "Nested Sets = Disjoint Buckets (2022 S1 Get-Together): When 3-day ⊂ 2-day ⊂ 1-day, use 4 disjoint buckets: '3-day', '2-day only', '1-day only', and 'None'.",
                    "Group + Knockout Match Counts (2021 S2 Chango): Rank 2 vs Rank 3 winner plays Rank 1 → Rank 1 plays at most 3 games total, while a Rank 2/3 champion plays 4 games.",
                    "Pooling Dilution (2021 S3 Bottles): Mixing equal samples from k bottles dilutes impurity by 1/k. Compare against the 10% detection threshold.",
                    "Zero-Sum Invariant (2022 S3 Betting, 2025 S1 Taps): Total money across all 4 players is 40 at the end of every round; total taps across all 5 questions is 40."
                ]
            }
        ]
    },
    "QA": {
        "title": "QA 40-Minute Three-Pass Triage & Formula Playbook (330 Questions)",
        "overview": "Every QA slot gives 40 minutes for 22 questions (~1.8 min/Q). High-percentile performance comes from a strict 3-Pass Triage: Pass 1 (Min 0–15) banks 8–10 Easy anchors; Pass 2 (Min 15–32) solves 5–7 Medium core items; Pass 3 (Min 32–40) targets 1–2 Hard items only if setup clicks immediately.",
        "calibration": [
            {"tier": "Easy (1.0–1.5 min)", "role": "Pass 1 Priority (Min 0–15)", "desc": "Single-concept application, clean linear/ratio setup, direct formula (SI/CI, work-rate, polygon angles, remainder cycles)."},
            {"tier": "Medium (1.75–2.5 min)", "role": "Pass 2 Core (Min 15–32)", "desc": "Two-concept hybrids (Ratios + Mixtures, Geometry + Similarity, Quadratics + Inequalities). Primary score differentiators."},
            {"tier": "Hard (3.0+ min)", "role": "Pass 3 / Skip Candidate", "desc": "Multi-case modulus/GIF analysis, Diophantine optimization, nested functional equations. Skip on sight in Pass 1."}
        ],
        "categories": [
            {
                "name": "Arithmetic (~42% of QA — 139 Questions)",
                "count": 139,
                "profile": "Undisputed backbone of CAT QA; rewards clean ratio & alligation setups",
                "rules": [
                    "Successive Percentage Change: Net change for a% and b% is a + b + ab/100. Express changes as multipliers (1 ± x/100).",
                    "Dishonest Merchant & Markup: SP = CP(1 + p/100) = MP(1 − d/100). If a merchant gets 105 cm for the price of 100 cm and sells 95 cm as 100 cm, effective SP/CP = (105/95) × (nominal SP/CP).",
                    "Consecutive Year CI Ratio: CI in Year (k+1) = [CI in Year k] × (1 + r/100). For two-installment loan repayment: P = X₁/(1+r) + X₂/(1+r)².",
                    "Weighted Averages & Alligation: w₁/w₂ = (A₂ − A_m)/(A_m − A₁). For max/min of distinct integer averages, push all non-target elements to their tightest permissible bounds.",
                    "Repeated Replacement: Remaining fraction = (1 − x/V)ⁿ. Watch the CAT trap 'done once and repeated three more times' → n = 4 total steps, not 3!",
                    "Time & Work Wages: Always split total wages in proportion to total work done by each person, not daily efficiency (unless they worked the same number of days).",
                    "Meeting-After-Crossing TSD Identity (2022 S1, 2023 S1): If A and B meet at t_m and take t_A, t_B after meeting to reach destinations, then S_A / S_B = √(t_B / t_A) and t_m = √(t_A · t_B)."
                ]
            },
            {
                "name": "Algebra (~30% of QA — 98 Questions)",
                "count": 98,
                "profile": "Primary 90-to-99 percentile separator; structural identities vs. modulus/log cases",
                "rules": [
                    "Sum of Squares = 0 (2023 S1 Q47, 2024 S1 Q55, 2024 S2 Q67): Rearrange underdetermined multi-variable equations into (A)² + (B)² + (C)² = 0 → each term is 0.",
                    "AM–GM Inequality: For x, y > 0, ax/y + by/x ≥ 2√(ab); for opposite signs, ≤ −2√(ab), leaving (−2√(ab), 2√(ab)) unattainable.",
                    "Vieta's & Sign Definiteness: f(x) = ax² + bx + c ≥ 0 for all real x iff a > 0 and D ≤ 0. If f(2) = 0 and f(x) ≥ 0 everywhere (2022 S2 Q45), then f(x) = a(x − 2)².",
                    "Exponential Base-1 Branches: A(x)^B(x) = 1 holds when (i) B(x) = 0 & A(x) ≠ 0, (ii) A(x) = 1, or (iii) A(x) = −1 & B(x) is an even integer.",
                    "Modulus Distance Identity: |x − a| + |x − b| = |a − b| holds for all x ∈ [a, b] (infinitely many solutions). Also max{a,b} − min{a,b} = |a − b|.",
                    "Logarithm Domain & Base Flip: Always enforce argument > 0, base > 0, base ≠ 1 before summing roots. When 0 < base < 1, log_b(u) > 0 flips to 0 < u < 1.",
                    "Functional Equations: For f(xy) = f(x)f(y) + f(x) + f(y), add 1 to both sides: f(xy) + 1 = (f(x)+1)(f(y)+1). For f(x) + 2f(1/x) = 3x, substitute x → 1/x and solve the 2×2 system."
                ]
            },
            {
                "name": "Geometry & Mensuration (~16% of QA — 52 Questions)",
                "count": 52,
                "profile": "Fast visual points; dominated by triangle area ratios, incircles & rhombus identities",
                "rules": [
                    "Triangle Area Ratios: Same height → Area ratio = base ratio. Shared angle A → Area(△ADE)/Area(△ABC) = (AD · AE)/(AB · AC).",
                    "Medians & Medial Triangle: 3 medians split a triangle into 6 equal-area triangles (1/6 each). Midpoint triangle has 1/4 area.",
                    "Right Triangle Inradius: r = (a + b − c)/2 and Area = r · s. Circumradius R = c/2.",
                    "The Rhombus Shortcut (2021 S2, 2021 S3, 2025 S1): (d₁ + d₂)² = 4s² + 4·Area and (d₁ − d₂)² = 4s² − 4·Area. Never solve a quadratic for d₁, d₂ separately!",
                    "Tangent Angle Property (2025 S2 Q56): If tangents PQ, PR subtend ∠P and third tangent AB touches the arc, ∠AOB = 90° − ∠P/2.",
                    "Parallelogram Vertex Identity (2022 S1, 2025 S1): Coordinate-wise A + C = B + D."
                ]
            },
            {
                "name": "Number Systems (~8% of QA — 27 Questions)",
                "count": 27,
                "profile": "Clean Round-1 points via factor formulas, Euler totient & place value",
                "rules": [
                    "Factors of Form 3r + 1 (2025 S2 Q63): Exclude all powers of 3. Primes ≡ 1 (mod 3) can take any exponent; primes ≡ 2 (mod 3) must have an even total exponent sum.",
                    "Euler's Totient & Remainders: a^φ(m) ≡ 1 (mod m) for coprime a, m. φ(7) = 6, φ(11) = 10, φ(13) = 12.",
                    "Sum of All n-Digit Permutations (2024 S1 Q50): For 4 distinct non-zero digits a, b, c, d, sum of all 24 four-digit numbers is 6 × (a+b+c+d) × 1111 = 6666(a+b+c+d).",
                    "Powers of 2 and 5 Digit Sum (2025 S2 Q66): Pair 5^a × 2^b = 10^min(a,b) × leftover power. Trailing zeros contribute 0 to the sum of digits!"
                ]
            },
            {
                "name": "Modern Math (~4% of QA — 14 Questions)",
                "count": 14,
                "profile": "High-ROI templates: Stars-and-Bars, Onto Functions & 3-Set Venn bounds",
                "rules": [
                    "Stars and Bars (Identical Items): n identical items into r distinct boxes (each ≥ 1) = C(n−1, r−1). For even positive balloons (2022 S1 Q57), halve n first: C(10−1, 4−1) = C(9,3) = 84.",
                    "Onto (Surjective) Functions (2024 S1 Q58): From m=6 elements to n=3 elements: 3⁶ − C(3,1)·2⁶ + C(3,2)·1⁶ = 729 − 192 + 3 = 540.",
                    "3-Set Triple Intersection Bounds (2022 S1 Q49): Max(A∩B∩C) = min(|A|, |B|, |C|). Min(A∩B∩C) = max(0, |A| + |B| + |C| − 2|U|).",
                    "'Up to k' & 'At least once' Traps: 'Up to 2 out of 6 sauces' (2025 S1 Q56) includes 0, 1, or 2 sauces: C(6,0)+C(6,1)+C(6,2) = 22."
                ]
            }
        ]
    },
    "VARC": {
        "title": "VARC 40-Minute Pacing & Elimination Playbook (24 Questions / Slot)",
        "overview": "Every VARC slot has 16 Reading Comprehension questions (4 passages × 4 Qs) and 8 Verbal Ability questions (Para Summary, Para Jumbles, Odd Sentence Out, Sentence Insertion). Target 26–28 minutes for the 4 RC passages (~6.5–7 min/passage) and 12–14 minutes for the 8 VA questions (~1.5 min/Q).",
        "calibration": [
            {"tier": "Easy (1.25–1.5 min)", "role": "High-Accuracy Anchors", "desc": "Sentence Insertion (Para Completion), Para Summary, and direct RC Main Idea / Purpose questions."},
            {"tier": "Medium (1.5–2.0 min)", "role": "Core RC & VA", "desc": "RC Inference / EXCEPT questions and TITA Para Jumbles / Odd Sentence Out (zero negative marking on TITA!)."},
            {"tier": "Hard (2.0+ min)", "role": "Double-Negative / Abstract RC", "desc": "'Which statement, if false, would contradict / weaken...' — translate double negatives into a simple '+ / −' sign check before reading options."}
        ],
        "categories": [
            {
                "name": "Reading Comprehension (16 Qs / Slot)",
                "count": 240,
                "profile": "4 Passages × 4 Qs; 100% elimination-driven rather than memory-driven",
                "rules": [
                    "The 4-Flaw Elimination Filter: 95% of wrong RC options fail due to one of four traps: (1) Extreme Quantifiers ('always', 'solely', 'never', 'all'), (2) Scope Shift (true for one example, claimed for the whole field), (3) Alien Comparison (comparing X and Y when the text only mentions both), or (4) Reversed Causality.",
                    "Double-Negative Decoding ('if false, could be seen as supporting/contradicting'): Write the table: 'If False → Supports Passage' means the statement itself Contradicts the Passage! 'If False → Contradicts Passage' means the statement itself Agrees with the Passage!",
                    "First & Last Sentence Paragraph Map: Read for structure (Where is the author's thesis? Where does the counter-argument start?), not to memorize details. Verify every option's exact noun phrase against the anchor paragraph."
                ]
            },
            {
                "name": "Verbal Ability — Summary, Insertion, Jumbles & Odd-Out (8 Qs / Slot)",
                "count": 120,
                "profile": "High-speed 90-second puzzles; TITA items have zero negative marking",
                "rules": [
                    "Sentence Insertion (Para Completion): Look at the sentence immediately AFTER each blank. Pronouns ('This reality...', 'Yet each day...', 'They changed...') must bind tightly to the inserted sentence's subject.",
                    "Para Summary: A valid summary must cover the passage's primary claim + main reason without adding advice ('should/must') that the author never gave.",
                    "Para Jumbles & Odd Sentence Out (TITA — Never Leave Blank!): Because TITA questions carry 0 negative penalty, always lock your mandatory pair (pronoun/chronology link) and enter your 4-digit sequence or odd sentence number (1–5)."
                ]
            }
        ]
    }
}

with open(f"{base_dir}/knowledge_briefs.json", "w") as f:
    json.dump(knowledge_briefs, f, indent=2)

print("Saved knowledge_briefs.json!")
