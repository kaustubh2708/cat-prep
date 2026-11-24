/* ============================================================================
   CAT Study Desk & 24-Skill Workbook (2021-2025)
   ============================================================================ */

const STORAGE_KEY = 'cat_sprint_progress_v1';
const PAGE_ASPECT = 1684 / 1190.5;
const MAX_PAGES_BY_YEAR = { 2021: 45, 2022: 49, 2023: 41, 2024: 57, 2025: 55 };

const state = {
  questions: [],
  qById: {},
  skills: [],
  skillById: {},

  activeTab: 'plan',
  activeSprintDay: 1,
  activeModule: null, // { title, qIds }

  // Skills View State
  skillSectionFilter: 'ALL',
  skillConfFilter: 'ALL',
  skillDepthFilter: 'ALL', // 'ALL' | 'beginner' | 'intermediate' | 'advanced'
  selectedSkillId: 'qa-pct-pl-si',

  // Practice Desk Filters & Navigation
  filters: {
    section: 'ALL',
    skill: 'ALL',
    difficulty: 'ALL',
    year: 'ALL',
    slot: 'ALL',
    status: 'ALL',
    search: ''
  },
  filteredQuestions: [],
  currentIndex: 0,
  visualMode: 'both',
  sliceZoomed: false,
  zenTimer: false,

  // Active Question Timer
  timerSeconds: 0,
  timerPaused: false,
  timerInterval: null,

  // Active Question User Interaction
  currentSelection: '',
  eliminatedOptions: {},

  // Past Papers & 40-Min Timer
  simYear: 2024,
  simSlot: 1,
  simSection: 'DILR',
  simItems: [],
  simChoices: {},
  simClockSeconds: 40 * 60,
  simClockRunning: false,
  simClockInterval: null,

  // Full Page Modal
  modalYear: 2024,
  modalPage: 2,

  // Persistent Progress
  progress: {
    activeDay: 1,
    darkMode: false,
    attempts: {},       // { qId: { status, tag, correct, userAns, timeSec, ts } }
    skillConfidence: {},// { skillId: 'focus' | 'steady' | 'confident' }
    customKeys: {},     // { qId: 'B' }
    notes: {}           // { qId: 'text' }
  }
};

// Six-Day Study Plan (45-60 mins per day, 100% verified answers)
const SPRINT_DAYS = [
  {
    day: 1,
    shortTitle: 'First-Pass Anchors',
    title: 'Day 1: Locking In Easy First-Pass Questions (2024 & 2025)',
    goal: 'Build steady momentum on high-yield easy questions in Arithmetic, Algebra, Visual Charts, and Para Summary.',
    mindset: 'In CAT, an easy question carries the exact same +3 marks as the hardest problem in the slot. Securing every easy question first is the foundation of a 99th percentile score.',
    modules: [
      {
        id: 'd1-qa',
        name: 'Block A: QA First-Pass Arithmetic & Algebra',
        sub: 'CAT 2024 & 2025 Slot 1 (Target: 1.25 to 1.5 min per question)',
        qIds: ['2024-S1-Q47', '2024-S1-Q49', '2024-S1-Q50', '2024-S1-Q57', '2025-S1-Q47', '2025-S1-Q51']
      },
      {
        id: 'd1-dilr',
        name: 'Block B: DILR Visual Chart Set (Subcategory Sales)',
        sub: 'CAT 2021 Slot 1 (Q25 to Q28, Target: 8 to 9 min for all 4 questions)',
        qIds: ['2021-S1-Q25', '2021-S1-Q26', '2021-S1-Q27', '2021-S1-Q28']
      },
      {
        id: 'd1-varc',
        name: 'Block C: VARC Para Summary & Sentence Insertion',
        sub: 'CAT 2024 Slot 1 (Fast elimination and zero-penalty TITA items)',
        qIds: ['2024-S1-Q12', '2024-S1-Q13', '2024-S1-Q18', '2024-S1-Q19', '2024-S1-Q22', '2024-S1-Q23']
      }
    ]
  },
  {
    day: 2,
    shortTitle: 'Visual DI & Geometry',
    title: 'Day 2: Visual DI Set Selection, Geometry & Number Systems',
    goal: 'Practice reading candlestick charts and constraint tables cleanly, paired with fast Geometry and Divisibility setups.',
    mindset: 'Spend the first 90 seconds reading a DILR chart legend and axes before touching Question 1. Visual sets rarely require a full 10-minute deduction upfront.',
    modules: [
      {
        id: 'd2-dilr',
        name: 'Block A: DILR Seven Shares Candlestick Plot & Countries Matrix',
        sub: 'CAT 2024 Slot 1 (Q30 to Q37, 2 complete 4-question sets)',
        qIds: ['2024-S1-Q30', '2024-S1-Q31', '2024-S1-Q32', '2024-S1-Q33', '2024-S1-Q34', '2024-S1-Q35', '2024-S1-Q36', '2024-S1-Q37']
      },
      {
        id: 'd2-qa',
        name: 'Block B: QA Geometry, Mensuration & Number Systems',
        sub: 'CAT 2021 to 2024 Slot 1 (Triangles, circles, factors, and remainders)',
        qIds: ['2021-S1-Q51', '2021-S1-Q60', '2022-S1-Q47', '2023-S1-Q49', '2024-S1-Q52', '2024-S1-Q55']
      },
      {
        id: 'd2-varc',
        name: 'Block C: VARC Reading Comprehension Passage 1',
        sub: 'CAT 2024 Slot 1 (Q1 to Q4, Main idea and contextual inference)',
        qIds: ['2024-S1-Q1', '2024-S1-Q2', '2024-S1-Q3', '2024-S1-Q4']
      }
    ]
  },
  {
    day: 3,
    shortTitle: 'Second-Pass Core',
    title: 'Day 3: Second-Pass Score Differentiators (Medium Tier)',
    goal: 'Move from clearing cutoffs to a 99th percentile score with structured medium questions in Logs, Quadratics, TSD, and Quant Grids.',
    mindset: 'Medium questions reward a single clean setup: write Vieta sum/product of roots, convert logs to a common prime base, or check row/column sum totals.',
    modules: [
      {
        id: 'd3-qa',
        name: 'Block A: QA Second-Pass Algebra & Arithmetic',
        sub: 'Logarithms, Quadratic Vieta, Time-Speed-Distance, and Mixtures',
        qIds: ['2021-S1-Q45', '2021-S1-Q46', '2022-S1-Q45', '2023-S1-Q45', '2024-S1-Q48', '2025-S1-Q52']
      },
      {
        id: 'd3-dilr',
        name: 'Block B: DILR Quant Grid (Six Web Surfers Distributing 30 Stars)',
        sub: 'CAT 2024 Slot 1 (Q38 to Q41, Row and column sum invariants)',
        qIds: ['2024-S1-Q38', '2024-S1-Q39', '2024-S1-Q40', '2024-S1-Q41']
      },
      {
        id: 'd3-varc',
        name: 'Block C: VARC Critical Reasoning & EXCEPT Passage',
        sub: 'CAT 2025 Slot 1 Passage 1 (Q1 to Q4)',
        qIds: ['2025-S1-Q1', '2025-S1-Q2', '2025-S1-Q3', '2025-S1-Q4']
      }
    ]
  },
  {
    day: 4,
    shortTitle: '68-Q Modern Format',
    title: 'Day 4: Modern 68-Question Format Calibration (2024 & 2025)',
    goal: 'Practice the current 68-question structure (24 VARC, 22 DILR, 22 QA) including 5-question DILR flow sets.',
    mindset: 'In the 22-question DILR section, completing two clean sets plus one or two standalone questions (10 to 11 net correct) places you comfortably in the 99th percentile range.',
    modules: [
      {
        id: 'd4-dilr',
        name: 'Block A: DILR 5-Question Flow Set (Train Route Station A to E)',
        sub: 'CAT 2025 Slot 1 (Q25 to Q29, Passenger boarding and alighting conservation)',
        qIds: ['2025-S1-Q25', '2025-S1-Q26', '2025-S1-Q27', '2025-S1-Q28', '2025-S1-Q29']
      },
      {
        id: 'd4-qa',
        name: 'Block B: CAT 2025 Slot 1 QA Mixed Drill',
        sub: 'Balancing zero-penalty TITA questions with fast MCQ eliminations',
        qIds: ['2025-S1-Q48', '2025-S1-Q49', '2025-S1-Q50', '2025-S1-Q53', '2025-S1-Q54', '2025-S1-Q55']
      },
      {
        id: 'd4-varc',
        name: 'Block C: CAT 2025 Slot 1 Verbal Ability Sprint',
        sub: 'Odd Sentence Out, Para Summary, and Sentence Insertion (Q17 to Q22)',
        qIds: ['2025-S1-Q17', '2025-S1-Q18', '2025-S1-Q19', '2025-S1-Q20', '2025-S1-Q21', '2025-S1-Q22']
      }
    ]
  },
  {
    day: 5,
    shortTitle: 'Skip Discipline',
    title: 'Day 5: Smart Skip Discipline & High-Frequency Traps',
    goal: 'Practice separating 90-second winners from 4-minute traps, and polish your flagged focus skills.',
    mindset: 'If a question has no clear equation or entry point after 45 seconds, use "Skip (Too Long)" and move on. Protecting your clock is a core exam skill.',
    modules: [
      {
        id: 'd5-qa',
        name: 'Block A: QA Mixed Pacing & Trap Recognition',
        sub: 'CAT 2021 to 2024 Slot 1 (Arithmetic, Sequences, and Modulus)',
        qIds: ['2021-S1-Q47', '2021-S1-Q48', '2022-S1-Q46', '2023-S1-Q46', '2024-S1-Q51', '2024-S1-Q53']
      },
      {
        id: 'd5-dilr',
        name: 'Block B: DILR Assignment Matrix (Project & Question Review)',
        sub: 'CAT 2021 Slot 1 (Q29 to Q32)',
        qIds: ['2021-S1-Q29', '2021-S1-Q30', '2021-S1-Q31', '2021-S1-Q32']
      },
      {
        id: 'd5-varc',
        name: 'Block C: VARC Dense Reading Comprehension Drill',
        sub: 'CAT 2021 Slot 1 Utopia Passage (Q1 to Q4)',
        qIds: ['2021-S1-Q1', '2021-S1-Q2', '2021-S1-Q3', '2021-S1-Q4']
      }
    ]
  },
  {
    day: 6,
    shortTitle: 'Exam-Eve Warmup',
    title: 'Day 6 (Exam Eve): Light 20-Minute Warmup & Formula Scan',
    goal: 'Solve 8 straightforward confidence builders and skim your 24 skill cheat sheets. Finish early and rest well.',
    mindset: 'Your preparation is complete. Tomorrow is simply about staying calm, picking your two best DILR sets, and collecting every easy mark in QA and VARC.',
    modules: [
      {
        id: 'd6-warmup',
        name: 'Exam-Eve 8-Question Confidence Warmup',
        sub: 'Clean 1-minute first-pass questions across QA and VARC',
        qIds: ['2021-S1-Q45', '2021-S1-Q50', '2024-S1-Q47', '2024-S1-Q50', '2025-S1-Q47', '2025-S1-Q51', '2024-S1-Q18', '2025-S1-Q21']
      }
    ]
  }
];

/* ============================================================================
   INITIALIZATION & STORAGE
   ============================================================================ */
document.addEventListener('DOMContentLoaded', async () => {
  loadProgressFromStorage();
  if (state.progress.darkMode) {
    document.body.classList.add('dark-theme');
  }
  state.activeSprintDay = state.progress.activeDay || 1;

  try {
    const [qRes, sRes] = await Promise.all([
      fetch('./data/questions_1002.json'),
      fetch('./data/skills_24.json')
    ]);
    state.questions = await qRes.json();
    state.skills = await sRes.json();

    state.questions.forEach((q) => {
      state.qById[q.id] = q;
    });
    state.skills.forEach((s) => {
      state.skillById[s.id] = s;
    });

    if (state.skills.length > 0) {
      state.selectedSkillId = state.skills[0].id;
    }

    populateSkillFilterDropdown();
    bindAllEvents();

    renderStudyPlanView();
    renderSkillsView();
    applyFiltersAndRenderPractice(false);
    loadSimulatorSection();
    updateFocusSkillsBadge();

    document.getElementById('loading-overlay').hidden = true;
  } catch (err) {
    console.error('Error loading study desk data:', err);
    const bar = document.getElementById('loading-overlay');
    bar.textContent = 'Could not load question bank files. Please refresh the page.';
  }
});

function loadProgressFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      state.progress = {
        ...state.progress,
        ...parsed,
        attempts: parsed.attempts || {},
        skillConfidence: parsed.skillConfidence || {},
        customKeys: parsed.customKeys || {},
        notes: parsed.notes || {}
      };
    }
  } catch (e) {
    console.warn('Could not read saved progress:', e);
  }
}

function saveProgressToStorage() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.progress));
  } catch (e) {
    console.warn('Could not write progress:', e);
  }
  updateFocusSkillsBadge();
}

function getEffectiveSkillConfidence(skillId) {
  if (state.progress.skillConfidence[skillId]) {
    return state.progress.skillConfidence[skillId];
  }
  // Derive from attempts in this skill if user hasn't manually set it
  const skillQs = state.questions.filter((q) => q.skillId === skillId);
  let solved = 0;
  let weak = 0;
  skillQs.forEach((q) => {
    const att = state.progress.attempts[q.id];
    if (!att || att.status === 'triage') return;
    if (att.tag === 'weak' || att.correct === false) weak += 1;
    else solved += 1;
  });
  if (weak > 0) return 'focus';
  if (solved >= 3) return 'confident';
  if (solved >= 1) return 'steady';
  return 'steady';
}

function getFocusSkillCount() {
  return state.skills.filter((s) => getEffectiveSkillConfidence(s.id) === 'focus').length;
}

function updateFocusSkillsBadge() {
  const count = getFocusSkillCount();
  const badge = document.getElementById('focus-skills-count');
  if (count > 0) {
    badge.textContent = String(count);
    badge.hidden = false;
  } else {
    badge.hidden = true;
  }
}

/* ============================================================================
   NAVIGATION & GLOBAL EVENTS
   ============================================================================ */
function switchTab(tabName) {
  state.activeTab = tabName;
  document.querySelectorAll('.nav-link').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tab === tabName);
  });
  document.querySelectorAll('.view-pane').forEach((sec) => {
    sec.classList.toggle('active', sec.id === `view-${tabName}`);
  });

  if (tabName === 'plan') renderStudyPlanView();
  if (tabName === 'skills') renderSkillsView();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function bindAllEvents() {
  document.querySelectorAll('.nav-link').forEach((btn) => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });

  document.getElementById('btn-theme-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    state.progress.darkMode = document.body.classList.contains('dark-theme');
    saveProgressToStorage();
  });

  document.getElementById('btn-quick-warmup').addEventListener('click', () => {
    const candidates = state.questions.filter(
      (q) => q.difficulty === 'Easy' && q.answer && !state.progress.attempts[q.id]
    );
    const pool = candidates.length >= 5 ? candidates : state.questions.filter((q) => q.difficulty === 'Easy' && q.answer);
    launchPracticeSession('5-Question Easy Warmup', pool.slice(0, 5).map((q) => q.id));
  });

  // View 1: Study Plan Events
  document.getElementById('btn-start-active-day').addEventListener('click', () => {
    const dayObj = SPRINT_DAYS.find((d) => d.day === state.activeSprintDay) || SPRINT_DAYS[0];
    const allIds = dayObj.modules.flatMap((m) => m.qIds);
    launchPracticeSession(dayObj.title, allIds);
  });

  document.getElementById('btn-goto-skills').addEventListener('click', () => {
    switchTab('skills');
  });

  document.getElementById('btn-review-focus-skills').addEventListener('click', () => {
    const focusCount = getFocusSkillCount();
    state.skillConfFilter = focusCount > 0 ? 'focus' : 'ALL';
    document.querySelectorAll('[data-sconf]').forEach((b) => {
      b.classList.toggle('active', b.dataset.sconf === state.skillConfFilter);
    });
    switchTab('skills');
  });

  // View 2: Skills Filter Events
  document.querySelectorAll('[data-ssec]').forEach((btn) => {
    btn.addEventListener('click', () => {
      state.skillSectionFilter = btn.dataset.ssec;
      document.querySelectorAll('[data-ssec]').forEach((b) => b.classList.toggle('active', b === btn));
      renderSkillsView();
    });
  });

  document.querySelectorAll('[data-sconf]').forEach((btn) => {
    btn.addEventListener('click', () => {
      state.skillConfFilter = btn.dataset.sconf;
      document.querySelectorAll('[data-sconf]').forEach((b) => b.classList.toggle('active', b === btn));
      renderSkillsView();
    });
  });

  // View 3: Practice Desk Filter Events
  ['section', 'skill', 'difficulty', 'year', 'slot', 'status'].forEach((key) => {
    document.getElementById(`filter-${key}`).addEventListener('change', (e) => {
      state.activeModule = null;
      state.filters[key] = e.target.value;
      if (key === 'section') populateSkillFilterDropdown();
      applyFiltersAndRenderPractice(true);
    });
  });

  document.getElementById('filter-search-input').addEventListener('input', (e) => {
    state.activeModule = null;
    state.filters.search = e.target.value.trim();
    applyFiltersAndRenderPractice(true);
  });

  document.getElementById('btn-reset-filters').addEventListener('click', () => {
    resetPracticeFilters();
    applyFiltersAndRenderPractice(true);
  });

  document.getElementById('btn-clear-session').addEventListener('click', () => {
    state.activeModule = null;
    applyFiltersAndRenderPractice(true);
  });

  document.getElementById('btn-prev-q').addEventListener('click', () => {
    if (state.currentIndex > 0) selectQuestionByIndex(state.currentIndex - 1);
  });
  document.getElementById('btn-next-q').addEventListener('click', () => {
    if (state.currentIndex < state.filteredQuestions.length - 1) selectQuestionByIndex(state.currentIndex + 1);
  });

  // Left Pane Context Mode
  document.querySelectorAll('[data-vmode]').forEach((btn) => {
    btn.addEventListener('click', () => {
      state.visualMode = btn.dataset.vmode;
      document.querySelectorAll('[data-vmode]').forEach((b) => b.classList.toggle('active', b === btn));
      renderCurrentQuestion();
    });
  });

  document.getElementById('btn-zoom-slice').addEventListener('click', () => {
    state.sliceZoomed = !state.sliceZoomed;
    document.getElementById('btn-zoom-slice').textContent = state.sliceZoomed ? 'Normal Scan Size' : 'Enlarge Scan';
    document.querySelectorAll('.slice-viewport').forEach((vp) => vp.classList.toggle('zoomed', state.sliceZoomed));
  });

  document.getElementById('btn-open-fullpage').addEventListener('click', () => {
    const q = state.filteredQuestions[state.currentIndex];
    if (q) openFullPageModal(q.year, q.page);
  });

  // Timer Controls
  document.getElementById('btn-timer-pause').addEventListener('click', () => {
    state.timerPaused = !state.timerPaused;
    document.getElementById('btn-timer-pause').textContent = state.timerPaused ? 'Resume' : 'Pause';
  });
  document.getElementById('btn-timer-reset').addEventListener('click', () => {
    state.timerSeconds = 0;
    updateTimerDisplay();
  });
  document.getElementById('btn-timer-zen').addEventListener('click', () => {
    state.zenTimer = !state.zenTimer;
    document.getElementById('timer-display-wrap').hidden = state.zenTimer;
    document.getElementById('btn-timer-zen').textContent = state.zenTimer ? 'Show Timer' : 'Hide Timer';
  });

  // Solver Actions
  document.getElementById('btn-check-answer').addEventListener('click', handleCheckAnswer);
  document.getElementById('btn-show-hint').addEventListener('click', () => {
    document.getElementById('q-hint-box').hidden = false;
  });
  document.getElementById('btn-close-hint').addEventListener('click', () => {
    document.getElementById('q-hint-box').hidden = true;
  });
  document.getElementById('btn-triage-skip').addEventListener('click', handleStrategicSkip);

  // Self-Rating Buttons
  document.querySelectorAll('#reflection-chips .btn-rate').forEach((btn) => {
    btn.addEventListener('click', () => {
      const q = state.filteredQuestions[state.currentIndex];
      if (!q) return;
      recordQuestionRating(q, btn.dataset.tag);
    });
  });

  // Custom Key Override
  document.getElementById('btn-save-custom-key').addEventListener('click', () => {
    const q = state.filteredQuestions[state.currentIndex];
    if (!q) return;
    const val = document.getElementById('input-custom-key').value.trim().toUpperCase();
    if (!val) return;
    state.progress.customKeys[q.id] = val;
    saveProgressToStorage();
    handleCheckAnswer();
  });

  // Personal Note
  document.getElementById('q-user-note').addEventListener('input', (e) => {
    const q = state.filteredQuestions[state.currentIndex];
    if (!q) return;
    const txt = e.target.value;
    if (txt.trim()) state.progress.notes[q.id] = txt;
    else delete state.progress.notes[q.id];
    saveProgressToStorage();
  });

  // View 4: Past Papers & 40-Min Timer
  document.getElementById('btn-start-triage-sim').addEventListener('click', loadSimulatorSection);
  document.getElementById('btn-grade-triage').addEventListener('click', gradeSimulatorTriage);
  document.getElementById('btn-sim-clock-toggle').addEventListener('click', toggleSimClock);
  document.getElementById('btn-sim-clock-reset').addEventListener('click', resetSimClock);
  document.getElementById('btn-launch-r1-queue').addEventListener('click', launchSimulatorRound1Queue);

  // Modals
  document.getElementById('btn-close-fullpage').addEventListener('click', () => {
    document.getElementById('modal-fullpage').hidden = true;
  });
  document.getElementById('btn-modal-prev-page').addEventListener('click', () => {
    if (state.modalPage > 1) openFullPageModal(state.modalYear, state.modalPage - 1);
  });
  document.getElementById('btn-modal-next-page').addEventListener('click', () => {
    const maxP = MAX_PAGES_BY_YEAR[state.modalYear] || 50;
    if (state.modalPage < maxP) openFullPageModal(state.modalYear, state.modalPage + 1);
  });

  document.getElementById('btn-open-backup').addEventListener('click', () => {
    document.getElementById('modal-backup').hidden = false;
  });
  document.getElementById('btn-close-backup').addEventListener('click', () => {
    document.getElementById('modal-backup').hidden = true;
  });
  document.getElementById('btn-export-json').addEventListener('click', exportProgressJson);
  document.getElementById('input-import-json').addEventListener('change', importProgressJson);
  document.getElementById('btn-reset-progress').addEventListener('click', () => {
    if (confirm('Clear all saved study progress, confidence ratings, and notes?')) {
      state.progress = {
        activeDay: 1,
        darkMode: state.progress.darkMode,
        attempts: {},
        skillConfidence: {},
        customKeys: {},
        notes: {}
      };
      saveProgressToStorage();
      renderStudyPlanView();
      renderSkillsView();
      renderCurrentQuestion();
      document.getElementById('modal-backup').hidden = true;
    }
  });
}

/* ============================================================================
   VIEW 1: 6-DAY STUDY PLAN (FLAT TIMETABLE & LEDGER)
   ============================================================================ */
function renderStudyPlanView() {
  const activeDayObj = SPRINT_DAYS.find((d) => d.day === state.activeSprintDay) || SPRINT_DAYS[0];
  const dayIds = activeDayObj.modules.flatMap((m) => m.qIds);
  const dayDone = dayIds.filter((id) => Boolean(state.progress.attempts[id])).length;

  // Update Ledger Summary Strip
  document.getElementById('stat-day-progress').textContent = `${dayDone} / ${dayIds.length}`;
  document.getElementById('stat-day-note').textContent = `Day ${activeDayObj.day} (${activeDayObj.shortTitle})`;

  let easyTotal = 0;
  let easyCorrect = 0;
  let smartSkips = 0;

  Object.entries(state.progress.attempts).forEach(([qid, att]) => {
    const q = state.qById[qid];
    if (!q) return;
    if (att.status === 'triage' || att.tag === 'triage') {
      smartSkips += 1;
      return;
    }
    if (q.difficulty === 'Easy') {
      easyTotal += 1;
      if (att.correct !== false) easyCorrect += 1;
    }
  });

  document.getElementById('stat-easy-acc').textContent =
    easyTotal > 0 ? `${Math.round((easyCorrect / easyTotal) * 100)}%` : 'Ready';
  document.getElementById('stat-easy-note').textContent =
    easyTotal > 0 ? `${easyCorrect} of ${easyTotal} easy questions correct` : 'Target 85%+ on easy questions';
  document.getElementById('stat-smart-skips').textContent = String(smartSkips);
  document.getElementById('stat-focus-skills').textContent = String(getFocusSkillCount());

  // Render Horizontal 6-Day Selector Bar
  const tabsBar = document.getElementById('day-tabs-bar');
  tabsBar.innerHTML = SPRINT_DAYS.map((d) => {
    const qIds = d.modules.flatMap((m) => m.qIds);
    const done = qIds.filter((id) => Boolean(state.progress.attempts[id])).length;
    const isActive = d.day === state.activeSprintDay;
    return `
      <button class="day-tab-btn ${isActive ? 'active' : ''}" role="tab" aria-selected="${isActive}" data-daytab="${d.day}">
        <span class="day-tab-num">DAY ${d.day}</span>
        <span class="day-tab-title">${escapeHtml(d.shortTitle)}</span>
        <span class="day-tab-count">${done} / ${qIds.length} done</span>
      </button>
    `;
  }).join('');

  tabsBar.querySelectorAll('[data-daytab]').forEach((btn) => {
    btn.addEventListener('click', () => {
      state.activeSprintDay = parseInt(btn.dataset.daytab, 10);
      state.progress.activeDay = state.activeSprintDay;
      saveProgressToStorage();
      renderStudyPlanView();
    });
  });

  // Render Active Day Study Sheet as a Flat Ledger Table (zero nested cards)
  const sheet = document.getElementById('active-day-sheet');
  const blocksHtml = activeDayObj.modules
    .map((m) => {
      const mDone = m.qIds.filter((id) => Boolean(state.progress.attempts[id])).length;
      const rowsHtml = m.qIds
        .map((qid) => {
          const q = state.qById[qid];
          if (!q) return '';
          const att = state.progress.attempts[q.id];
          let statusBadge = '<span class="status-tag">Unattempted</span>';
          if (att) {
            if (att.status === 'triage' || att.tag === 'triage') {
              statusBadge = '<span class="status-tag tag-sand">Smart Skip</span>';
            } else if (att.tag === 'weak' || att.correct === false) {
              statusBadge = '<span class="status-tag tag-clay">Needs Practice</span>';
            } else {
              statusBadge = '<span class="status-tag tag-sage">Completed</span>';
            }
          }
          const diffTagClass = q.difficulty === 'Easy' ? 'tag-sage' : q.difficulty === 'Medium' ? 'tag-sand' : 'tag-clay';
          return `
            <tr>
              <td class="tabular"><strong>${escapeHtml(q.id)}</strong></td>
              <td>${escapeHtml(q.section)} (${escapeHtml(q.type)})</td>
              <td>
                <button class="inline-action" data-openskill="${escapeHtml(q.skillId)}">${escapeHtml(q.skillName)}</button>
                <div style="font-size:0.875rem; color:var(--ink-muted);">${escapeHtml(q.hook)}</div>
              </td>
              <td><span class="status-tag ${diffTagClass}">${escapeHtml(q.difficulty)}</span></td>
              <td class="tabular">${escapeHtml(q.expectedTime)}</td>
              <td>${statusBadge}</td>
              <td>
                <button class="btn-quiet btn-compact" data-solveqid="${escapeHtml(q.id)}" data-modid="${escapeHtml(m.id)}">
                  ${att ? 'Review' : 'Solve'}
                </button>
              </td>
            </tr>
          `;
        })
        .join('');

      return `
        <div class="study-block-section">
          <div class="block-title-bar">
            <div>
              <h4>${escapeHtml(m.name)}</h4>
              <span class="block-subtitle">${escapeHtml(m.sub)}</span>
            </div>
            <div style="display:flex; align-items:center; gap:0.75rem;">
              <span class="tabular" style="font-size:0.875rem; color:var(--ink-secondary);">${mDone} of ${m.qIds.length} completed</span>
              <button class="btn-solid btn-compact" data-startblock="${escapeHtml(m.id)}">Practice This Block</button>
            </div>
          </div>
          <table class="ledger-table">
            <thead>
              <tr>
                <th>Question</th>
                <th>Section</th>
                <th>Skill &amp; Topic Focus</th>
                <th>Tier</th>
                <th>Target Time</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
            </tbody>
          </table>
        </div>
      `;
    })
    .join('');

  sheet.innerHTML = `
    <div class="sheet-header">
      <div>
        <h3>${escapeHtml(activeDayObj.title)}</h3>
        <p class="reading-column" style="color:var(--ink-secondary);">${escapeHtml(activeDayObj.goal)}</p>
        <div class="sheet-mindset">${escapeHtml(activeDayObj.mindset)}</div>
      </div>
      <button class="btn-solid" id="btn-sheet-start-day">
        Practice All Day ${activeDayObj.day} Questions (${dayIds.length})
      </button>
    </div>
    ${blocksHtml}
  `;

  document.getElementById('btn-sheet-start-day').addEventListener('click', () => {
    launchPracticeSession(activeDayObj.title, dayIds);
  });

  sheet.querySelectorAll('[data-startblock]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const mod = activeDayObj.modules.find((m) => m.id === btn.dataset.startblock);
      if (mod) launchPracticeSession(mod.name, mod.qIds);
    });
  });

  sheet.querySelectorAll('[data-solveqid]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const qid = btn.dataset.solveqid;
      const mod = activeDayObj.modules.find((m) => m.id === btn.dataset.modid);
      const qIds = mod ? mod.qIds : [qid];
      launchPracticeSession(mod ? mod.name : `Question ${qid}`, qIds, qid);
    });
  });

  sheet.querySelectorAll('[data-openskill]').forEach((btn) => {
    btn.addEventListener('click', () => {
      openSkillInWorkbench(btn.dataset.openskill);
    });
  });
}

/* ============================================================================
   VIEW 2: 24 SKILLS & CHEAT SHEETS WORKBENCH
   ============================================================================ */
function openSkillInWorkbench(skillId) {
  if (!state.skillById[skillId]) return;
  state.selectedSkillId = skillId;
  state.skillSectionFilter = 'ALL';
  state.skillConfFilter = 'ALL';
  document.querySelectorAll('[data-ssec]').forEach((b) => b.classList.toggle('active', b.dataset.ssec === 'ALL'));
  document.querySelectorAll('[data-sconf]').forEach((b) => b.classList.toggle('active', b.dataset.sconf === 'ALL'));
  switchTab('skills');
}

function renderSkillsView() {
  const listCol = document.getElementById('skills-ledger-list');
  const filteredSkills = state.skills.filter((s) => {
    if (state.skillSectionFilter !== 'ALL' && s.section !== state.skillSectionFilter) return false;
    const conf = getEffectiveSkillConfidence(s.id);
    if (state.skillConfFilter !== 'ALL' && conf !== state.skillConfFilter) return false;
    return true;
  });

  if (filteredSkills.length > 0 && !filteredSkills.some((s) => s.id === state.selectedSkillId)) {
    state.selectedSkillId = filteredSkills[0].id;
  }

  // Group filtered skills by section for clean ledger scanability
  const sectionsOrder = ['QA', 'DILR', 'VARC'];
  const sectionNames = {
    QA: 'Quantitative Ability (11 Core Skills)',
    DILR: 'Data Interpretation & Logical Reasoning (6 Set Archetypes)',
    VARC: 'Verbal Ability & Reading Comprehension (7 Question Skills)'
  };

  let ledgerHtml = '';
  sectionsOrder.forEach((sec) => {
    const groupSkills = filteredSkills.filter((s) => s.section === sec);
    if (groupSkills.length === 0) return;
    ledgerHtml += `
      <div class="skill-group-heading">
        <span>${escapeHtml(sectionNames[sec])}</span>
        <span class="tabular">${groupSkills.length} skills</span>
      </div>
    `;
    groupSkills.forEach((s) => {
      const isSelected = s.id === state.selectedSkillId;
      const conf = getEffectiveSkillConfidence(s.id);
      const confLabel = conf === 'confident' ? 'Confident' : conf === 'focus' ? 'Needs Practice' : 'Getting There';
      const confClass = conf === 'confident' ? 'tag-sage' : conf === 'focus' ? 'tag-clay' : 'tag-sand';

      const skillQs = state.questions.filter((q) => q.skillId === s.id);
      const solvedCount = skillQs.filter((q) => {
        const a = state.progress.attempts[q.id];
        return a && a.status !== 'triage';
      }).length;

      ledgerHtml += `
        <div class="skill-row-item ${isSelected ? 'active' : ''}" role="option" aria-selected="${isSelected}" data-skillid="${s.id}">
          <div class="skill-row-main">
            <span class="skill-row-title">${escapeHtml(s.name)}</span>
            <span class="skill-row-meta">${escapeHtml(s.group)} · <span class="tabular">${solvedCount}/${s.totalCount} solved</span> (${s.easyCount} Easy, ${s.mediumCount} Med)</span>
          </div>
          <span class="status-tag ${confClass}">${confLabel}</span>
        </div>
      `;
    });
  });

  if (!ledgerHtml) {
    ledgerHtml = `<div style="padding:1.5rem; color:var(--ink-secondary);">No skills match this filter. Switch back to "All Levels" to view all 24 skills.</div>`;
  }

  listCol.innerHTML = ledgerHtml;
  listCol.querySelectorAll('.skill-row-item').forEach((row) => {
    row.addEventListener('click', () => {
      state.selectedSkillId = row.dataset.skillid;
      renderSkillsView();
    });
  });

  renderSelectedSkillMonograph();
}

function renderSelectedSkillMonograph() {
  const panel = document.getElementById('skill-detail-sheet');
  const s = state.skillById[state.selectedSkillId];
  if (!s) {
    panel.innerHTML = `<div style="padding:1.5rem;">Select any skill on the left to view its formula sheet and practice questions.</div>`;
    return;
  }

  const conf = getEffectiveSkillConfidence(s.id);
  const skillQs = state.questions
    .filter((q) => q.skillId === s.id)
    .sort((a, b) => {
      const rank = { Easy: 1, Medium: 2, Hard: 3 };
      // Sort verified first, then Easy -> Medium -> Hard
      const vA = a.answer ? 0 : 1;
      const vB = b.answer ? 0 : 1;
      if (vA !== vB) return vA - vB;
      return (rank[a.difficulty] || 2) - (rank[b.difficulty] || 2);
    });

  const easyQs = skillQs.filter((q) => q.difficulty === 'Easy');
  const medQs = skillQs.filter((q) => q.difficulty === 'Medium');
  const hardQs = skillQs.filter((q) => q.difficulty === 'Hard');

  const lv = s.levels || {};
  const beg = lv.beginner || {};
  const inter = lv.intermediate || {};
  const adv = lv.advanced || {};
  const df = state.skillDepthFilter || 'ALL';

  const level1Html = (df === 'ALL' || df === 'beginner') ? `
    <div class="depth-level-block">
      <div class="depth-header-row">
        <div>
          <span class="status-tag tag-sage">Level 1 · Beginner / Explain Like I'm 5</span>
          <h4 style="margin-top:0.35rem;">${escapeHtml(beg.title || 'Simple Intuition & Mental Picture')}</h4>
        </div>
        ${easyQs.length > 0 ? `<button class="btn-quiet btn-compact" data-pract-tier="Easy">Try 3 Beginner Warmups (${easyQs.length} Easy)</button>` : ''}
      </div>
      <div class="depth-subblock">
        <span class="depth-sublabel">The Mental Picture</span>
        <p class="reading-column">${escapeHtml(beg.mentalPicture || '')}</p>
      </div>
      <div class="depth-highlight-box">
        <strong>Quick Numbers Example:</strong> ${escapeHtml(beg.toyExample || '')}
      </div>
      <div class="depth-rule-box">
        <strong>Golden Rule to Remember:</strong> ${escapeHtml(beg.goldenRule || '')}
      </div>
    </div>
  ` : '';

  const level2Html = (df === 'ALL' || df === 'intermediate') ? `
    <div class="depth-level-block">
      <div class="depth-header-row">
        <div>
          <span class="status-tag tag-sand">Level 2 · Intermediate / Explain Like I'm 15</span>
          <h4 style="margin-top:0.35rem;">${escapeHtml(inter.title || 'Core Exam Mechanics & Formulas')}</h4>
        </div>
        ${medQs.length > 0 ? `<button class="btn-quiet btn-compact" data-pract-tier="Medium">Practice Intermediate (${medQs.length} Medium)</button>` : ''}
      </div>
      <div class="depth-subblock">
        <span class="depth-sublabel">Step-by-Step Solving Recipe</span>
        <ul class="formula-list">
          ${(inter.stepByStep || []).map((st) => `<li>${escapeHtml(st)}</li>`).join('')}
        </ul>
      </div>
      <div class="depth-subblock">
        <span class="depth-sublabel">Core Formulas &amp; Rules</span>
        <ul class="formula-list">
          ${(inter.formulas || s.formulas || []).map((f) => `<li>${escapeHtml(f)}</li>`).join('')}
        </ul>
      </div>
      ${inter.workedTemplate ? `
        <div class="depth-highlight-box">
          <strong>Worked CAT Archetype:</strong> ${escapeHtml(inter.workedTemplate)}
        </div>
      ` : ''}
      <div class="depth-sand-box">
        <strong>How to Spot First-Pass Easy Questions:</strong> ${escapeHtml(inter.easyTrigger || s.easyTrigger || '')}
      </div>
    </div>
  ` : '';

  const level3Html = (df === 'ALL' || df === 'advanced') ? `
    <div class="depth-level-block">
      <div class="depth-header-row">
        <div>
          <span class="status-tag tag-clay">Level 3 · Advanced / Explain Like I'm 25 (99%ile Pro)</span>
          <h4 style="margin-top:0.35rem;">${escapeHtml(adv.title || '99%ile Speed Shortcuts & Trap Defense')}</h4>
        </div>
        ${(hardQs.length > 0 || medQs.length > 0) ? `<button class="btn-quiet btn-compact" data-pract-tier="Hard">Test Advanced / Trap Questions</button>` : ''}
      </div>
      <div class="depth-subblock">
        <span class="depth-sublabel">99%ile Speed Shortcuts (Bypass Long Algebra)</span>
        <ul class="formula-list">
          ${(adv.speedShortcuts || []).map((sc) => `<li>${escapeHtml(sc)}</li>`).join('')}
        </ul>
      </div>
      <div class="trap-callout">
        <strong>Watch Out For (Common Paper-Setter Trap):</strong> ${escapeHtml(adv.commonTrap || s.commonTrap || '')}
      </div>
      ${adv.bailoutRule ? `
        <div class="depth-highlight-box">
          <strong>45-Second Bailout &amp; Triage Rule:</strong> ${escapeHtml(adv.bailoutRule)}
        </div>
      ` : ''}
    </div>
  ` : '';

  const ex = s.solvedExample;
  const solvedExampleHtml = ex ? `
    <div class="depth-level-block" style="background-color:var(--bg-canvas);">
      <div class="depth-header-row">
        <div>
          <span class="status-tag tabular">${escapeHtml(ex.source || 'Benchmark CAT Example')}</span>
          <h4 style="margin-top:0.35rem;">Solved CAT Example: Concept in Action</h4>
        </div>
        ${ex.qId ? `<button class="btn-solid btn-compact" data-practsingle="${escapeHtml(ex.qId)}">Open ${escapeHtml(ex.qId)} in Desk</button>` : ''}
      </div>

      <div class="depth-highlight-box" style="background-color:var(--bg-sheet);">
        <span class="depth-sublabel" style="display:block; margin-bottom:0.25rem;">The CAT Question</span>
        <p class="reading-column">${escapeHtml(ex.question)}</p>
      </div>

      ${(df === 'ALL' || df === 'beginner') && ex.intuition ? `
        <div class="depth-rule-box">
          <strong>1. Beginner Intuition (Age 5 View):</strong> ${escapeHtml(ex.intuition)}
        </div>
      ` : ''}

      ${(df === 'ALL' || df === 'intermediate') && ex.steps?.length ? `
        <div class="depth-subblock">
          <span class="depth-sublabel">2. Core Exam Walkthrough (Age 15 Step-by-Step)</span>
          <ul class="formula-list">
            ${ex.steps.map((st) => `<li>${escapeHtml(st)}</li>`).join('')}
          </ul>
        </div>
      ` : ''}

      ${(df === 'ALL' || df === 'advanced') && ex.proMove ? `
        <div class="depth-sand-box">
          <strong>3. 99%ile Speed Shortcut &amp; Trap Check (Age 25 Pro View):</strong> ${escapeHtml(ex.proMove)}
        </div>
      ` : ''}

      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem; padding-top:0.35rem;">
        <span class="status-tag tag-sage tabular"><strong>Verified Answer: ${escapeHtml(ex.answer)}</strong></span>
        ${ex.qId ? `<button class="inline-action" data-practsingle="${escapeHtml(ex.qId)}">Try solving this question with the original exam scan</button>` : ''}
      </div>
    </div>
  ` : '';

  const qRowsHtml = skillQs
    .slice(0, 30)
    .map((q) => {
      const att = state.progress.attempts[q.id];
      const diffClass = q.difficulty === 'Easy' ? 'tag-sage' : q.difficulty === 'Medium' ? 'tag-sand' : 'tag-clay';
      let statusTxt = 'Unattempted';
      if (att) {
        if (att.status === 'triage') statusTxt = 'Skipped';
        else if (att.tag === 'weak' || att.correct === false) statusTxt = 'Needs Practice';
        else statusTxt = 'Completed';
      }
      return `
        <tr>
          <td class="tabular"><strong>${escapeHtml(q.id)}</strong></td>
          <td><span class="status-tag ${diffClass}">${escapeHtml(q.difficulty)}</span></td>
          <td>${escapeHtml(q.hook.slice(0, 62))}${q.hook.length > 62 ? '...' : ''}</td>
          <td class="tabular">${escapeHtml(q.expectedTime)}</td>
          <td>${statusTxt}</td>
          <td>
            <button class="btn-quiet btn-compact" data-practsingle="${escapeHtml(q.id)}">Solve</button>
          </td>
        </tr>
      `;
    })
    .join('');

  panel.innerHTML = `
    <div class="monograph-top">
      <div class="monograph-top-row">
        <span class="status-tag">${escapeHtml(s.section)} · ${escapeHtml(s.group)}</span>
        <span class="tabular" style="font-size:0.875rem; color:var(--ink-secondary);">${escapeHtml(s.frequency)} · Target: ${escapeHtml(s.targetTime)}</span>
      </div>
      <h3>${escapeHtml(s.name)}</h3>
      <p class="monograph-tagline">${escapeHtml(s.tagline)}</p>

      <div class="confidence-picker-bar">
        <span class="confidence-label">Your Confidence Level:</span>
        <div class="segmented-group" role="group" aria-label="Set Skill Confidence">
          <button class="seg-btn ${conf === 'focus' ? 'active' : ''}" data-setconf="focus">Needs Practice</button>
          <button class="seg-btn ${conf === 'steady' ? 'active' : ''}" data-setconf="steady">Getting There</button>
          <button class="seg-btn ${conf === 'confident' ? 'active' : ''}" data-setconf="confident">Confident</button>
        </div>
      </div>
    </div>

    <div class="depth-switcher-bar">
      <span class="confidence-label">Explain It To Me As:</span>
      <div class="segmented-group" role="group" aria-label="Select Cheat Sheet Depth Level">
        <button class="seg-btn ${df === 'ALL' ? 'active' : ''}" data-setdepth="ALL">All 3 Levels (Ladder)</button>
        <button class="seg-btn ${df === 'beginner' ? 'active' : ''}" data-setdepth="beginner">Age 5 (Beginner)</button>
        <button class="seg-btn ${df === 'intermediate' ? 'active' : ''}" data-setdepth="intermediate">Age 15 (Core Exam)</button>
        <button class="seg-btn ${df === 'advanced' ? 'active' : ''}" data-setdepth="advanced">Age 25 (99%ile Pro)</button>
      </div>
    </div>

    <div class="monograph-body">
      ${level1Html}
      ${level2Html}
      ${level3Html}
      ${solvedExampleHtml}
    </div>

    <div class="monograph-practice-bar">
      <div>
        <strong>Practice This Skill (${skillQs.length} Questions)</strong>
        <div style="font-size:0.875rem; color:var(--ink-secondary);">${s.easyCount} Easy · ${s.mediumCount} Medium · ${s.hardCount} Hard</div>
      </div>
      <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
        ${easyQs.length > 0 ? `<button class="btn-solid btn-compact" id="btn-skill-warmup3">Start 3 Easy Warmups</button>` : ''}
        ${medQs.length > 0 ? `<button class="btn-quiet btn-compact" id="btn-skill-med">Practice Medium (${medQs.length})</button>` : ''}
        <button class="btn-quiet btn-compact" id="btn-skill-all">Open All ${skillQs.length} in Desk</button>
      </div>
    </div>

    <div class="monograph-q-list">
      <table class="ledger-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Tier</th>
            <th>Theme / Prompt</th>
            <th>Budget</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          ${qRowsHtml}
        </tbody>
      </table>
    </div>
  `;

  panel.querySelectorAll('[data-setdepth]').forEach((btn) => {
    btn.addEventListener('click', () => {
      state.skillDepthFilter = btn.dataset.setdepth;
      renderSelectedSkillMonograph();
    });
  });

  panel.querySelectorAll('[data-pract-tier]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const tier = btn.dataset.practTier;
      if (tier === 'Easy') {
        const unattemptedEasy = easyQs.filter((q) => !state.progress.attempts[q.id]);
        const pick = (unattemptedEasy.length >= 3 ? unattemptedEasy : easyQs).slice(0, 3);
        launchPracticeSession(`${s.name} (Level 1: Easy Warmups)`, pick.map((q) => q.id));
      } else if (tier === 'Medium') {
        launchPracticeSession(`${s.name} (Level 2: Intermediate Core)`, medQs.slice(0, 8).map((q) => q.id));
      } else {
        const pool = hardQs.length > 0 ? [...hardQs, ...medQs.slice(0, 4)] : medQs.slice(0, 6);
        launchPracticeSession(`${s.name} (Level 3: Advanced & Traps)`, pool.map((q) => q.id));
      }
    });
  });

  panel.querySelectorAll('[data-setconf]').forEach((btn) => {
    btn.addEventListener('click', () => {
      state.progress.skillConfidence[s.id] = btn.dataset.setconf;
      saveProgressToStorage();
      renderSkillsView();
    });
  });

  const btnWarmup3 = document.getElementById('btn-skill-warmup3');
  if (btnWarmup3) {
    btnWarmup3.addEventListener('click', () => {
      const unattemptedEasy = easyQs.filter((q) => !state.progress.attempts[q.id]);
      const pick = (unattemptedEasy.length >= 3 ? unattemptedEasy : easyQs).slice(0, 3);
      launchPracticeSession(`${s.name}: 3 Easy Warmups`, pick.map((q) => q.id));
    });
  }

  const btnMed = document.getElementById('btn-skill-med');
  if (btnMed) {
    btnMed.addEventListener('click', () => {
      launchPracticeSession(`${s.name}: Medium Practice`, medQs.slice(0, 8).map((q) => q.id));
    });
  }

  document.getElementById('btn-skill-all').addEventListener('click', () => {
    resetPracticeFilters();
    state.filters.skill = s.id;
    document.getElementById('filter-skill').value = s.id;
    switchTab('practice');
    applyFiltersAndRenderPractice(true);
  });

  panel.querySelectorAll('[data-practsingle]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const qid = btn.dataset.practsingle;
      const q = state.qById[qid];
      // If part of a DILR or RC set, load the whole set so the user has all questions in the set
      if (q && q.setId) {
        const setQs = state.questions.filter((item) => item.setId === q.setId).map((item) => item.id);
        launchPracticeSession(`${s.name} (${q.setQRange})`, setQs, qid);
      } else {
        launchPracticeSession(s.name, skillQs.map((item) => item.id), qid);
      }
    });
  });
}

/* ============================================================================
   VIEW 3: PRACTICE DESK (SOLVER)
   ============================================================================ */
function populateSkillFilterDropdown() {
  const sec = document.getElementById('filter-section').value;
  const select = document.getElementById('filter-skill');
  const prev = select.value;
  const matchingSkills = state.skills.filter((s) => sec === 'ALL' || s.section === sec);

  select.innerHTML =
    `<option value="ALL">All Skills (${matchingSkills.length})</option>` +
    matchingSkills
      .map((s) => `<option value="${escapeHtml(s.id)}">${escapeHtml(s.section)}: ${escapeHtml(s.name)} (${s.totalCount})</option>`)
      .join('');

  if (matchingSkills.some((s) => s.id === prev)) {
    select.value = prev;
  } else {
    select.value = 'ALL';
    state.filters.skill = 'ALL';
  }
}

function resetPracticeFilters() {
  state.activeModule = null;
  state.filters = {
    section: 'ALL',
    skill: 'ALL',
    difficulty: 'ALL',
    year: 'ALL',
    slot: 'ALL',
    status: 'ALL',
    search: ''
  };
  document.getElementById('filter-section').value = 'ALL';
  populateSkillFilterDropdown();
  document.getElementById('filter-difficulty').value = 'ALL';
  document.getElementById('filter-year').value = 'ALL';
  document.getElementById('filter-slot').value = 'ALL';
  document.getElementById('filter-status').value = 'ALL';
  document.getElementById('filter-search-input').value = '';
}

function launchPracticeSession(title, qIds, startQId = null) {
  state.activeModule = { title, qIds };
  switchTab('practice');
  applyFiltersAndRenderPractice(true, startQId);
}

function applyFiltersAndRenderPractice(resetIdx = true, targetQId = null) {
  const strip = document.getElementById('practice-session-bar');
  if (state.activeModule) {
    strip.hidden = false;
    document.getElementById('session-strip-title').textContent = state.activeModule.title;
    const modQs = state.activeModule.qIds.map((id) => state.qById[id]).filter(Boolean);
    const done = modQs.filter((q) => Boolean(state.progress.attempts[q.id])).length;
    document.getElementById('session-strip-count').textContent = `(${done} of ${modQs.length} completed)`;
    state.filteredQuestions = modQs;
  } else {
    strip.hidden = true;
    const f = state.filters;
    const qLower = f.search.toLowerCase();
    state.filteredQuestions = state.questions.filter((q) => {
      if (f.section !== 'ALL' && q.section !== f.section) return false;
      if (f.skill !== 'ALL' && q.skillId !== f.skill) return false;
      if (f.difficulty !== 'ALL' && q.difficulty !== f.difficulty) return false;
      if (f.year !== 'ALL' && String(q.year) !== f.year) return false;
      if (f.slot !== 'ALL' && String(q.slot) !== f.slot) return false;

      const att = state.progress.attempts[q.id];
      const hasKey = Boolean(q.answer || state.progress.customKeys[q.id]);
      if (f.status === 'VERIFIED' && !hasKey) return false;
      if (f.status === 'UNATTEMPTED' && att) return false;
      if (f.status === 'SOLVED' && (!att || att.status === 'triage')) return false;
      if (f.status === 'REVIEW' && (!att || (att.tag !== 'weak' && att.correct !== false))) return false;
      if (f.status === 'SKIPPED' && (!att || att.status !== 'triage')) return false;

      if (qLower) {
        const hay = `${q.id} ${q.skillName} ${q.topic} ${q.subtopic} ${q.hook} ${q.questionText}`.toLowerCase();
        if (!hay.includes(qLower)) return false;
      }
      return true;
    });
  }

  document.getElementById('filtered-count-label').textContent =
    `${state.filteredQuestions.length} question${state.filteredQuestions.length === 1 ? '' : 's'}`;

  if (targetQId) {
    const idx = state.filteredQuestions.findIndex((q) => q.id === targetQId);
    state.currentIndex = idx >= 0 ? idx : 0;
  } else if (resetIdx) {
    if (state.activeModule) {
      const firstOpen = state.filteredQuestions.findIndex((q) => !state.progress.attempts[q.id]);
      state.currentIndex = firstOpen >= 0 ? firstOpen : 0;
    } else {
      state.currentIndex = 0;
    }
  } else if (state.currentIndex >= state.filteredQuestions.length) {
    state.currentIndex = 0;
  }

  renderQuestionPills();
  renderCurrentQuestion();
}

function renderQuestionPills() {
  const container = document.getElementById('question-pills-strip');
  const total = state.filteredQuestions.length;
  const maxShow = 75;
  let start = 0;
  let end = total;
  if (total > maxShow) {
    start = Math.max(0, state.currentIndex - 32);
    end = Math.min(total, start + maxShow);
  }

  const html = [];
  for (let i = start; i < end; i++) {
    const q = state.filteredQuestions[i];
    const att = state.progress.attempts[q.id];
    let stClass = '';
    if (att) {
      if (att.status === 'triage' || att.tag === 'triage') stClass = 'status-triage';
      else if (att.tag === 'weak' || att.correct === false) stClass = 'status-weak';
      else stClass = 'status-nailed';
    }
    const active = i === state.currentIndex ? 'active' : '';
    html.push(
      `<button class="q-pill ${active} ${stClass}" data-qidx="${i}" title="${escapeHtml(q.skillName)} (${q.difficulty})">${escapeHtml(q.id)}</button>`
    );
  }
  container.innerHTML = html.join('');
  container.querySelectorAll('.q-pill').forEach((btn) => {
    btn.addEventListener('click', () => selectQuestionByIndex(parseInt(btn.dataset.qidx, 10)));
  });

  const activeEl = container.querySelector('.q-pill.active');
  if (activeEl) activeEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
}

function selectQuestionByIndex(idx) {
  if (idx < 0 || idx >= state.filteredQuestions.length) return;
  state.currentIndex = idx;
  renderQuestionPills();
  renderCurrentQuestion();
}

function renderCurrentQuestion() {
  const q = state.filteredQuestions[state.currentIndex];
  if (!q) {
    document.getElementById('q-stem-text').textContent = 'No questions match your current filter selection. Click "Reset" to show all questions.';
    document.getElementById('q-interaction-area').innerHTML = '';
    return;
  }

  const savedAttempt = state.progress.attempts[q.id];
  state.currentSelection = savedAttempt?.userAns || '';
  document.getElementById('q-hint-box').hidden = true;
  document.getElementById('q-solution-box').hidden = !savedAttempt;

  startQuestionTimer(savedAttempt?.timeSec || 0);
  renderSetSiblings(q);
  renderLeftPane(q);

  const diffTagClass = q.difficulty === 'Easy' ? 'tag-sage' : q.difficulty === 'Medium' ? 'tag-sand' : 'tag-clay';
  const hasVerifiedKey = Boolean(q.answer || state.progress.customKeys[q.id]);

  document.getElementById('q-badges-row').innerHTML = `
    <span class="status-tag tabular"><strong>${escapeHtml(q.id)}</strong></span>
    <span class="status-tag">${escapeHtml(q.section)} · ${escapeHtml(q.type)}</span>
    <span class="status-tag ${diffTagClass}">${escapeHtml(q.difficulty)}</span>
    ${hasVerifiedKey ? '<span class="status-tag tag-sage">Verified Key</span>' : ''}
  `;

  document.getElementById('q-timer-target').textContent = `/ ${q.expectedTime}`;

  const skillObj = state.skillById[q.skillId];
  document.getElementById('q-skill-bar').innerHTML = `
    <div>
      <strong>Skill:</strong>
      <button class="inline-action" id="btn-jump-current-skill">${escapeHtml(q.skillName)}</button>
      <span style="color:var(--ink-muted);"> (${escapeHtml(q.subtopic)})</span>
    </div>
    <span style="color:var(--ink-secondary);">${escapeHtml(q.strategyRole)}</span>
  `;

  document.getElementById('btn-jump-current-skill').addEventListener('click', () => {
    openSkillInWorkbench(q.skillId);
  });

  document.getElementById('q-stem-text').textContent =
    q.questionText || '(See the original exam scan on the left for the mathematical expression or chart.)';

  // Starting Hint Content (3-Level Progressive Breakdown: 5yo Intuition -> 15yo Formula -> 25yo Pro Shortcut & Trap)
  const lv = skillObj?.levels || {};
  const begRule = lv.beginner?.goldenRule || lv.beginner?.mentalPicture || '';
  const firstFormula = lv.intermediate?.formulas?.[0] || skillObj?.formulas?.[0] || '';
  const proShortcut = lv.advanced?.speedShortcuts?.[0] || '';
  const trapNote = lv.advanced?.commonTrap || skillObj?.commonTrap || '';
  document.getElementById('q-hint-content').innerHTML = `
    <p><strong>Starting Step for This Question:</strong> ${escapeHtml(q.coreMechanic)}</p>
    ${begRule ? `<p style="margin-top:0.45rem;"><strong>Level 1 (Age 5 · Simple Intuition):</strong> ${escapeHtml(begRule)}</p>` : ''}
    ${firstFormula ? `<p style="margin-top:0.45rem;"><strong>Level 2 (Age 15 · Core Formula):</strong> ${escapeHtml(firstFormula)}</p>` : ''}
    ${proShortcut ? `<p style="margin-top:0.45rem;"><strong>Level 3 (Age 25 · 99%ile Speed Shortcut):</strong> ${escapeHtml(proShortcut)}</p>` : ''}
    ${trapNote ? `<p style="margin-top:0.45rem;"><strong>Watch Out For (Trap):</strong> ${escapeHtml(trapNote)}</p>` : ''}
  `;

  renderInteractionControls(q);

  document.getElementById('note-qid-label').textContent = q.id;
  document.getElementById('q-user-note').value = state.progress.notes[q.id] || '';
  document.getElementById('input-custom-key').value = state.progress.customKeys[q.id] || q.answer || '';

  if (savedAttempt) {
    displaySolutionPanel(q, savedAttempt.userAns, savedAttempt.tag);
  }

  if (state.activeModule) {
    const modQs = state.activeModule.qIds.map((id) => state.qById[id]).filter(Boolean);
    const done = modQs.filter((item) => Boolean(state.progress.attempts[item.id])).length;
    document.getElementById('session-strip-count').textContent = `(${done} of ${modQs.length} completed)`;
  }
}

function renderSetSiblings(q) {
  const bar = document.getElementById('set-siblings-bar');
  if (!q.setId) {
    bar.innerHTML = '';
    return;
  }
  const siblings = state.questions.filter((item) => item.setId === q.setId);
  if (siblings.length <= 1) {
    bar.innerHTML = '';
    return;
  }
  bar.innerHTML =
    `<span>Set ${escapeHtml(q.setQRange)}:</span>` +
    siblings
      .map((sib) => {
        const isCurrent = sib.id === q.id;
        return `<button class="q-pill ${isCurrent ? 'active' : ''}" data-sibid="${sib.id}">Q${sib.qNum}</button>`;
      })
      .join('');

  bar.querySelectorAll('[data-sibid]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.sibid;
      const idx = state.filteredQuestions.findIndex((item) => item.id === targetId);
      if (idx >= 0) {
        selectQuestionByIndex(idx);
      } else {
        const targetQ = state.qById[targetId];
        if (targetQ) {
          state.filteredQuestions.splice(state.currentIndex + 1, 0, targetQ);
          selectQuestionByIndex(state.currentIndex + 1);
        }
      }
    });
  });
}

function renderLeftPane(q) {
  const slicesBox = document.getElementById('visual-slices-box');
  const textBox = document.getElementById('text-context-box');
  const titleEl = document.getElementById('left-pane-title');

  const slicesToShow = [];
  const seen = new Set();
  const pushSlice = (s, label) => {
    const k = `${s.page}-${Math.round(s.topPct)}-${Math.round(s.bottomPct)}`;
    if (!seen.has(k)) {
      seen.add(k);
      slicesToShow.push({ ...s, label });
    }
  };

  if (q.section === 'DILR' && q.contextSlices?.length) {
    q.contextSlices.forEach((s, i) =>
      pushSlice(s, `Set Diagram & Stem (Page ${s.page}${q.contextSlices.length > 1 ? `, Part ${i + 1}` : ''})`)
    );
  }
  if (q.questionSlices?.length) {
    q.questionSlices.forEach((s) => pushSlice(s, `Question ${q.qNum} Original Scan (Page ${s.page})`));
  }

  titleEl.textContent = q.setId
    ? `Set Context (${q.setQRange}) & Exam Paper Scan`
    : `Original Exam Paper Scan (CAT ${q.year} Slot ${q.slot}, Page ${q.page})`;

  if (state.visualMode === 'text') {
    slicesBox.hidden = true;
  } else {
    slicesBox.hidden = false;
    slicesBox.innerHTML = slicesToShow
      .map((s) => {
        const sliceH = Math.max(4, s.bottomPct - s.topPct);
        const aspectH = (sliceH * PAGE_ASPECT).toFixed(2);
        const marginTop = -(s.topPct * PAGE_ASPECT).toFixed(2);
        const imgUrl = `./pages/${q.year}/page_${s.page}.webp`;
        return `
          <div class="slice-frame">
            <div class="slice-bar">
              <span>${escapeHtml(s.label)}</span>
              <button class="inline-action" data-openpage="${s.page}">Open Full Page ${s.page}</button>
            </div>
            <div class="slice-viewport ${state.sliceZoomed ? 'zoomed' : ''}" style="aspect-ratio: 100 / ${aspectH};">
              <img src="${imgUrl}" alt="CAT ${q.year} Page ${s.page} Scan" style="margin-top: ${marginTop}%;" loading="lazy" />
            </div>
          </div>
        `;
      })
      .join('');

    slicesBox.querySelectorAll('[data-openpage]').forEach((btn) => {
      btn.addEventListener('click', () => openFullPageModal(q.year, parseInt(btn.dataset.openpage, 10)));
    });
  }

  if (state.visualMode === 'visual') {
    textBox.hidden = true;
  } else {
    const parts = [];
    if (q.directions) parts.push(q.directions);
    if (q.contextText && q.contextText !== q.directions) parts.push(q.contextText);
    textBox.hidden = false;
    if (parts.length > 0) {
      textBox.textContent = parts.join('\n\n');
    } else {
      textBox.innerHTML = `<span style="color:var(--ink-muted);">Standalone ${escapeHtml(q.section)} question. The original exam scan above displays all mathematical notation, symbols, and figures directly from the paper.</span>`;
    }
  }
}

function renderInteractionControls(q) {
  const area = document.getElementById('q-interaction-area');
  const elimMap = state.eliminatedOptions[q.id] || {};

  if (q.type === 'MCQ' && q.options?.length > 0) {
    area.innerHTML = `
      <div class="mcq-options-list">
        ${q.options
          .map((opt) => {
            const isSel = state.currentSelection === opt.id;
            const isElim = Boolean(elimMap[opt.id]);
            return `
              <div class="mcq-option-row">
                <button class="mcq-option-btn ${isSel ? 'selected' : ''} ${isElim ? 'eliminated' : ''}" data-opt="${opt.id}">
                  <span class="opt-letter">${opt.id}</span>
                  <span>${escapeHtml(opt.text)}</span>
                </button>
                <button class="btn-eliminate" data-elim="${opt.id}" title="Cross out option ${opt.id}">Strike</button>
              </div>
            `;
          })
          .join('')}
      </div>
    `;

    area.querySelectorAll('.mcq-option-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.currentSelection = btn.dataset.opt;
        area.querySelectorAll('.mcq-option-btn').forEach((b) => {
          b.classList.toggle('selected', b.dataset.opt === state.currentSelection);
        });
      });
    });

    area.querySelectorAll('.btn-eliminate').forEach((btn) => {
      btn.addEventListener('click', () => {
        const optId = btn.dataset.elim;
        state.eliminatedOptions[q.id] = state.eliminatedOptions[q.id] || {};
        state.eliminatedOptions[q.id][optId] = !state.eliminatedOptions[q.id][optId];
        renderInteractionControls(q);
      });
    });
  } else {
    area.innerHTML = `
      <div class="tita-panel">
        <div class="tita-input-row">
          <label for="tita-answer-input" style="font-weight:600;">Type-In Answer (TITA, No Negative Marking):</label>
          <input type="text" id="tita-answer-input" class="tita-input" value="${escapeHtml(state.currentSelection)}" placeholder="Enter answer..." />
        </div>
        <div class="tita-keypad">
          ${['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '-']
            .map((k) => `<button class="key-btn" data-tkey="${k}">${k}</button>`)
            .join('')}
          <button class="key-btn" data-tkey="BACK">Backspace</button>
          <button class="key-btn" data-tkey="CLEAR">Clear</button>
        </div>
      </div>
    `;

    const inputEl = document.getElementById('tita-answer-input');
    inputEl.addEventListener('input', (e) => {
      state.currentSelection = e.target.value.trim();
    });

    area.querySelectorAll('[data-tkey]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const k = btn.dataset.tkey;
        if (k === 'CLEAR') state.currentSelection = '';
        else if (k === 'BACK') state.currentSelection = state.currentSelection.slice(0, -1);
        else state.currentSelection += k;
        inputEl.value = state.currentSelection;
      });
    });
  }
}

/* ============================================================================
   TIMER, CHECK ANSWER & SKILL CONFIDENCE FEEDBACK
   ============================================================================ */
function parseExpectedTimeSeconds(q) {
  if (!q.expectedTime) return 105;
  const m = q.expectedTime.match(/(\d+(?:\.\d+)?)/);
  if (!m) return 105;
  let mins = parseFloat(m[1]);
  if (q.section === 'DILR' && mins >= 6) mins = mins / 4;
  return Math.round(mins * 60);
}

function startQuestionTimer(initialSec = 0) {
  if (state.timerInterval) clearInterval(state.timerInterval);
  state.timerSeconds = initialSec;
  state.timerPaused = false;
  document.getElementById('btn-timer-pause').textContent = 'Pause';
  updateTimerDisplay();

  state.timerInterval = setInterval(() => {
    if (!state.timerPaused && state.activeTab === 'practice') {
      state.timerSeconds += 1;
      updateTimerDisplay();
    }
  }, 1000);
}

function updateTimerDisplay() {
  const q = state.filteredQuestions[state.currentIndex];
  const mins = Math.floor(state.timerSeconds / 60);
  const secs = state.timerSeconds % 60;
  const el = document.getElementById('q-timer-clock');
  el.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  if (q) {
    el.classList.toggle('over-target', state.timerSeconds > parseExpectedTimeSeconds(q));
  }
}

function normalizeAns(str) {
  return String(str).replace(/\s+/g, '').replace(/^OPTION/i, '').toUpperCase();
}

function handleCheckAnswer() {
  const q = state.filteredQuestions[state.currentIndex];
  if (!q) return;
  state.timerPaused = true;
  document.getElementById('btn-timer-pause').textContent = 'Resume';

  const officialAns = (state.progress.customKeys[q.id] || q.answer || '').trim().toUpperCase();
  const userAns = (state.currentSelection || '').trim().toUpperCase();

  let isCorrect = null;
  if (officialAns && userAns) {
    isCorrect = normalizeAns(userAns) === normalizeAns(officialAns);
  }

  const targetSec = parseExpectedTimeSeconds(q);
  let defaultTag = 'nailed';
  if (isCorrect === false) defaultTag = 'weak';
  else if (state.timerSeconds > targetSec * 1.25) defaultTag = 'steady';

  const existing = state.progress.attempts[q.id];
  const chosenTag = existing?.tag || defaultTag;

  state.progress.attempts[q.id] = {
    status: chosenTag === 'weak' ? 'weak' : 'solved',
    tag: chosenTag,
    correct: isCorrect,
    userAns,
    timeSec: state.timerSeconds,
    ts: Date.now()
  };

  if (isCorrect === false) {
    state.progress.skillConfidence[q.skillId] = 'focus';
  }
  saveProgressToStorage();

  displaySolutionPanel(q, userAns, chosenTag);
  renderQuestionPills();
}

function displaySolutionPanel(q, userAns, activeTag) {
  const box = document.getElementById('q-solution-box');
  const banner = document.getElementById('q-solution-banner');
  const body = document.getElementById('q-solution-body');
  box.hidden = false;

  const officialAns = (state.progress.customKeys[q.id] || q.answer || '').trim().toUpperCase();
  const uNorm = normalizeAns(userAns || '');
  const oNorm = normalizeAns(officialAns);

  document.querySelectorAll('.mcq-option-btn').forEach((btn) => {
    btn.classList.remove('correct', 'wrong');
    const optId = btn.dataset.opt;
    if (oNorm && optId === oNorm) btn.classList.add('correct');
    else if (oNorm && uNorm && optId === uNorm && uNorm !== oNorm) btn.classList.add('wrong');
  });

  if (officialAns) {
    if (uNorm && uNorm === oNorm) {
      banner.className = 'solution-status-bar banner-correct';
      banner.innerHTML = `<span>Correct! Verified Answer: <strong>${escapeHtml(officialAns)}</strong></span><span class="tabular">Time: ${formatSec(state.timerSeconds)} (Budget: ${escapeHtml(q.expectedTime)})</span>`;
    } else if (uNorm) {
      banner.className = 'solution-status-bar banner-wrong';
      banner.innerHTML = `<span>Your Response: ${escapeHtml(userAns)} · Verified Answer: <strong>${escapeHtml(officialAns)}</strong></span><span>Skill marked for review</span>`;
    } else {
      banner.className = 'solution-status-bar banner-info';
      banner.innerHTML = `<span>Verified Answer Key: <strong>${escapeHtml(officialAns)}</strong></span><span class="tabular">Budget: ${escapeHtml(q.expectedTime)}</span>`;
    }
  } else {
    banner.className = 'solution-status-bar banner-info';
    banner.innerHTML = `<span>Solving Approach &amp; Self-Check</span><span>Rate how this felt below or save a key</span>`;
  }

  body.textContent = q.explanation || `Core Approach: ${q.coreMechanic}`;

  document.querySelectorAll('#reflection-chips .btn-rate').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tag === activeTag);
  });
}

function handleStrategicSkip() {
  const q = state.filteredQuestions[state.currentIndex];
  if (!q) return;
  recordQuestionRating(q, 'triage');
  if (state.currentIndex < state.filteredQuestions.length - 1) {
    selectQuestionByIndex(state.currentIndex + 1);
  }
}

function recordQuestionRating(q, tag) {
  const prev = state.progress.attempts[q.id] || {};
  state.progress.attempts[q.id] = {
    status: tag === 'triage' ? 'triage' : tag === 'weak' ? 'weak' : 'solved',
    tag,
    correct: tag === 'weak' ? false : prev.correct ?? true,
    userAns: state.currentSelection || prev.userAns || '',
    timeSec: state.timerSeconds || prev.timeSec || 0,
    ts: Date.now()
  };

  // Sync user's feeling directly to the Skill's confidence level
  if (tag === 'nailed') state.progress.skillConfidence[q.skillId] = 'confident';
  else if (tag === 'steady') state.progress.skillConfidence[q.skillId] = 'steady';
  else if (tag === 'weak') state.progress.skillConfidence[q.skillId] = 'focus';

  saveProgressToStorage();
  displaySolutionPanel(q, state.currentSelection, tag);
  renderQuestionPills();
}

function formatSec(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}m ${s}s`;
}

/* ============================================================================
   VIEW 4: PAST PAPERS & 40-MINUTE SECTION SELECTION
   ============================================================================ */
function loadSimulatorSection() {
  state.simYear = parseInt(document.getElementById('sim-year').value, 10);
  state.simSlot = parseInt(document.getElementById('sim-slot').value, 10);
  state.simSection = document.getElementById('sim-section').value;
  state.simChoices = {};
  document.getElementById('sim-triage-feedback').hidden = true;

  const slotQs = state.questions.filter(
    (q) => q.year === state.simYear && q.slot === state.simSlot && q.section === state.simSection
  );

  const items = [];
  if (state.simSection === 'DILR') {
    const bySet = {};
    slotQs.forEach((q) => {
      const k = q.setId || q.id;
      if (!bySet[k]) bySet[k] = [];
      bySet[k].push(q);
    });
    Object.values(bySet).forEach((group, idx) => {
      const first = group[0];
      items.push({
        itemId: first.setId || first.id,
        title: `Set ${idx + 1} (${first.setQRange || `Q${first.qNum}`}): ${first.subtopic}`,
        skillName: first.skillName,
        difficulty: first.difficulty,
        expectedTime: first.expectedTime,
        preview: (first.contextText || first.questionText).slice(0, 280) + '...',
        qIds: group.map((g) => g.id)
      });
    });
  } else {
    slotQs.forEach((q) => {
      items.push({
        itemId: q.id,
        title: `Q${q.qNum} (${q.type}): ${q.subtopic}`,
        skillName: q.skillName,
        difficulty: q.difficulty,
        expectedTime: q.expectedTime,
        preview: q.questionText.slice(0, 220) + (q.questionText.length > 220 ? '...' : ''),
        qIds: [q.id]
      });
    });
  }

  state.simItems = items;
  renderSimulatorSheet();
  updateSimBucketCounts();
}

function renderSimulatorSheet() {
  const sheet = document.getElementById('sim-cards-grid');
  sheet.innerHTML = state.simItems
    .map((it) => {
      const choice = state.simChoices[it.itemId] || '';
      return `
        <div class="paper-item-row">
          <div>
            <div class="paper-item-title">
              ${escapeHtml(it.title)}
              <span class="status-tag" style="margin-left:0.4rem;">${escapeHtml(it.skillName)}</span>
            </div>
            <p class="paper-item-preview">${escapeHtml(it.preview)}</p>
          </div>
          <div class="paper-item-actions">
            <button class="triage-choice-btn ${choice === 'R1' ? 'selected-r1' : ''}" data-itemid="${it.itemId}" data-b="R1">
              First Pass (Round 1)
            </button>
            <button class="triage-choice-btn ${choice === 'R2' ? 'selected-r2' : ''}" data-itemid="${it.itemId}" data-b="R2">
              Second Pass (Round 2)
            </button>
            <button class="triage-choice-btn ${choice === 'R3' ? 'selected-r3' : ''}" data-itemid="${it.itemId}" data-b="R3">
              Skip
            </button>
            <button class="btn-quiet btn-compact" data-opensimitem="${it.itemId}">Open</button>
          </div>
        </div>
      `;
    })
    .join('');

  sheet.querySelectorAll('.triage-choice-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      state.simChoices[btn.dataset.itemid] = btn.dataset.b;
      renderSimulatorSheet();
      updateSimBucketCounts();
    });
  });

  sheet.querySelectorAll('[data-opensimitem]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const it = state.simItems.find((x) => x.itemId === btn.dataset.opensimitem);
      if (it) launchPracticeSession(`CAT ${state.simYear} Slot ${state.simSlot}: ${it.title}`, it.qIds);
    });
  });
}

function updateSimBucketCounts() {
  const vals = Object.values(state.simChoices);
  document.getElementById('count-r1').textContent = String(vals.filter((v) => v === 'R1').length);
  document.getElementById('count-r2').textContent = String(vals.filter((v) => v === 'R2').length);
  document.getElementById('count-r3').textContent = String(vals.filter((v) => v === 'R3').length);
}

function gradeSimulatorTriage() {
  const fb = document.getElementById('sim-triage-feedback');
  fb.hidden = false;

  let matches = 0;
  let totalTagged = 0;
  const rows = [];

  state.simItems.forEach((it) => {
    const userB = state.simChoices[it.itemId];
    const idealB = it.difficulty === 'Easy' ? 'R1' : it.difficulty === 'Medium' ? 'R2' : 'R3';
    if (userB) {
      totalTagged += 1;
      if (userB === idealB || (userB === 'R1' && idealB === 'R2' && state.simSection === 'DILR')) {
        matches += 1;
      }
    }
    rows.push(
      `<li><strong>${escapeHtml(it.title)}</strong>: Brief Calibration is <strong>${escapeHtml(it.difficulty)} (${escapeHtml(it.expectedTime)})</strong> · Your Selection: <strong>${userB || 'Not tagged'}</strong></li>`
    );
  });

  const pct = totalTagged > 0 ? Math.round((matches / totalTagged) * 100) : 0;
  fb.innerHTML = `
    <h4 style="margin-bottom:0.35rem;">Section Selection Check: ${totalTagged > 0 ? `${pct}% alignment (${matches} of ${totalTagged})` : 'Tag items into First Pass, Second Pass, or Skip below'}</h4>
    <ul style="padding-left:1.25rem; display:flex; flex-direction:column; gap:0.25rem; font-size:0.9375rem;">
      ${rows.join('')}
    </ul>
  `;
}

function launchSimulatorRound1Queue() {
  const r1 = state.simItems.filter((it) => state.simChoices[it.itemId] === 'R1');
  const r2 = state.simItems.filter((it) => state.simChoices[it.itemId] === 'R2');
  const ordered = [...r1, ...r2];
  const finalItems = ordered.length > 0 ? ordered : state.simItems.filter((it) => it.difficulty !== 'Hard');
  launchPracticeSession(
    `CAT ${state.simYear} Slot ${state.simSlot} (${state.simSection} Queue)`,
    finalItems.flatMap((it) => it.qIds)
  );
}

function toggleSimClock() {
  state.simClockRunning = !state.simClockRunning;
  document.getElementById('btn-sim-clock-toggle').textContent = state.simClockRunning ? 'Pause Clock' : 'Resume Clock';
  if (state.simClockRunning && !state.simClockInterval) {
    state.simClockInterval = setInterval(() => {
      if (state.simClockRunning && state.simClockSeconds > 0) {
        state.simClockSeconds -= 1;
        const m = Math.floor(state.simClockSeconds / 60);
        const s = state.simClockSeconds % 60;
        document.getElementById('sim-clock').textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
      }
    }, 1000);
  }
}

function resetSimClock() {
  state.simClockRunning = false;
  state.simClockSeconds = 40 * 60;
  document.getElementById('sim-clock').textContent = '40:00';
  document.getElementById('btn-sim-clock-toggle').textContent = 'Start 40-Min Clock';
}

/* ============================================================================
   MODALS & UTILITIES
   ============================================================================ */
function openFullPageModal(year, page) {
  state.modalYear = year;
  state.modalPage = page;
  const maxP = MAX_PAGES_BY_YEAR[year] || 50;
  document.getElementById('modal-fullpage-title').textContent =
    `Original Exam Paper: CAT ${year} (Page ${page} of ${maxP})`;
  document.getElementById('modal-fullpage-img').src = `./pages/${year}/page_${page}.webp`;
  document.getElementById('modal-fullpage').hidden = false;
}

function exportProgressJson() {
  const dataStr = JSON.stringify(state.progress, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `cat_study_desk_backup_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function importProgressJson(e) {
  const file = e.target.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    try {
      const parsed = JSON.parse(ev.target.result);
      state.progress = {
        ...state.progress,
        ...parsed,
        attempts: parsed.attempts || {},
        skillConfidence: parsed.skillConfidence || {},
        customKeys: parsed.customKeys || {},
        notes: parsed.notes || {}
      };
      saveProgressToStorage();
      renderStudyPlanView();
      renderSkillsView();
      renderCurrentQuestion();
      document.getElementById('modal-backup').hidden = true;
      alert('Study progress restored.');
    } catch (err) {
      alert('Could not parse backup file.');
    }
  };
  reader.readAsText(file);
}

function escapeHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
