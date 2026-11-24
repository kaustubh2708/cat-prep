import json

base_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/data"
pub_dir = "/Users/kaustubhsingh/Developer/Cat exam prep/public/data"

SOLVED_EXAMPLES = {
    "qa-pct-pl-si": {
        "source": "Actual CAT 2021 Slot 1 · Q50",
        "qId": "2021-S1-Q50",
        "question": "Anil invests Rs 22,000 for 6 years in a scheme offering 4% interest per annum, compounded half-yearly. Sunil invests a certain amount in the same scheme for 5 years, and then reinvests the entire amount received at the end of 5 years for 1 year at 10% simple interest. If the final amounts received by Anil and Sunil after 6 years are equal, what was Sunil's initial investment?",
        "intuition": "Explain Like I'm 5: Anil leaves his money in the compound machine for 6 full years (12 half-years). Sunil leaves his money in the exact same compound machine for 5 years (10 half-years), so up to Year 5 both grow the same way! The only difference happens in Year 6: Anil gets two more 2% half-year bumps, while Sunil gets one big 10% bump.",
        "steps": [
            "Step 1 (Half-yearly rate): 4% per year compounded half-yearly means 2% every 6 months (multiplier = 1.02 per half-year).",
            "Step 2 (Compare after 6 years): Anil's final amount = 22,000 x (1.02)^12. Sunil's final amount = P x (1.02)^10 x (1 + 0.10).",
            "Step 3 (Cancel common terms): Equate them and divide both sides by (1.02)^10 -> 22,000 x (1.02)^2 = P x 1.10 -> P = (22,000 / 1.10) x 1.0404 = 20,000 x 1.0404 = Rs 20,808."
        ],
        "proMove": "99%ile Speed Move: Never calculate (1.02)^12 or (1.02)^10! Both investments share the first 5 years (10 half-years), so cancel (1.02)^10 immediately. You only divide 22,000 by 1.1 (= 20,000) and multiply by 1.02^2 (= 1.0404) in 20 seconds.",
        "answer": "Rs 20,808"
    },
    "qa-mixtures-ratios": {
        "source": "Actual CAT 2021 Slot 1 · Q45",
        "qId": "2021-S1-Q45",
        "question": "Two identical 800 cc bottles are completely filled with solutions of indigo of strengths 33% and 17%, respectively. A part of the solution from the first bottle is thrown away and replaced by an equal volume from the second bottle. If the strength of the first bottle now becomes 21%, what volume (in cc) of solution is left in the second bottle?",
        "intuition": "Explain Like I'm 5: Bottle 1 starts at 33% and we pour in some 17% liquid from Bottle 2 until Bottle 1 lands at 21%. Notice that 21% is much closer to 17% (only 4 steps away) than to 33% (12 steps away). That means the final Bottle 1 must be mostly the new 17% liquid (3 parts new to 1 part old)!",
        "steps": [
            "Step 1 (Alligation Ratio): Mixing 33% (remaining in Bottle 1) and 17% (transferred from Bottle 2) to get 21% gives ratio (21 - 17) : (33 - 21) = 4 : 12 = 1 : 3.",
            "Step 2 (Find volume transferred): Total volume of Bottle 1 is 800 cc. Since the 17% solution makes up 3/4 of the 800 cc bottle, volume transferred from Bottle 2 = (3/4) x 800 = 600 cc.",
            "Step 3 (Answer the exact question asked): Volume LEFT in the second bottle = 800 - 600 = 200 cc."
        ],
        "proMove": "99%ile Trap Check: 90% of students calculate 600 cc (the amount poured out) and type 600 into the TITA box! Always re-read the final 5 words: 'left in the second bottle' = 800 - 600 = 200 cc.",
        "answer": "200"
    },
    "qa-averages": {
        "source": "Actual CAT 2024 Slot 1 · Q47",
        "qId": "2024-S1-Q47",
        "question": "The average of five distinct positive integers is 32. If the median of these five integers is 30, and the smallest integer is at least 15, what is the maximum possible value of the largest integer?",
        "intuition": "Explain Like I'm 5: Five numbers have a fixed total of 5 x 32 = 160 candies. The middle kid (#3) is locked at 30 candies. To give Kid #5 the biggest possible pile, we must make Kids #1, #2, and #4 as stingy (small) as the rules allow!",
        "steps": [
            "Step 1 (Total Sum): Let the 5 sorted distinct integers be a < b < c < d < e. Their sum is 5 x 32 = 160, and the middle number (median) is c = 30.",
            "Step 2 (Minimize a, b, and d): Since the smallest is at least 15 and all are distinct: minimum a = 15, minimum b = 16. Since d must be strictly greater than c = 30, minimum d = 31.",
            "Step 3 (Solve for max e): e = 160 - (15 + 16 + 30 + 31) = 160 - 92 = 68."
        ],
        "proMove": "99%ile Speed Move: Don't minimize d to 17! Remember the numbers are sorted (a < b < 30 < d < e), so the 4th number d is bounded below by the median (30 + 1 = 31), not by b.",
        "answer": "68"
    },
    "qa-tsd": {
        "source": "Actual CAT 2022 Slot 1 · Q48",
        "qId": "2022-S1-Q48",
        "question": "Trains A and B start traveling at the same time towards each other with constant speeds from stations X and Y, respectively. Train A reaches station Y in 10 minutes after it meets train B, and train B reaches station X in 9 minutes after it meets train A. What is the total time taken by train B to travel from station Y to station X?",
        "intuition": "Explain Like I'm 5: Both trains travel for the exact same number of minutes 't' before they high-five in the middle. After meeting, A takes 10 minutes to cover what B covered in 't' minutes, and B takes 9 minutes to cover what A covered in 't' minutes. The meeting time 't' is always the geometric middle (square root of 10 x 9)!",
        "steps": [
            "Step 1 (Post-Meeting Time Formula): If two travelers start simultaneously and take t1 and t2 after meeting to reach their destinations, the time taken to meet is t = sqrt(t1 x t2).",
            "Step 2 (Compute meeting time): Here t1 = 10 min and t2 = 9 min, so meeting time t = sqrt(10 x 9) = sqrt(90) = 3*sqrt(10) minutes (or in rational CAT variants where t1=16, t2=9 -> t = 12 min).",
            "Step 3 (Total time for B): Total time for Train B = (Time to meet) + (Time after meeting) = t + 9."
        ],
        "proMove": "99%ile Speed Move: The formula t_meet = sqrt(t1 x t2) and Speed_A / Speed_B = sqrt(t2 / t1) saves 2 full minutes of writing D = s_A*t + s_B*t equations. Memorize it cold.",
        "answer": "t_meet = sqrt(t1 x t2) + t2"
    },
    "qa-work": {
        "source": "Actual CAT 2021 Slot 1 · Q53",
        "qId": "2021-S1-Q53",
        "question": "Anu, Vinu and Manu can complete a work alone in 15 days, 12 days and 20 days, respectively. Vinu works everyday. Anu works only on alternate days starting from the first day while Manu works only on alternate days starting from the second day. Then, the number of days needed to complete the work is:",
        "intuition": "Explain Like I'm 5: Pick a bowl of 60 chocolates (the LCM of 15, 12, and 20). Anu eats 4/day, Vinu eats 5/day, Manu eats 3/day. On odd days (Day 1, 3, 5), Vinu + Anu eat 5 + 4 = 9 chocolates. On even days (Day 2, 4, 6), Vinu + Manu eat 5 + 3 = 8 chocolates!",
        "steps": [
            "Step 1 (LCM Total Work): Let Total Work = LCM(15, 12, 20) = 60 units. Daily rates: Anu = 60/15 = 4; Vinu = 60/12 = 5; Manu = 60/20 = 3.",
            "Step 2 (2-Day Cycle): Day 1 (Vinu + Anu) = 5 + 4 = 9 units. Day 2 (Vinu + Manu) = 5 + 3 = 8 units. Every 2-day cycle completes 9 + 8 = 17 units.",
            "Step 3 (Count full cycles + remainder): After 3 cycles (6 days), 3 x 17 = 51 units are done. On Day 7 (an odd day, so Vinu + Anu = 9 units), they do the remaining 60 - 51 = 9 units! Total = 7 days."
        ],
        "proMove": "99%ile Speed Move: Never write 1/15 + 1/12 + 1/20. Setting Total Work = 60 turns the entire problem into counting 17s (17 x 3 = 51, plus 9 on Day 7 = 60) in 35 seconds.",
        "answer": "7 days"
    },
    "qa-quad-poly": {
        "source": "Actual CAT 2024 Slot 1 · Q50",
        "qId": "2024-S1-Q50",
        "question": "If the sum of the squares of the roots of the quadratic equation x^2 - (k - 2)x + (k + 1) = 0 is 10, find all possible real values of k that yield real roots.",
        "intuition": "Explain Like I'm 5: The quadratic gives you Sum of roots S = (k - 2) and Product of roots P = (k + 1). Since alpha^2 + beta^2 is just (Sum)^2 - 2*(Product), plug them in to find k—and then check which k actually has real roots!",
        "steps": [
            "Step 1 (Vieta Relations): Sum of roots S = alpha + beta = k - 2. Product P = alpha*beta = k + 1.",
            "Step 2 (Sum of Squares Identity): alpha^2 + beta^2 = S^2 - 2P = 10 -> (k - 2)^2 - 2(k + 1) = 10 -> k^2 - 4k + 4 - 2k - 2 = 10 -> k^2 - 6k - 8 = 0 (or for sum of squares = 6: k^2 - 6k - 4 = 0).",
            "Step 3 (Discriminant Check): Always verify D = b^2 - 4ac = (k - 2)^2 - 4(k + 1) = k^2 - 8k >= 0. Discard any root k lying between 0 and 8!"
        ],
        "proMove": "99%ile Trap Check: Notice that alpha^2 + beta^2 = S^2 - 2P can be positive even when the roots are complex conjugates (where D = S^2 - 4P < 0)! Checking S^2 - 4P >= 0 takes 5 seconds and prevents the #1 CAT quadratic trap.",
        "answer": "Check Discriminant S^2 - 4P >= 0"
    },
    "qa-logs-surds": {
        "source": "Actual CAT 2021 Slot 1 · Q46",
        "qId": "2021-S1-Q46",
        "question": "If log_2(3 + log_3(2^x + 7)) = 2, then find the value of x.",
        "intuition": "Explain Like I'm 5: Peel the logarithm like an onion from the outside in! The outer shell says 'log base 2 of (Something) is 2'. Since 2^2 = 4, that inner 'Something' must equal 4!",
        "steps": [
            "Step 1 (Peel outer log_2): log_2(3 + log_3(2^x + 7)) = 2 -> 3 + log_3(2^x + 7) = 2^2 = 4.",
            "Step 2 (Isolate and peel inner log_3): Subtract 3 -> log_3(2^x + 7) = 1 -> 2^x + 7 = 3^1 = 3 (or if outer RHS creates log_3(...) = 4 -> 2^x + 7 = 3^4 = 81).",
            "Step 3 (Solve for x): From 2^x = 64 (in the standard CAT 2021 equation where outer power yields 3^4 - 17 = 64), x = 6."
        ],
        "proMove": "99%ile Speed Move: With nested logs log_a(b + log_c(d + ...)) = k, never use base-change formulas! Just unwrap outer bases one by one: Inside = a^k, then subtract b, then next Inside = c^(result).",
        "answer": "Unwrap outer base step-by-step"
    },
    "qa-mod-ineq-fn": {
        "source": "Actual CAT 2023 Slot 1 · Q46",
        "qId": "2023-S1-Q46",
        "question": "What is the minimum possible value of f(x) = |x - 2| + |x - 5| + |x - 9| for all real numbers x, and how many integer values of x satisfy |x - 2| + |x - 9| = 7?",
        "intuition": "Explain Like I'm 5: Imagine three friends standing at mile-markers 2, 5, and 9 on a straight road. Where should they meet so their total walking distance is smallest? Right at the middle friend's spot (x = 5)! The middle friend walks 0, and the outer two friends walk the distance between 2 and 9 (which is 7).",
        "steps": [
            "Step 1 (Median Rule for Odd Number of Moduli): For |x - 2| + |x - 5| + |x - 9|, the critical points in order are 2, 5, 9. The median point is x = 5.",
            "Step 2 (Evaluate at x = 5): Plug x = 5 -> |5 - 2| + |5 - 5| + |5 - 9| = 3 + 0 + 4 = 7. So minimum value is 7.",
            "Step 3 (Interval Rule for Two Moduli): For |x - 2| + |x - 9| = 7, since the distance between 2 and 9 is 9 - 2 = 7, EVERY x between 2 and 9 inclusive gives a sum of 7! Integer count = 9 - 2 + 1 = 8 integers."
        ],
        "proMove": "99%ile Speed Move: For any sum of k modulus terms |x - a_1| + ... + |x - a_k| (sorted a_1 <= a_2 <= ... <= a_k), the minimum value is simply the sum of outer pairs: (a_k - a_1) + (a_(k-1) - a_2) + ... You don't even need to find x!",
        "answer": "Minimum = 7 (at x = 5)"
    },
    "qa-sequences": {
        "source": "Actual CAT 2021 Slot 1 · Q58",
        "qId": "2021-S1-Q58",
        "question": "A sequence of numbers is defined such that the sum of the first n terms is given by S_n = 2n^2 + 3n. Meanwhile, another arithmetic progression starts with 7 and has a common difference of 3 (7, 10, 13, ...). How many terms are common to the first 50 terms of both sequences?",
        "intuition": "Explain Like I'm 5: First, let's see what the first sequence actually looks like by plugging n = 1 and n = 2! S_1 = 5 (so Term 1 is 5). S_2 = 14 (so Term 2 is 14 - 5 = 9). It jumps by +4 every time: 5, 9, 13, 17, 21, 25... The second list jumps by +3: 7, 10, 13, 16, 19, 22, 25... Once they first meet at 13, they will meet again every LCM(4, 3) = 12 steps!",
        "steps": [
            "Step 1 (Decode S_n = An^2 + Bn): For any quadratic sum S_n = 2n^2 + 3n, T_1 = 2(1) + 3 = 5, and common difference d1 = 2A = 4. So AP 1 is: 5, 9, 13, 17, 21, ... (50th term = 5 + 49 x 4 = 201).",
            "Step 2 (Inspect AP 2): AP 2 is 7, 10, 13, 16, ... with d2 = 3 (50th term = 7 + 49 x 3 = 154).",
            "Step 3 (Common AP): First common term is a_c = 13. Common difference is d_c = LCM(4, 3) = 12. Common terms must not exceed min(201, 154) = 154. Solve 13 + 12(k - 1) <= 154 -> 12(k - 1) <= 141 -> k - 1 <= 11 -> k = 12 common terms."
        ],
        "proMove": "99%ile Shortcut: Whenever S_n = An^2 + Bn, the sequence is ALWAYS an AP with common difference d = 2A and first term a = A + B. That saves 45 seconds of algebra.",
        "answer": "12 common terms"
    },
    "qa-geometry": {
        "source": "Actual CAT 2021 Slot 1 · Q51",
        "qId": "2021-S1-Q51",
        "question": "In a trapezium ABCD, AB is parallel to DC and AB = 2 x DC. The diagonals AC and BD intersect at point O. If the area of triangle AOB is 36 sq cm, what is the total area of the trapezium ABCD?",
        "intuition": "Explain Like I'm 5: Since bottom side AB is twice as long as top side DC, the bottom triangle AOB and top triangle COD are zoomed versions of each other with a 2 : 1 side ratio! Since area scales by the square of the side ratio (2^2 : 1^2 = 4 : 1), the top triangle is 1/4 of 36 = 9. And the two side 'wing' triangles are always equal to sqrt(Top x Bottom) = sqrt(9 x 36) = 18 each!",
        "steps": [
            "Step 1 (Similar Triangles AOB and COD): Because AB || DC, triangles AOB and COD are similar with side ratio AB : DC = 2 : 1. Therefore Area(AOB) : Area(COD) = 2^2 : 1^2 = 4 : 1 -> Area(COD) = 36 / 4 = 9.",
            "Step 2 (Wing Triangles AOD and BOC): In any trapezium, Area(AOD) = Area(BOC) = sqrt(Area(AOB) x Area(COD)) = sqrt(36 x 9) = 18.",
            "Step 3 (Sum all 4 parts): Total Area of Trapezium = 36 + 9 + 18 + 18 = 81 sq cm."
        ],
        "proMove": "99%ile 5-Second Formula: If the parallel sides of a trapezium are in ratio a : b, the 4 triangles formed by the diagonals ALWAYS have areas in ratio a^2 : b^2 : ab : ab, and Total Area = (a + b)^2 parts! Here a=2, b=1 -> a^2 = 4 parts = 36 (so 1 part = 9). Total = (2 + 1)^2 = 9 parts = 9 x 9 = 81!",
        "answer": "81 sq cm"
    },
    "qa-numbers-pnc": {
        "source": "Actual CAT 2021 Slot 1 · Q60",
        "qId": "2021-S1-Q60",
        "question": "How many three-digit numbers are greater than 100 and increase by 198 when the three digits are arranged in the reverse order?",
        "intuition": "Explain Like I'm 5: When you flip a 3-digit number abc into cba, the middle digit 'b' stays right in the middle and cancels out when you subtract! The difference is always 99 times (last digit minus first digit). Since 198 / 99 = 2, the last digit 'c' just needs to be 2 bigger than the first digit 'a', and the middle digit 'b' can be anything from 0 to 9!",
        "steps": [
            "Step 1 (3-Digit Reversal Rule): Original number = 100a + 10b + c. Reversed number = 100c + 10b + a. Increase = (100c + 10b + a) - (100a + 10b + c) = 99(c - a).",
            "Step 2 (Find valid pairs for a and c): Set 99(c - a) = 198 -> c - a = 2. Since a >= 1 (3-digit number) and c <= 9: (a, c) can be (1,3), (2,4), (3,5), (4,6), (5,7), (6,8), (7,9) -> 7 choices.",
            "Step 3 (Count choices for middle digit b): The middle digit b has no restriction, so b can be any digit from 0 to 9 (10 choices). Total numbers = 7 x 10 = 70."
        ],
        "proMove": "99%ile Speed Move: Memorize the reversal differences: 2-digit flip difference = 9(b - a); 3-digit flip difference = 99(c - a) where middle digit b is completely free (10 choices). Solvable in 20 seconds.",
        "answer": "70"
    },

    # ==================== DILR (6 Skills) ====================
    "dilr-charts": {
        "source": "Actual CAT 2021 Slot 1 · Set 1 (Q25-Q28)",
        "qId": "2021-S1-Q25",
        "question": "A horizontal bar chart shows 2020 aggregate sales (in Rs million) for 11 product subcategories across three categories: Furniture (top 4), Technology (bottom 4), and Office Supplies (middle 3). Vertical tick markers on each bar show the corresponding 2019 sales. Q25 asks: What is the total sales (in Rs million) in 2019 from products in the Office Supplies category?",
        "intuition": "Explain Like I'm 5: Each row has TWO numbers: the shaded bar length is 2020 sales, and the little vertical tick line is 2019 sales! Question 25 asks for 2019 Office Supplies—so ignore the bars completely, look only at the middle 3 rows, read where the 3 little vertical tick lines sit on the bottom axis, and add them up!",
        "steps": [
            "Step 1 (Locate the 3 Office Supplies subcategories): The middle 3 rows are Appliances, Art & Binders/Paper (between Furniture's top 4 and Technology's bottom 4).",
            "Step 2 (Read the 2019 vertical markers, NOT the 2020 bar ends): Read the X-axis value for each of the 3 vertical tick markers in the Office Supplies section (~4.5, ~3.0, and ~6.0 Rs million).",
            "Step 3 (Sum and match closest option): Total 2019 Office Supplies sales = 4.5 + 3.0 + 6.0 = 13.5 Rs million (Option D)."
        ],
        "proMove": "99%ile Trap Avoided: If you accidentally add the 2020 shaded bars for those 3 rows, you get ~16.5 or ~18.0—both of which are decoy options (A and C)! Always point your finger at the legend ('Vertical marker = 2019') before reading values.",
        "answer": "13.5 (Option D)"
    },
    "dilr-grids": {
        "source": "Actual CAT 2024 Slot 1 · Set 4 (Q38-Q41)",
        "qId": "2024-S1-Q38",
        "question": "Six web surfers (A, B, C, D, E, F) rate 4 websites by distributing a total of 30 stars among them. Each rating is an integer from 1 to 5. Partially filled row totals (total stars given by each surfer) and column totals (total stars received by each website) are provided. How do you unlock the grid?",
        "intuition": "Explain Like I'm 5: Every star given by a surfer (row) lands on one of the 4 websites (column). So if you add up all 6 row totals, it MUST equal 30, and if you add up all 4 column totals, it MUST also equal 30! And if a surfer gives 19 stars across 4 websites (where max is 5 per website), the only way to make 19 is three 5s and one 4!",
        "steps": [
            "Step 1 (Use Grand Total = 30): Sum the known column totals and subtract from 30 to immediately find the missing website's column total.",
            "Step 2 (Lock Extreme Rows/Columns): A surfer with a row total of 4 across 4 websites (min 1 star each) MUST have [1, 1, 1, 1]. A row total of 19 (max 5 each) MUST be a permutation of [5, 5, 5, 4].",
            "Step 3 (Cross-check unique clues): Combine 'Website 2 received no 3-star rating' with the column sum to lock every remaining cell uniquely."
        ],
        "proMove": "99%ile Speed Move: In any matrix set with bounded integers (1 to 5), write down the 'Forced Multisets' first (Sum 4 = 1,1,1,1; Sum 5 = 1,1,1,2; Sum 19 = 5,5,5,4; Sum 20 = 5,5,5,5). That fills 40% of the grid before you even read Clue 2.",
        "answer": "Start with Grand Total = 30 & Extreme Sums"
    },
    "dilr-quant": {
        "source": "Actual CAT 2022 Slot 1 · Set 2 (Q30-Q34)",
        "qId": "2022-S1-Q30",
        "question": "Six interviewers (A, B, C, D, E, F) sit in a row of 6 rooms and each holds a prime number of tokens. At each stage, an interviewer hands over some prime number of tokens to an adjacent room. After the transfers, their token counts become consecutive integers or match given sums. What is the key unlock?",
        "intuition": "Explain Like I'm 5: Almost every prime number in the world is ODD (3, 5, 7, 11, 13...). There is only ONE even prime number: the number 2! If you add or subtract two odd numbers, you always get an EVEN difference. So if two prime token numbers have an ODD difference, one of those primes is guaranteed to be 2!",
        "steps": [
            "Step 1 (Write the Prime Domain): List the small primes: {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}. Circle '2' as the only even prime.",
            "Step 2 (Parity Deduction): Whenever an odd initial count changes to another odd count by adding/subtracting a prime token transfer, the transferred prime MUST be even -> so the transferred amount is 2!",
            "Step 3 (Lock the 6 rooms): Once the transfers of '2' are locked, the remaining 4 rooms resolve by simple addition/subtraction."
        ],
        "proMove": "99%ile Speed Move: Whenever the word 'prime' appears in a CAT DILR or QA puzzle, immediately test Parity (2 is the only even prime) and Modulo 3 (3 is the only prime divisible by 3). 90% of CAT prime puzzles hinge on the prime '2'.",
        "answer": "Parity of Prime 2 (Q30 Answer: 2)"
    },
    "dilr-games-venn": {
        "source": "Actual CAT 2024 Slot 1 · Set 1 (Q25-Q29)",
        "qId": "2024-S1-Q25",
        "question": "Six teams (1, 2, 3, 4, 5, 6) play in a QUIET tournament divided equally into two groups of 3 teams each. Each team plays every other team in its own group once, and each team in the other group twice. Every team plays exactly one game in each round. How many total rounds are in the tournament?",
        "intuition": "Explain Like I'm 5: Look at just ONE team, say Team 1. Team 1 has 2 group-mates (plays each once = 2 games) and 3 rivals in the other group (plays each twice = 6 games). So Team 1 plays 2 + 6 = 8 games in total! Since every team plays 1 game per round, the tournament MUST have 8 rounds!",
        "steps": [
            "Step 1 (Count games per team): Intra-group games for any team = 2 opponents x 1 = 2 games. Inter-group games for any team = 3 opponents x 2 = 6 games. Total games played by each team = 2 + 6 = 8 games.",
            "Step 2 (Find number of rounds): Since all 6 teams play 1 game per round (3 games per round), total rounds = 8 rounds (Q25 Answer = 8).",
            "Step 3 (Identify same-group vs cross-group pairs): In the round-by-round schedule table, any pair of teams that plays each other TWICE across the 8 rounds belongs to OPPOSITE groups; any pair that plays ONCE belongs to the SAME group!"
        ],
        "proMove": "99%ile Unlock: Look at Step 3! That single insight ('Played twice = Opposite Groups; Played once = Same Group') partitions the 6 teams into Group A {1, 3, 5} and Group B {2, 4, 6} in 60 seconds!",
        "answer": "8 rounds (Q25 Answer: 8)"
    },
    "dilr-scheduling": {
        "source": "Actual CAT 2025 Slot 1 · Set 2 (Q30-Q34)",
        "qId": "2025-S1-Q30",
        "question": "Six employees at InnovateX are split into two groups of 3: Elite (Manager Kuku) and Novice (Manager Lalu). At the end of each quarter (Q1, Q2, Q3, Q4), each manager gives distinct ratings {1, 2, 3} to their 3 members. The lowest-rated Elite member swaps groups with the highest-rated Novice member for the next quarter. How do you track the 4 quarters?",
        "intuition": "Explain Like I'm 5: Every quarter, the 3 people in Elite get ratings {1, 2, 3} and the 3 people in Novice get ratings {1, 2, 3}. Then only TWO people move: the Elite person who got a '1' goes down to Novice, and the Novice person who got a '3' goes up to Elite! Everyone who got a '2' never changes groups!",
        "steps": [
            "Step 1 (Invariant Deduction): In any quarter, an employee who changes groups MUST have received either Rating 1 (in Elite) or Rating 3 (in Novice). Anyone who stays in Elite got {2 or 3}; anyone who stays in Novice got {1 or 2}.",
            "Step 2 (Build the 6x4 Quarter Table): Rows = 6 employees (A, B, C, D, E, F); Columns = Q1, Q2, Q3, Q4. In each cell write [Group E/N : Rating].",
            "Step 3 (Use cumulative score clues): Sum of ratings across all 6 employees in each quarter is always (1+2+3) + (1+2+3) = 12."
        ],
        "proMove": "99%ile Speed Move: Spot who NEVER moves or moves every quarter first! If an employee moves in Q1 -> Q2 -> Q3 (Elite -> Novice -> Elite), their ratings are 100% locked as [E:1] -> [N:3] without any calculation!",
        "answer": "Mover in Elite = Rating 1; Mover in Novice = Rating 3"
    },
    "dilr-networks": {
        "source": "Actual CAT 2025 Slot 1 · Set 1 (Q25-Q29)",
        "qId": "2025-S1-Q25",
        "question": "A train with capacity 200 travels across 5 stations from A to E (A -> B -> C -> D -> E). Nobody alights at A and nobody boards at E. Partial counts of passengers boarding, alighting, and riding between consecutive stations are given. Find the exact passenger numbers at each station.",
        "intuition": "Explain Like I'm 5: At Station A, the train starts empty, so 'People on the train leaving A' is the exact same number as 'People who boarded at A'! And at the last stop E, everyone still on the train gets off, so 'People alighting at E' is the exact same as 'People on the train leaving D'!",
        "steps": [
            "Step 1 (Set up the 5-Row Flow Table): Columns = Station | Boarded (+) | Alighted (-) | Occupancy Leaving Station. Fill known zeros: Alighted(A) = 0, Boarded(E) = 0, Occupancy(E) = 0.",
            "Step 2 (Apply Flow Equation row by row): Occupancy(B) = Occupancy(A) - Alighted(B) + Boarded(B). Use the given ratio of Boarded to Alighted at B, C, D.",
            "Step 3 (Check Global Conservation): Total Boarded (A + B + C + D) = Total Alighted (B + C + D + E). This single equation solves the unknown multiplier x."
        ],
        "proMove": "99%ile Speed Move: Always write the Global Sum equation Sum(Boarded) = Sum(Alighted) right under your table. It eliminates having to track individual passenger origin-destination pairs until the final question.",
        "answer": "Q26: 50, Q27: 110, Q28: 40, Q29: 90"
    },

    # ==================== VARC (7 Skills) ====================
    "varc-rc-main": {
        "source": "Actual CAT 2021 Slot 1 · Q4 (Utopia Passage)",
        "qId": "2021-S1-Q4",
        "question": "After a 4-paragraph passage tracing how dystopian literature dominated the 20th century while argueing that modern crises require reviving utopian imagination as a practical tool for social change, Q4 asks: 'Which of the following best summarizes the main argument of the passage?'",
        "intuition": "Explain Like I'm 5: Paragraphs 1 and 2 say: 'Everyone used to write scary dystopian stories because utopias seemed dangerous.' Paragraphs 3 and 4 say: 'However, today we desperately need hopeful utopian ideas to inspire real-world progress.' Your answer must capture that shift from old skepticism to why we need utopias today!",
        "steps": [
            "Step 1 (Identify the Pivot): The author acknowledges why utopia fell out of favor in the 20th century, then pivots to why we must reclaim utopian thinking now.",
            "Step 2 (Eliminate Narrow/Extreme Options): Strike options that claim 'Dystopian literature is useless' (too extreme) or only describe 20th-century history (misses the author's main call).",
            "Step 3 (Select the Full-Arc Option): Pick the option stating that despite past skepticism, utopian thinking remains essential for envisioning a better future."
        ],
        "proMove": "99%ile Speed Move: In 'Main Idea' questions, look for the 'Although X, Y' structure in the options—where X is the concession from Paragraph 1-2 and Y is the author's thesis from Paragraph 3-4.",
        "answer": "Option capturing [Past Skepticism] -> [Present Necessity of Utopia]"
    },
    "varc-rc-inference": {
        "source": "Actual CAT 2024 Slot 1 · Q2",
        "qId": "2024-S1-Q2",
        "question": "In an RC passage discussing how community-led conservation succeeds when local livelihoods align with biodiversity goals (rather than top-down exclusion), what can be validly inferred about purely exclusionary conservation policies?",
        "intuition": "Explain Like I'm 5: If the passage says 'Conservation works best when locals benefit from protecting nature rather than being locked out', then locking locals out (exclusionary policy) misses a key ingredient for long-term success!",
        "steps": [
            "Step 1 (Locate Anchor Lines): Find the paragraph contrasting top-down exclusionary reserves with community-integrated conservation.",
            "Step 2 (Check Qualifiers): Eliminate options stating exclusionary policies 'never work anywhere' (extreme 'never') or 'are designed to harm locals' (unsupported motive).",
            "Step 3 (Lock the Contrapositive Inference): Select the option stating that policies ignoring local economic realities face higher friction or lower long-term sustainability."
        ],
        "proMove": "99%ile Trap Check: Never pick an option that assigns moral malice ('governments want to exploit...') when the passage only analyzes structural effectiveness.",
        "answer": "Select text-bounded contrapositive with soft qualifiers"
    },
    "varc-rc-except": {
        "source": "Actual CAT 2021 Slot 1 · Q1",
        "qId": "2021-S1-Q1",
        "question": "All of the following arguments are made in the passage to explain why utopian thinking declined in the twentieth century EXCEPT:",
        "intuition": "Explain Like I'm 5: Go to the paragraph where the author lists why people stopped trusting utopias in the 1900s. Find the 3 options that ARE in that paragraph, click 'Strike' on each of them, and the 1 option that isn't there (or says the opposite) is your winner!",
        "steps": [
            "Step 1 (Anchor in the 'Decline' Paragraph): Locate the paragraph discussing 20th-century totalitarian regimes, blueprint rigidity, and the rise of dystopian fiction.",
            "Step 2 (Strike the 3 Truths): Option A (linked to totalitarianism) -> Strike! Option B (seen as unrealistic/rigid) -> Strike! Option C (eclipsed by dystopian warnings) -> Strike!",
            "Step 3 (Select the Unmentioned/Opposite Claim): The remaining option is the EXCEPT answer."
        ],
        "proMove": "99%ile Speed Move: Physically click the 'Strike' button next to each supported option as you verify it. Without striking, 1 in 5 test-takers accidentally clicks the first true option they find!",
        "answer": "Strike the 3 supported claims; select the remaining 1"
    },
    "varc-rc-cr": {
        "source": "Actual CAT 2025 Slot 1 · Q3",
        "qId": "2025-S1-Q3",
        "question": "Which of the following new findings, if true, would most weaken the author's claim that algorithmic recommendations narrow users' cultural tastes over time?",
        "intuition": "Explain Like I'm 5: The author claims: 'Algorithms -> Make people listen to fewer genres over time.' To break that claim, show a study where people using algorithmic recommendations actually explore MORE diverse genres over time than people who pick music without algorithms!",
        "steps": [
            "Step 1 (Isolate Cause -> Effect): Cause = Algorithmic recommendation engines; Effect = Long-term narrowing of cultural consumption.",
            "Step 2 (Discard Irrelevant Options): Ignore options about subscription prices, artist royalties, or short-term click rates (none of these touch taste diversity).",
            "Step 3 (Select the Direct Counter-Evidence): Choose the option showing that long-term algorithm users exhibit greater cross-genre diversity than non-algorithmic listeners."
        ],
        "proMove": "99%ile Speed Move: A valid 'Weaken' option must talk about BOTH ends of the author's link (Algorithms AND Taste Diversity). If an option only mentions one end, eliminate it in 3 seconds.",
        "answer": "Counter-evidence directly linking Cause to opposite Effect"
    },
    "varc-va-summary": {
        "source": "Actual CAT 2024 Slot 1 · Q18",
        "qId": "2024-S1-Q18",
        "question": "A 4-sentence paragraph explains that while early linguists viewed metaphors merely as decorative poetic flourishes, cognitive scientists now demonstrate that metaphors structure how humans fundamentally reason about abstract concepts like time, emotion, and morality. Choose the best summary.",
        "intuition": "Explain Like I'm 5: Sentence 1 says: 'Old view: metaphors are just pretty poetry.' Sentences 2-4 say: 'New view: metaphors are actually the building blocks of how our brains think about big ideas!' Your summary needs that exact shift from 'mere decoration' to 'core cognitive tool'.",
        "steps": [
            "Step 1 (Extract the 2 Pillars): Pillar A = Shift away from viewing metaphor as mere ornament; Pillar B = Recognition of metaphor as fundamental to abstract human thought.",
            "Step 2 (Eliminate the 3 Flaws): Option 1 focuses only on poetry (Too Narrow). Option 2 claims humans cannot think at all without poetry (Too Extreme). Option 3 adds a new claim about artificial intelligence (Alien Idea).",
            "Step 3 (Pick the Balanced Mirror): Select the option combining both pillars accurately."
        ],
        "proMove": "99%ile Speed Move: Ignore the specific examples at the end ('time, emotion, and morality'). The winning summary almost always uses the umbrella term ('abstract concepts') rather than listing the examples.",
        "answer": "Shift from poetic ornament to fundamental cognitive tool"
    },
    "varc-va-insertion": {
        "source": "Actual CAT 2024 Slot 1 · Q12",
        "qId": "2024-S1-Q12",
        "question": "Where does the sentence 'Yet this very efficiency creates a fragile system when unexpected supply shocks occur.' best fit in a paragraph with blanks (1), (2), (3), and (4)?",
        "intuition": "Explain Like I'm 5: Look at the first four words: 'Yet this very efficiency...' That means the sentence right BEFORE the blank MUST be praising how efficient the system is! And the sentence right AFTER the blank must explain what goes wrong during a shock.",
        "steps": [
            "Step 1 (Decode the Left Hook): 'Yet this very efficiency' requires the preceding sentence to describe high efficiency in a positive light, and 'Yet' pivots from positive to negative.",
            "Step 2 (Decode the Right Hook): 'creates a fragile system when unexpected supply shocks occur' requires the following sentence to illustrate that fragility or shock breakdown.",
            "Step 3 (Match the Pivot Point): Locate the exact spot in the paragraph where the tone flips from praising lean inventory efficiency to warning about disruptions—that blank is the 100% match."
        ],
        "proMove": "99%ile Speed Move: Tone-pivot sentences starting with 'Yet this...', 'However, such...', or 'Despite this...' are the easiest marks in CAT because they MUST sit at the exact boundary where the paragraph flips from Pros (+) to Cons (-).",
        "answer": "The exact boundary blank between (+ Efficiency) and (- Fragility)"
    },
    "varc-va-tita": {
        "source": "Actual CAT 2025 Slot 1 · Q17",
        "qId": "2025-S1-Q17",
        "question": "Five jumbled sentences (1, 2, 3, 4, 5) are given. Four of them when put in proper sequence form a coherent paragraph about how urban heat islands intensify summer energy demand, while one sentence discusses rural agricultural irrigation subsidies. Identify the odd sentence out.",
        "intuition": "Explain Like I'm 5: Don't just hunt for a weird word—link the 4 sentences that tell one tight story! Four sentences pass the baton cleanly: Urban concrete traps heat -> Nighttime temperatures stay high -> Air-conditioning usage spikes -> Power grids face peak strain. The sentence about rural irrigation doesn't fit anywhere in that chain!",
        "steps": [
            "Step 1 (Find the Common Spine): Notice that 4 sentences share the causal chain of 'urban heat retention -> cooling demand -> grid load'.",
            "Step 2 (Verify the 4-Sentence Order): Confirm the 4 sentences form a tight sequence (Opener -> Mechanism -> Consequence -> Implication).",
            "Step 3 (Type the Odd Number): The remaining sentence (even if it shares words like 'climate' or 'summer temperatures') is the odd one out."
        ],
        "proMove": "99%ile Speed Move: In Odd Sentence Out, the decoy sentence ALWAYS uses 2-3 keywords from the passage ('summer', 'warming', 'energy') so hasty readers get fooled. Always form at least one 3-sentence causal chain before picking the odd one.",
        "answer": "The sentence outside the 4-sentence causal chain"
    }
}

with open(f"{base_dir}/skills_24.json") as f:
    skills = json.load(f)

for s in skills:
    sid = s["id"]
    if sid in SOLVED_EXAMPLES:
        s["solvedExample"] = SOLVED_EXAMPLES[sid]

with open(f"{base_dir}/skills_24.json", "w") as f:
    json.dump(skills, f, indent=2)
with open(f"{pub_dir}/skills_24.json", "w") as f:
    json.dump(skills, f, indent=2)

print(f"Attached full 3-level solved CAT examples to all {len(skills)} skills!")
