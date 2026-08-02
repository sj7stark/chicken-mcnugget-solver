# 🥔 Chicken McNugget Problem Solver

A [Streamlit](https://streamlit.io) web app that solves the **Chicken Nugget
Problem** (a.k.a. the **Frobenius coin problem**): given 2–5 nugget pack
sizes, find the **largest number of nuggets that cannot be purchased
exactly** — or prove that no such largest number exists.

Built by [Steven Stark](https://www.linkedin.com/in/steven-stark).

## The app

Five pages, reachable from the sidebar:

| Page | What it does |
|---|---|
| **Home** | Explains the Chicken Nugget Problem with the classic 6/9/20 example, and links to the Problem Solver and The Math |
| **Problem Solver** | Pick how many pack sizes you have (2–5), enter each one (integers 2–100), hit **Solve**, and get the answer — or an animated **No Solution** verdict with falling nuggets. **Clear** resets the page |
| **The Math** | When a solution exists (the gcd test), the Chicken McNugget Theorem, and the residue-class (Apéry set) method |
| **About the Creator** | Background, education, career highlights, and patents |
| **Sources** | Numbered citations for every mathematical claim |

## How the solver works

**Existence check** — a Frobenius number exists **iff**
`gcd(p1, ..., pk) == 1`. If the gcd is greater than 1, every purchasable
amount is a multiple of it, so infinitely many amounts are unreachable and
the app reports **No Solution**.

**Residue-class table / Apéry set (instant).** With
`a = min(pack_sizes)`, compute for each residue `r` mod `a` the smallest
purchasable amount `w_r` in that class (the *Apéry set*), using
Nijenhuis's Dijkstra-based shortest-path algorithm on a graph with one
node per residue. Then `n` is purchasable iff `n >= w[n % a]`, and the
answer comes straight from the Brauer–Shockley formula
`g = max(w_r) - a` — no scanning loop at all. See The Math page,
section 3, and Sources [6]–[8]. The computation is effectively instant
for every allowed input.

## Project structure

```
chicken-mcnugget-solver/
├── streamlit_app.py          # Home page + st.navigation (entry point)
├── 🥔_Chicken_McNugget_Problem_Solver.py  # Deployment shim → streamlit_app.main()
├── pages/
│   ├── 1_Problem_Solver.py   # Input UI + solve/clear flow
│   ├── 2_The_Math.py         # Existence test, theorem, Apéry method
│   ├── 3_About_the_Author.py # Bio, education, career summary, patents
│   └── 4_Sources.py          # Citations
├── core/
│   ├── solver.py             # gcd test + Apéry set + Brauer–Shockley
│   └── ui.py                 # Shared UI helpers (animations, emoji box)
├── assets/                   # Images (nugget photos, theorem figure, logos/)
├── tests/test_solver.py      # Unit tests (DP oracle cross-checks)
├── requirements.txt
├── LICENSE
└── .streamlit/config.toml    # Warm golden theme
```

The emoji-named file at the root is a thin shim: the deployed Streamlit
Community Cloud app was created with that file as its main module, and
Streamlit Cloud cannot change an app's main file after creation. The shim
imports `streamlit_app` and calls its `main()` so both entry points render the
identical app.

## Run locally

Requires Python 3.9+ (3.11 recommended).

```bash
git clone https://github.com/sj7stark/chicken-mcnugget-solver.git
cd chicken-mcnugget-solver
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

The Apéry-set solver is verified against an independent dynamic-programming
oracle on dozens of randomized cases plus a table of known answers
(including the classic 6, 9, 20 → 43).

## Sources

See the in-app **Sources** page for the full numbered citation list
(Art of Problem Solving, Wikipedia's coin-problem article, Sylvester 1882,
Ramírez Alfonsín's *The Diophantine Frobenius Problem*, Brilliant.org,
Apéry 1946, Brauer & Shockley 1962, and Nijenhuis 1979).

## License

Released under the [MIT License](LICENSE) — © 2026 Steven Stark.
