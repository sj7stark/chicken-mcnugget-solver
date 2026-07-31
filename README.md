# 🍗 Chicken Nugget Problem Solver

A [Streamlit](https://streamlit.io) web app that solves the **Chicken Nugget
Problem** (a.k.a. the **Frobenius coin problem**): given 2–5 nugget pack
sizes, find the **largest number of nuggets that cannot be purchased
exactly** — or prove that no such largest number exists.

Built by [Steven Stark](https://www.linkedin.com/in/steven-stark).

## The app

| Page | What it does |
|---|---|
| **Landing** | What the Chicken Nugget Problem is, plus original nugget artwork |
| **Problem Solver** | Pick 2–5 pack sizes (integers 2–100), hit **Solve**, and get the answer — or an animated **No Solution** verdict with falling nuggets |
| **The Math** | When a solution exists (the gcd test), the Chicken McNugget Theorem, and the CP-SAT search algorithm |
| **About the Author** | Background, education, and career highlights |
| **Sources** | Numbered citations for every mathematical claim |

## How the solver works

**Existence check** (both approaches) — a Frobenius number exists **iff**
`gcd(p1, ..., pk) == 1`. If the gcd is greater than 1, every purchasable
amount is a multiple of it, so infinitely many amounts are unreachable and
the app reports **No Solution**.

The Problem Solver page offers two approaches via a dropdown:

1. **Residue-class table / Apéry set (default — instant).** With
   `a = min(pack_sizes)`, compute for each residue `r` mod `a` the smallest
   purchasable amount `w_r` in that class (the *Apéry set*), using
   Nijenhuis's Dijkstra-based shortest-path algorithm on a graph with one
   node per residue. Then `n` is purchasable iff `n >= w[n % a]`, and the
   answer comes straight from the Brauer–Shockley formula
   `g = max(w_r) - a` — no scanning loop at all. See The Math page,
   section 4, and Sources [8]–[10].
2. **Sliding-window CP-SAT search.** For `N = 1, 2, 3, ...` the app asks
   [Google OR-Tools' CP-SAT solver](https://developers.google.com/optimization/cp)
   whether `p1*x1 + ... + pk*xk == N` has any solution in non-negative
   integers (a pure feasibility model — no objective function). A counter
   starts at `max(pack_sizes)`; each representable `N` decrements it, each
   non-representable `N` records `answer = N` and resets it. When the counter
   hits 0 — i.e. `max(pack_sizes)` consecutive amounts were all purchasable —
   no unreachable amount can ever occur again, and `answer` is returned.

The two approaches always agree (unit-tested); they differ in speed and in
what they demonstrate — number theory versus constraint programming.

> **Note on the algorithm spec:** the implementation follows the project
> owner's algorithm with two small corrections: (1) the counter counts
> consecutive *successes* (the as-specified branch roles would never
> terminate once every amount becomes representable), and (2) the scan
> starts at `N = 1` instead of `max(pack) + 1` so small answers (e.g. packs
> `{2, 3}`, answer `1`) come out right. Both are covered by unit tests.

### Performance fine print

The Apéry-set approach is effectively instant for every allowed input. The
CP-SAT search issues one solve per candidate `N`: everyday inputs (e.g.
`6, 9, 20` → 43) take about a second, while adversarial inputs like
`99, 100` (answer 9,701) require thousands of sequential solves and can take
a few minutes — well within Streamlit Community Cloud's 1 GB resource limit,
just not instant.

## Project structure

```
chicken-nugget-solver/
├── streamlit_app.py          # Landing page (entry point)
├── pages/
│   ├── 1_Problem_Solver.py   # Input UI + solve/clear flow
│   ├── 2_The_Math.py         # Existence test, theorem, algorithm
│   ├── 3_About_the_Author.py # Bio and career summary
│   └── 4_Sources.py          # Citations
├── core/
│   ├── solver.py             # gcd test + CP-SAT feasibility + window search
│   └── ui.py                 # Shared UI helpers (animations, emoji box)
├── assets/                   # Images (see "Artwork & images" below)
├── scripts/generate_images.py# Regenerates the original nugget artwork
├── tests/test_solver.py      # Unit tests (DP oracle + CP-SAT cross-checks)
├── requirements.txt
└── .streamlit/config.toml    # Warm golden theme
```

## Run locally

Requires Python 3.9+ (3.11 recommended).

```bash
git clone <your-github-url>/chicken-nugget-solver.git
cd chicken-nugget-solver
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open http://localhost:8501.

### Run the tests

```bash
python tests/test_solver.py        # no pytest required
# or
python -m pytest tests/ -q
```

The sliding-window logic is verified against an independent
dynamic-programming oracle on dozens of randomized cases; when OR-Tools is
installed, the CP-SAT checker and an end-to-end solve (6, 9, 20 → 43) are
tested as well.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, and click **New app**.
3. Select this repo, branch `main`, and main file `streamlit_app.py`.
4. Click **Deploy** — dependencies install automatically from
   `requirements.txt`. The app fits comfortably in the free tier's 1 GB
   resource allowance (OR-Tools is the largest dependency at ~100 MB
   installed).

## Artwork & images

* The nugget images on the landing page are **original illustrations
  generated programmatically** by `scripts/generate_images.py` (Pillow).
  Nothing is copied or derived from photos or other websites, so there are
  no third-party copyright concerns. Regenerate them any time with
  `python scripts/generate_images.py`.
* Want fancier pictures? Drop any AI-generated nugget images you own into
  `assets/` as `nugget_banner.png` / `nugget_1.png` and they will be picked
  up automatically.
* **Author photo:** save your LinkedIn profile picture as
  `assets/profile.png` (or `.jpg`) and the About page will use it instead of
  the placeholder avatar.
* **Education section:** edit the marked `TODO` block in
  `pages/3_About_the_Author.py`.

## Sources

See the in-app **Sources** page for the full numbered citation list
(Art of Problem Solving, Wikipedia's coin-problem article, Sylvester 1882,
Ramírez Alfonsín's *The Diophantine Frobenius Problem*, Brilliant.org, and
the Google OR-Tools CP-SAT documentation).

## License

No license file yet — add one (e.g. MIT) before making the GitHub repository
public if you want others to reuse the code.
