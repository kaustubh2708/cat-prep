import json

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"
pub_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/public/data"

SKILLS_24 = [
    # ==================== QA (11 Skills) ====================
    {
        "id": "qa-pct-pl-si",
        "section": "QA",
        "group": "Arithmetic",
        "name": "Percentages, Profit & Loss & Interest",
        "tagline": "Markup/discount chains, successive % changes, and SI vs. CI shortcuts",
        "frequency": "High Frequency (~3–4 Qs per slot)",
        "targetTime": "1.25 – 1.75 min",
        "formulas": [
            "Successive % change of a% and b%: Net % = a + b + (ab / 100)",
            "Markup M% then Discount D%: Selling Price = CP × (1 + M/100) × (1 - D/100)",
            "2-Year CI − SI difference on Principal P at r%: Diff = P × (r / 100)²",
            "3-Year CI − SI difference: Diff = P × (r / 100)² × (3 + r / 100)"
        ],
        "howToApproach": "Start by setting the unknown base (Cost Price or Principal) to 100 or 100x if only percentages are given. Convert percentages like 12.5% → 1/8, 16.67% → 1/6, 33.33% → 1/3 into clean fractions before multiplying.",
        "easyTrigger": "Single chain of markup/discount or comparing 2-year Simple vs. Compound Interest.",
        "commonTrap": "Taking discount % on Cost Price instead of Marked Price, or applying annual interest rate without halving it for half-yearly compounding."
    },
    {
        "id": "qa-mixtures-ratios",
        "section": "QA",
        "group": "Arithmetic",
        "name": "Ratios, Mixtures & Alligation",
        "tagline": "Blending two solutions, repeated draw-and-replace, and ratio proportion setups",
        "frequency": "High Frequency (~2–3 Qs per slot)",
        "targetTime": "1.25 – 1.75 min",
        "formulas": [
            "Alligation Ratio: Quantity₁ / Quantity₂ = (C₂ − C_mean) / (C_mean − C₁)",
            "Repeated Replacement (n draws of volume r from total V): Final Pure Fraction = (1 − r / V)ⁿ",
            "Componendo-Dividendo: If a/b = c/d, then (a+b)/(a−b) = (c+d)/(c−d)"
        ],
        "howToApproach": "In any mixture problem where liquid is poured from A to B and back, track the invariant quantity (total solute or total volume) or use the alligation see-saw line.",
        "easyTrigger": "Two vessels mixed to achieve a target concentration, or finding initial volume after 2 replacements.",
        "commonTrap": "In replacement problems, forgetting that the denominator V is the total solution volume, not just the remaining pure liquid."
    },
    {
        "id": "qa-averages",
        "section": "QA",
        "group": "Arithmetic",
        "name": "Averages & Min/Max Bounds",
        "tagline": "Weighted averages, group joins/leaves, and maximizing/minimizing one score",
        "frequency": "Consistent (~1–2 Qs per slot)",
        "targetTime": "1.25 – 1.5 min",
        "formulas": [
            "Deviation Method: True Mean = Assumed Base + (Sum of deviations from Base) / N",
            "New member joining: New Total = Old Total + New Value → ΔAverage = (New Value − Old Avg) / (N + 1)",
            "To Maximize one element in a fixed sum: push all other elements to their minimum allowed integer values."
        ],
        "howToApproach": "Never multiply large 3-digit numbers to find a sum if you can work with surpluses and deficits around a round base number (e.g., 50 or 100).",
        "easyTrigger": "Average of N items changes by k when 1 or 2 items are excluded or replaced.",
        "commonTrap": "Ignoring distinctness or integer constraints ('distinct positive integers') when minimizing the remaining elements."
    },
    {
        "id": "qa-tsd",
        "section": "QA",
        "group": "Arithmetic",
        "name": "Time, Speed & Distance (Tracks, Trains & Boats)",
        "tagline": "Relative speed, post-meeting times, circular tracks, and upstream/downstream",
        "frequency": "High Frequency (~2–3 Qs per slot)",
        "targetTime": "1.5 – 2.0 min",
        "formulas": [
            "After meeting on the way, if A takes t₁ and B takes t₂ to reach destinations: Speed_A / Speed_B = √(t₂ / t₁) and Meeting Time t = √(t₁ × t₂)",
            "Circular Track distinct meeting points (speeds in lowest ratio a : b): Opposite dir = a + b points; Same dir = |a − b| points",
            "Boats & Streams: Downstream = u + v, Upstream = u − v; Average speed for equal distance = (u² − v²) / u"
        ],
        "howToApproach": "Draw a quick 1-line timeline marking where the two travelers are at the exact same moment t. Equal-time ratios convert distance ratios directly into speed ratios.",
        "easyTrigger": "Two travelers start from A and B, cross each other, or run on a circular track.",
        "commonTrap": "Starting relative speed calculation before both travelers are actually moving (always advance the earlier traveler to the later start time first!)."
    },
    {
        "id": "qa-work",
        "section": "QA",
        "group": "Arithmetic",
        "name": "Time, Work & Pipes",
        "tagline": "LCM total-work units, efficiency changes, and filling/emptying pipes",
        "frequency": "High Frequency (~1–2 Qs per slot)",
        "targetTime": "1.25 – 1.5 min",
        "formulas": [
            "Set Total Work W = LCM of given days (d₁, d₂, d₃) so daily rates r_i = W / d_i are clean integers",
            "Man-Days-Efficiency Rule: (M₁ × D₁ × H₁) / W₁ = (M₂ × D₂ × H₂) / W₂",
            "Net Rate with Leak: r_net = r_inlet − r_leak"
        ],
        "howToApproach": "Avoid fractions like 1/12 + 1/15. Immediately pick Total Work = 60 units so A does 5 units/day and B does 4 units/day.",
        "easyTrigger": "Two or three workers/pipes working together and one leaves k days before completion.",
        "commonTrap": "In alternating-day problems with a negative leak, computing cycles blindly without reserving the positive fill of the final step."
    },
    {
        "id": "qa-quad-poly",
        "section": "QA",
        "group": "Algebra",
        "name": "Quadratics, Polynomials & Linear Equations",
        "tagline": "Vieta’s root relations, discriminant conditions, and integer linear systems",
        "frequency": "High Frequency (~2–3 Qs per slot)",
        "targetTime": "1.5 – 2.0 min",
        "formulas": [
            "For ax² + bx + c = 0: Sum of roots α + β = −b/a, Product αβ = c/a",
            "Sum of squares: α² + β² = (α + β)² − 2αβ; Difference: |α − β| = √[(α + β)² − 4αβ]",
            "Real roots condition: Discriminant Δ = b² − 4ac ≥ 0",
            "Identities: a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca)"
        ],
        "howToApproach": "Whenever a question mentions 'roots of a quadratic', write down α + β and αβ first before trying the quadratic formula.",
        "easyTrigger": "Finding the value of an expression involving roots α, β or finding k for equal/real roots.",
        "commonTrap": "Forgetting to check that the discriminant b² − 4ac is non-negative when finding valid parameter values."
    },
    {
        "id": "qa-logs-surds",
        "section": "QA",
        "group": "Algebra",
        "name": "Logarithms, Exponents & Surds",
        "tagline": "Base change rules, log equations, and nested square roots",
        "frequency": "Very High ROI (~1–2 Qs almost every slot)",
        "targetTime": "1.25 – 1.75 min",
        "formulas": [
            "Base Power Rule: log_(a^k)(b^m) = (m / k) × log_a(b)",
            "Reciprocal Base: log_a(b) = 1 / log_b(a); Chain product: log_a(b) × log_b(c) = log_a(c)",
            "Nested Surd: √(a ± 2√b) = √x ± √y where x + y = a and xy = b (with x > y)"
        ],
        "howToApproach": "Convert all logarithms in an equation to a single common prime base (like 2, 3, or 10). Substitute t = log_a(x) if you see a quadratic in logs.",
        "easyTrigger": "Any equation with logs of bases like 2, 4, 8 or 3, 9, 27 — convert all to base 2 or 3 immediately.",
        "commonTrap": "Keeping a root x that makes the argument of any original log(f(x)) zero or negative (always check f(x) > 0!)."
    },
    {
        "id": "qa-mod-ineq-fn",
        "section": "QA",
        "group": "Algebra",
        "name": "Modulus, Inequalities & Functions",
        "tagline": "Absolute value graphs, AM-GM minimum values, and functional equations",
        "frequency": "High Frequency (~2–3 Qs per slot)",
        "targetTime": "1.5 – 2.25 min",
        "formulas": [
            "Minimum of |x − a| + |x − b| is |a − b|, achieved at any x between a and b",
            "For odd number of terms ∑|x − a_i|, minimum occurs at the median of {a_i}",
            "AM ≥ GM (for positive numbers): (x + y)/2 ≥ √(xy); x + c/x ≥ 2√c for x > 0",
            "|x| < k ⇔ −k < x < k; |x| > k ⇔ x > k or x < −k"
        ],
        "howToApproach": "Treat |x − a| as distance on a number line instead of splitting into 4 algebraic cases. For functional equations f(x+y), test x=0, y=0, or x=1 first.",
        "easyTrigger": "Finding the minimum value of a sum of modulus terms or number of integer solutions to |x − a| + |x − b| ≤ c.",
        "commonTrap": "Applying AM ≥ GM without checking that the variables are strictly positive and that the equality condition can actually be reached."
    },
    {
        "id": "qa-sequences",
        "section": "QA",
        "group": "Algebra",
        "name": "Sequences & Series (AP, GP & Telescoping)",
        "tagline": "Arithmetic & Geometric Progressions, common terms, and telescoping sums",
        "frequency": "High Frequency (~1–2 Qs per slot)",
        "targetTime": "1.5 – 2.0 min",
        "formulas": [
            "AP n-th term: T_n = a + (n−1)d; Sum S_n = (n/2)[2a + (n−1)d] = n × (Middle Term)",
            "GP n-th term: T_n = a × r^(n−1); Infinite GP Sum (|r| < 1): S_∞ = a / (1 − r)",
            "Telescoping Fraction: 1 / [n(n + d)] = (1 / d) × [1/n − 1/(n + d)]",
            "Common terms of two APs with differences d₁ and d₂ form an AP with common difference LCM(d₁, d₂)"
        ],
        "howToApproach": "If a sequence is defined recursively or asks for S_100, compute the first 3 terms (n=1, 2, 3) to spot the cancellation pattern or period.",
        "easyTrigger": "Sum of n terms of an AP/GP or common terms between two arithmetic progressions.",
        "commonTrap": "Off-by-one error when counting the number of terms from index k to m (number of terms is m − k + 1, not m − k)."
    },
    {
        "id": "qa-geometry",
        "section": "QA",
        "group": "Geometry & Mensuration",
        "name": "Geometry, Mensuration & Coordinate Geometry",
        "tagline": "Triangles, circles, quadrilaterals, 3D solids, and coordinate lines",
        "frequency": "High Frequency (~3 Qs per slot)",
        "targetTime": "1.5 – 2.25 min",
        "formulas": [
            "Similar Triangles (side ratio k): Area ratio = k²; Cevians sharing vertex height: Area ratio = Base ratio",
            "Right Triangle altitude h to hypotenuse c: h = (ab)/c; Inradius r = (a + b − c)/2; Circumradius R = c/2",
            "Circle Chords: PA × PB = PC × PD; Tangent-Secant: PT² = PA × PB",
            "Rhombus Area = ½ × d₁ × d₂ with (d₁/2)² + (d₂/2)² = side²; Trapezium diagonals divide into 4 triangles with Area(Left) = Area(Right) = √(A_top × A_bottom)"
        ],
        "howToApproach": "Draw a large, clean diagram first. Look for standard Pythagorean triples (3-4-5, 5-12-13, 8-15-17, 7-24-25) and similar triangles created by parallel lines.",
        "easyTrigger": "Direct angle chasing, rhombus/trapezium area, or coordinate intersection of lines.",
        "commonTrap": "Confusing diameter with radius in circle/sphere formulas, or assuming a triangle is isosceles when not stated."
    },
    {
        "id": "qa-numbers-pnc",
        "section": "QA",
        "group": "Number Systems & Modern Math",
        "name": "Number Systems, Divisibility & Combinatorics",
        "tagline": "Factors, remainders, digit puzzles, and Stars-and-Bars counting",
        "frequency": "Consistent (~2–3 Qs per slot)",
        "targetTime": "1.25 – 2.0 min",
        "formulas": [
            "For N = p₁^a × p₂^b: Total Factors = (a+1)(b+1); Odd factors = ignore power of 2",
            "2-Digit reversal: |(10a + b) − (10b + a)| = 9|a − b|; 3-Digit reversal difference = 99|a − c|",
            "Divisibility by 9 (or 3): Sum of digits is divisible by 9 (or 3); by 11: |(Odd pos sum) − (Even pos sum)| is 0 or 11k",
            "Distributing n identical items into r distinct bins: C(n + r − 1, r − 1) (if each bin ≥ 1: C(n − 1, r − 1))"
        ],
        "howToApproach": "For remainders, reduce the base modulo the divisor first (aim for ±1 mod d). For counting problems with 'at least one', compute Total − (None).",
        "easyTrigger": "Finding number of factors, remainder of a power, or 3-digit number with digit constraints.",
        "commonTrap": "Allowing the leading digit of an n-digit number to be 0 in permutation problems."
    },

    # ==================== DILR (6 Skills) ====================
    {
        "id": "dilr-charts",
        "section": "DILR",
        "group": "Data Interpretation",
        "name": "Visual Charts, Bar Graphs & Candlestick Plots",
        "tagline": "Bar/line charts, scatter plots, stacked percentages, and min-max-open-close charts",
        "frequency": "Top Round-1 Pick (1 set in almost every slot)",
        "targetTime": "8 – 10 min per set",
        "formulas": [
            "Read the X/Y axes, units (₹ million vs. %), and legend definitions for 45 seconds before touching Q1",
            "In Candlestick / Box plots: White/hollow box vs. shaded box tells you whether Close > Open or Open > Close",
            "Growth Rate = (Final − Initial) / Initial; Average share = Part / Total"
        ],
        "howToApproach": "Visual DI sets are your #1 Round-1 confidence anchors because they rarely require a global 10-minute deduction before Q1. Read the chart values directly for the specific rows asked in each question.",
        "easyTrigger": "Any set with a horizontal/vertical bar chart, scatter plot, or explicit numeric table.",
        "commonTrap": "Misreading 'percentage points increase' vs. 'percentage increase', or swapping 2019 markers with 2020 bars."
    },
    {
        "id": "dilr-grids",
        "section": "DILR",
        "group": "Logical Reasoning",
        "name": "Distribution Grids & Constraint Tables",
        "tagline": "Assigning people/items across categories, ratings, departments, or slots",
        "frequency": "Very High Frequency (~1–2 sets per slot)",
        "targetTime": "9 – 11 min per set",
        "formulas": [
            "Always check Row Totals and Column Totals first — hidden cells are often forced by Total − (Known Sum)",
            "Start with the most restricted clue ('neither A nor B', 'unique integer', or exact product/sum)",
            "Maintain a single clean 2D matrix rather than scattered notes"
        ],
        "howToApproach": "Draw the master entity × attribute table immediately. Fill in the 100% definite clues first, mark impossible cells with '×', and check which row/column sum forces a unique split.",
        "easyTrigger": "Fixed 4×4 or 5×4 assignment matrix with explicit row and column totals.",
        "commonTrap": "Jumping into trial-and-error branching before using the total sum invariant across all rows."
    },
    {
        "id": "dilr-quant",
        "section": "DILR",
        "group": "Logical Reasoning",
        "name": "Quant-Based Puzzles & Numerical Logic",
        "tagline": "Missing-number tables, coin/token distributions, and average/rating puzzles",
        "frequency": "High Frequency (~1 set per slot)",
        "targetTime": "10 – 12 min per set",
        "formulas": [
            "Write out the allowed set of integers first (e.g., primes {2, 3, 5, 7, 11} or ratings {1, 2, 3, 4, 5})",
            "Find which target sums can only be partitioned in 1 unique way (e.g., 3 distinct ratings summing to 14 from 1..5 MUST be {4, 5, 5} or {3, 5, 6})",
            "Use parity (odd/even) and divisibility to eliminate cases rapidly"
        ],
        "howToApproach": "List the extreme integer partitions first (minimum possible sum and maximum possible sum). That usually locks 2 or 3 rows immediately without any guessing.",
        "easyTrigger": "Small integer domains (ratings 1 to 5, prime tokens, or fixed total coins) where extreme sums have unique combinations.",
        "commonTrap": "Forgetting whether values in a row must be distinct or can repeat."
    },
    {
        "id": "dilr-games-venn",
        "section": "DILR",
        "group": "Logical Reasoning",
        "name": "Games, Tournaments & Venn Set Theory",
        "tagline": "Round-robin tables, knockout brackets, and 3-set/4-set Venn overlaps",
        "frequency": "Consistent (~1 set per slot)",
        "targetTime": "10 – 12 min per set",
        "formulas": [
            "Round-Robin with n teams: Total Matches = n(n − 1)/2; Total Wins = Total Losses (if no draws)",
            "3-Set Venn: Total = (A + B + C) − (Exactly 2) − 2×(All 3) + None",
            "Sum of goals scored by all teams = Sum of goals conceded by all teams"
        ],
        "howToApproach": "For tournaments, build a Wins / Losses / Draws / Points table and check the total points invariant. For Venn diagrams, label the atomic regions ('Only A', 'Exactly 2', 'All 3') with variables rather than overlapping circles.",
        "easyTrigger": "Standard round-robin point table or 3-group Venn overlap with 'exactly k' counts given.",
        "commonTrap": "Confusing 'at least two' (which is Exactly 2 + All 3) with 'more than two'."
    },
    {
        "id": "dilr-scheduling",
        "section": "DILR",
        "group": "Logical Reasoning",
        "name": "Scheduling, Timelines & Queues",
        "tagline": "Time-slot allocation, counter wait-times, and multi-day/quarter transitions",
        "frequency": "Moderate (~1 set every 1–2 slots)",
        "targetTime": "10 – 13 min per set",
        "formulas": [
            "Service Start Time = max(Customer Arrival Time, Counter Free Time)",
            "Use a discrete time grid (e.g., 9:00, 9:10, 9:20 or Q1, Q2, Q3, Q4) as your table columns",
            "Track capacity bottlenecks (maximum parallel servers/rooms available at time t)"
        ],
        "howToApproach": "Step through time chronologically from t = 0. Never try to solve t = 4 before locking who finishes at t = 1 and t = 2.",
        "easyTrigger": "Short 4-period or 5-slot timeline with deterministic transition rules.",
        "commonTrap": "Off-by-one boundary error on whether a counter freeing up at 10:15 can take a customer arriving at 10:15 immediately."
    },
    {
        "id": "dilr-networks",
        "section": "DILR",
        "group": "Logical Reasoning",
        "name": "Routes, Networks & Flow Diagrams",
        "tagline": "Pipelines, metro/train passenger flow, and delivery routing graphs",
        "frequency": "Moderate (~1 set every 2 slots)",
        "targetTime": "9 – 11 min per set",
        "formulas": [
            "Flow Conservation at any station/node: (Existing + Boarding/Inflow) = (Alighting/Outflow + Continuing)",
            "Start at degree-1 leaf nodes (first station A or final destination E) where the flow is 100% determined"
        ],
        "howToApproach": "Label the directed edges or build a Station × (Boarded / Alighted / On-Train) table. Work inward from the start and end stations.",
        "easyTrigger": "5-station linear train/bus route or simple directed delivery network with fixed node demands.",
        "commonTrap": "Ignoring direction arrows on one-way links or exceeding edge/train capacity."
    },

    # ==================== VARC (7 Skills) ====================
    {
        "id": "varc-rc-main",
        "section": "VARC",
        "group": "Reading Comprehension",
        "name": "RC: Main Idea, Purpose & Tone",
        "tagline": "Spotting the author's overarching thesis across paragraphs",
        "frequency": "Every RC Passage (~4 Qs per slot)",
        "targetTime": "1.25 – 1.5 min",
        "formulas": [
            "After each paragraph, mentally note a 4-word role tag (e.g., 'Old theory', 'Why it fails', 'Author's alternative')",
            "The correct Main Idea must cover the arc of the whole passage, not just a single vivid example from Paragraph 2"
        ],
        "howToApproach": "Ask yourself: 'Why did the author write this piece — to critique a view, explain a paradox, or trace a shift?' Eliminate options that are too narrow (1-paragraph detail) or too extreme in tone.",
        "easyTrigger": "Questions asking for the 'central theme', 'primary purpose', or 'best title/keywords'.",
        "commonTrap": "Picking an option that repeats catchy keywords from the final paragraph while missing the main argument."
    },
    {
        "id": "varc-rc-inference",
        "section": "VARC",
        "group": "Reading Comprehension",
        "name": "RC: Contextual Inference & Detail",
        "tagline": "Deducing what must be true from a specific argument in the passage",
        "frequency": "Highest Volume in VARC (~7–8 Qs per slot)",
        "targetTime": "1.5 – 1.75 min",
        "formulas": [
            "CAT Inference = Unstated premise or direct logical consequence of the text (never an outside opinion)",
            "Check the quantifiers: 'some/often/may' in the passage can NEVER support 'all/always/only' in an option"
        ],
        "howToApproach": "Go back to the specific 4–5 lines referenced by the question stem. Compare the final 2 contenders word-by-word against the author's qualifiers.",
        "easyTrigger": "Questions pointing to a specific phrase, quote, or paragraph ('In the context of the second paragraph...').",
        "commonTrap": "Selecting a 'True but Irrelevant' option or an option that reverses cause and effect."
    },
    {
        "id": "varc-rc-except",
        "section": "VARC",
        "group": "Reading Comprehension",
        "name": "RC: Negative / EXCEPT Questions",
        "tagline": "Eliminating 3 supported statements to isolate the 1 unsupported/contradicted claim",
        "frequency": "High Frequency (~3–4 Qs per slot)",
        "targetTime": "1.5 – 2.0 min",
        "formulas": [
            "Use the Strike (✕) button to cross out each option as soon as you find its supporting sentence in the passage",
            "The winner is either directly contradicted by the passage or brings in an alien comparison never made by the author"
        ],
        "howToApproach": "Treat EXCEPT questions as a 3-item scavenger hunt. Three options will map cleanly to specific sentences in the text; the odd one out is your answer.",
        "easyTrigger": "Questions containing 'EXCEPT', 'NOT true', or 'cannot be inferred'.",
        "commonTrap": "Misreading the negative prompt under time pressure and clicking the first option that IS true!"
    },
    {
        "id": "varc-rc-cr",
        "section": "VARC",
        "group": "Reading Comprehension",
        "name": "RC: Critical Reasoning (Strengthen / Weaken)",
        "tagline": "Testing how a new fact impacts the author’s causal argument",
        "frequency": "Consistent (~1–2 Qs per slot)",
        "targetTime": "1.75 – 2.0 min",
        "formulas": [
            "Isolate the exact link: [Premise / Evidence] → [Author's Conclusion]",
            "To Weaken/Invalidate: break the causal link or show a counter-example where the premise holds but the conclusion fails",
            "To Strengthen/Support: remove an alternative explanation or reinforce the core assumption"
        ],
        "howToApproach": "Before reading the 4 options, state in one sentence WHICH claim the question asks you to weaken or strengthen (sometimes it's a critic's claim quoted in the passage, not the author's!).",
        "easyTrigger": "Prompts asking 'Which of the following, if true, would most undermine/bolster the argument...'",
        "commonTrap": "Attacking a side detail instead of the specific argument named in the question prompt."
    },
    {
        "id": "varc-va-summary",
        "section": "VARC",
        "group": "Verbal Ability",
        "name": "VA: Para Summary",
        "tagline": "Condensing a short paragraph into its core claim + primary reason",
        "frequency": "Guaranteed (~3 Qs every slot)",
        "targetTime": "1.25 – 1.5 min",
        "formulas": [
            "Formula for a 60-word CAT paragraph: [Main Conclusion] + [Primary Supporting Mechanism / Contrast]",
            "Eliminate options that: (1) add new advice/facts, (2) leave out the main conclusion, or (3) distort a neutral tone"
        ],
        "howToApproach": "Read the paragraph and summarize it in your own 10 words before looking at A, B, C, D. Usually 2 options are immediately out for being too narrow or adding an extra claim.",
        "easyTrigger": "Every Para Summary question is a high-ROI Round-1 anchor.",
        "commonTrap": "Falling for an option that copies whole phrases verbatim from the first sentence while missing the 'However...' turn in the middle."
    },
    {
        "id": "varc-va-insertion",
        "section": "VARC",
        "group": "Verbal Ability",
        "name": "VA: Sentence Insertion (Para Completion)",
        "tagline": "Placing a missing sentence into blank (1), (2), (3), or (4)",
        "frequency": "High Frequency (~2 Qs per slot in modern papers)",
        "targetTime": "1.0 – 1.25 min",
        "formulas": [
            "Circle the hooks in the target sentence: pronouns ('this', 'these', 'such', 'they') and connectors ('yet', 'therefore', 'for instance')",
            "The sentence MUST bridge BOTH the sentence before the blank and the sentence after the blank"
        ],
        "howToApproach": "Check what the sentence *after* each blank refers back to. Often placing the sentence into blank (k) repairs a broken pronoun reference in the sentence right after blank (k).",
        "easyTrigger": "Fastest questions in the entire VARC section (often solvable in 60 seconds).",
        "commonTrap": "Checking only that the sentence flows nicely after the preceding sentence without checking if the NEXT sentence still makes sense."
    },
    {
        "id": "varc-va-tita",
        "section": "VARC",
        "group": "Verbal Ability",
        "name": "VA: Para Jumbles & Odd Sentence Out (TITA)",
        "tagline": "4-sentence sequencing and 5-sentence odd-one-out (Zero Negative Marking!)",
        "frequency": "Guaranteed (~4–5 TITA Qs per slot)",
        "targetTime": "1.5 – 1.75 min",
        "formulas": [
            "Zero Negative Marking: Never leave a VA TITA blank!",
            "Para Jumbles: Find the independent opening sentence (introduces the main noun/concept) and 1 ironclad mandatory pair (Pronoun → Noun or Cause → Effect)",
            "Odd One Out: Form the coherent 4-sentence paragraph first; the 5th sentence usually shares the same topic word but shifts era, scope, or angle"
        ],
        "howToApproach": "Don't try to guess all 24 permutations. Lock one 2-sentence link (e.g., 3→1) and check whether the remaining sentences go before or after that block.",
        "easyTrigger": "Sentences with explicit chronological markers, full name → surname, or 'This phenomenon...' hooks.",
        "commonTrap": "Spending 3.5+ minutes agonizing over a TITA Para Jumble when you could bank two MCQ questions in that time."
    }
]

def map_question_to_skill(q):
    sec = q["section"]
    top = q["topic"]
    sub = q["subtopic"].lower()
    txt = (q["questionText"] + " " + q["hook"]).lower()

    if sec == "QA":
        if any(k in sub for k in ["percent", "profit", "loss", "p&l", "interest", "discount", "si", "ci"]):
            return "qa-pct-pl-si"
        if any(k in sub for k in ["mixture", "alligation", "ratio", "proportion", "alloy", "replacement"]):
            return "qa-mixtures-ratios"
        if "average" in sub or "mean" in sub:
            return "qa-averages"
        if any(k in sub for k in ["tsd", "speed", "distance", "train", "boat", "track", "circular", "race"]):
            return "qa-tsd"
        if any(k in sub for k in ["work", "pipe", "cistern", "efficiency"]):
            return "qa-work"
        if any(k in sub for k in ["log", "surd", "exponent", "indices"]):
            return "qa-logs-surds"
        if any(k in sub for k in ["modulus", "inequalit", "function", "minima", "maxima", "am-gm", "graph"]):
            return "qa-mod-ineq-fn"
        if any(k in sub for k in ["sequence", "series", "progression", "ap", "gp", "common terms", "telescop"]):
            return "qa-sequences"
        if top == "Geometry & Mensuration" or any(k in sub for k in ["triangle", "circle", "rhombus", "trapezium", "polygon", "coordinate", "mensuration", "rectangle", "square", "chord", "area", "volume", "octagon", "hexagon"]):
            return "qa-geometry"
        if top in ["Number Systems", "Modern Math"] or any(k in sub for k in ["factor", "divisib", "remainder", "digit", "prime", "hcf", "lcm", "combinator", "counting", "permutation", "probability", "set theory"]):
            return "qa-numbers-pnc"
        if top == "Algebra" or any(k in sub for k in ["quadratic", "polynomial", "linear", "equation", "identit", "root"]):
            return "qa-quad-poly"
        return "qa-pct-pl-si"

    if sec == "DILR":
        if "chart" in top.lower() or "visual" in top.lower() or any(k in sub for k in ["chart", "plot", "candlestick", "scatter", "graph", "sales"]):
            return "dilr-charts"
        if "quant" in top.lower() or any(k in sub for k in ["token", "coin", "average", "mean", "median", "rating", "score", "random draw", "trick", "triccek"]):
            return "dilr-quant"
        if "game" in top.lower() or "tournament" in top.lower() or any(k in sub for k in ["tournament", "match", "quiet", "hockey", "javelin", "betting", "get-together", "supermarket", "students"]):
            return "dilr-games-venn"
        if "schedul" in top.lower() or any(k in sub for k in ["schedul", "visa", "metro", "mortality", "project", "timeline", "queue"]):
            return "dilr-scheduling"
        if "network" in top.lower() or "route" in top.lower() or any(k in sub for k in ["route", "train", "station", "pipeline", "delivery", "flight", "path"]):
            return "dilr-networks"
        return "dilr-grids"

    # VARC
    if "main idea" in sub:
        return "varc-rc-main"
    if "except" in sub:
        return "varc-rc-except"
    if "critical reasoning" in sub or "strengthen" in sub:
        return "varc-rc-cr"
    if "summary" in sub:
        return "varc-va-summary"
    if "insertion" in sub or "completion" in sub:
        return "varc-va-insertion"
    if "jumble" in sub or "odd" in sub:
        return "varc-va-tita"
    return "varc-rc-inference"

with open(f"{pub_dir}/questions_1002.json") as f:
    qs = json.load(f)

skill_lookup = {s["id"]: s for s in SKILLS_24}
counts = {}
for q in qs:
    sid = map_question_to_skill(q)
    q["skillId"] = sid
    q["skillName"] = skill_lookup[sid]["name"]
    counts[sid] = counts.get(sid, 0) + 1

with open(f"{base_dir}/questions_1002.json", "w") as f:
    json.dump(qs, f, indent=2)
with open(f"{pub_dir}/questions_1002.json", "w") as f:
    json.dump(qs, f, indent=2)

for s in SKILLS_24:
    sid = s["id"]
    sq = [q for q in qs if q["skillId"] == sid]
    s["totalCount"] = len(sq)
    s["easyCount"] = sum(1 for q in sq if q["difficulty"] == "Easy")
    s["mediumCount"] = sum(1 for q in sq if q["difficulty"] == "Medium")
    s["hardCount"] = sum(1 for q in sq if q["difficulty"] == "Hard")

with open(f"{base_dir}/skills_24.json", "w") as f:
    json.dump(SKILLS_24, f, indent=2)
with open(f"{pub_dir}/skills_24.json", "w") as f:
    json.dump(SKILLS_24, f, indent=2)

print("Mapped all 1,002 questions across 24 user-friendly skills:")
for s in SKILLS_24:
    print(f"  [{s['section']}] {s['name']}: {s['totalCount']} Qs (Easy: {s['easyCount']}, Med: {s['mediumCount']}, Hard: {s['hardCount']})")
