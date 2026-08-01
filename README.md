# 🥔 Chicken McNugget Problem Solver

A [Streamlit](https://streamlit.io) web app that solves the **Chicken Nugget
Problem** (a.k.a. the **Frobenius coin problem**): given 2–5 nugget pack
sizes, find the **largest number of nuggets that cannot be purchased
exactly** — or prove that no such largest number exists.

Built by [Steven Stark](https://www.linkedin.com/in/steven-stark).

## The app

| Page | What it does |
|---|---|
| **Home** | What the Chicken Nugget Problem is |
| **Problem Solver** | Pick 2–5 pack sizes (integers 2–100), hit **Solve**, and get the answer — or an animated **No Solution** verdict with falling nuggets |
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
├── pages/
│   ├── 1_Problem_Solver.py   # Input UI + solve/clear flow
│   ├── 2_The_Math.py         # Existence test, theorem, Apéry method
│   ├── 3_About_the_Author.py # Bio, career summary, patents
│   └── 4_Sources.py          # Citations
├── core/
│   ├── solver.py             # gcd test + Apéry set + Brauer–Shockley
│   └── ui.py                 # Shared UI helpers (animations, emoji box)
├── assets/                   # Images (nugget photos, logos, figures)
├── scripts/generate_images.py# Regenerates placeholder artwork (unused)
├── tests/test_solver.py      # Unit tests (DP oracle cross-checks)
├── requirements.txt
└── .streamlit/config.toml    # Warm golden theme
```

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

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub
   ([github.com/sj7stark/chicken-mcnugget-solver](https://github.com/sj7stark/chicken-mcnugget-solver)).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, and click **New app**.
3. Select `sj7stark/chicken-mcnugget-solver`, branch `main`, and main file
   `streamlit_app.py`.

> **Note — existing deployment:** the currently deployed app was created
> with `🥔_Chicken_McNugget_Problem_Solver.py` as its main module, and
> Streamlit Cloud cannot change an app's main file after creation. That
> file is kept in the repo as a thin shim that calls
> `streamlit_app.main()`, so the existing deployment keeps working. If you
> delete the app and redeploy with `streamlit_app.py` as the main file,
> you can remove the shim.
4. Click **Deploy** — dependencies install automatically from
   `requirements.txt`. The app fits easily in the free tier's 1 GB
   resource allowance.

## Images

* The chicken nugget photos on the Home page and the organization logos on
  the About page live in `assets/` and were provided by the project owner.
* **Author photo:** `assets/profile.jpg` — replace it to update the About
  page portrait.

## Sources

See the in-app **Sources** page for the full numbered citation list
(Art of Problem Solving, Wikipedia's coin-problem article, Sylvester 1882,
Ramírez Alfonsín's *The Diophantine Frobenius Problem*, Brilliant.org,
Apéry 1946, Brauer & Shockley 1962, and Nijenhuis 1979).

## License

No license file yet — add one (e.g. MIT) before making the GitHub repository
public if you want others to reuse the code.
