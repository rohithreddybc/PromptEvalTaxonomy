"""
Generate PRISMA 2020 flowchart PNG matching the existing structure but with
numbers covering all five rounds (primary + 4 expansions -> 153 final papers).

Reproduces:
  prisma_flowchart.png

The numbers below are pulled from Table 4 (tab:expansion_rounds) in main.tex:
  Round 0:  2,847 identified ->   412 screened (FT) ->   354 excluded ->  80 added
  Round 1:    118 identified ->   118 screened (FT) ->    98 excluded ->  20 added
  Round 2:     74 identified ->    74 screened (FT) ->    63 excluded ->  11 added
  Round 3:    212 identified ->   212 screened (FT) ->   177 excluded ->  35 added
  Round 4:     46 identified ->    46 screened (FT) ->    39 excluded ->   7 added
  Total:    3,297 identified ->   862 screened (FT) ->   731 excluded -> 153 corpus

  Round 0 title/abstract screening: 2,847 -> 2,435 excluded -> 412 to FT review
  Round 0 venue filter: 129 passed FT -> 71 venue-excluded, 58 retained
  Round 0 citation search: +22 -> 80 (round 0 corpus)
  Then expansions: +20 +11 +35 +7 = 73 -> 153 final corpus
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import os

# ---- canvas ----------------------------------------------------------------
fig_w, fig_h = 5.6, 8.7  # inches
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 158)
ax.set_aspect("auto")
ax.axis("off")

# ---- color palette ---------------------------------------------------------
COL_TITLE      = "#1f4e79"
COL_BOX        = "#e9eff7"
COL_BOX_EDGE   = "#1f4e79"
COL_SIDE       = "#fff7d6"
COL_SIDE_EDGE  = "#bf9000"
COL_FINAL      = "#c6e6c6"
COL_FINAL_EDGE = "#1f6b3f"

PHASE_COLORS = {
    "IDENTIFICATION": "#5b3a8a",
    "SCREENING":      "#b14143",
    "ELIGIBILITY":    "#d68633",
    "INCLUDED":       "#3b8c5a",
}

# ---- title -----------------------------------------------------------------
ax.text(50, 154, "PRISMA 2020 Screening Flowchart",
        ha="center", va="center", fontsize=11.5, weight="bold",
        color=COL_TITLE)

# ---- helpers ---------------------------------------------------------------
def main_box(x, y, w, h, text, fontsize=6.6, color=COL_BOX, edge=COL_BOX_EDGE, weight="normal"):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4",
                          linewidth=0.9, edgecolor=edge, facecolor=color)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, weight=weight, color="#1a1a1a")

def side_box(x, y, w, h, text, fontsize=6.0):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                          linewidth=0.8, edgecolor=COL_SIDE_EDGE, facecolor=COL_SIDE)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color="#1a1a1a")

def arrow_down(x_from, y_from, x_to, y_to):
    arr = FancyArrowPatch((x_from, y_from), (x_to, y_to),
                          arrowstyle="->", mutation_scale=11,
                          linewidth=0.9, color="#444444")
    ax.add_patch(arr)

def arrow_right(x_from, y_from, x_to, y_to):
    arr = FancyArrowPatch((x_from, y_from), (x_to, y_to),
                          arrowstyle="->", mutation_scale=11,
                          linewidth=0.9, color="#444444")
    ax.add_patch(arr)

def phase_band(y_top, y_bot, label):
    color = PHASE_COLORS[label]
    rect = patches.Rectangle((1, y_bot), 7, y_top - y_bot,
                             linewidth=0, facecolor=color)
    ax.add_patch(rect)
    ax.text(4.5, (y_top + y_bot) / 2, label,
            ha="center", va="center", fontsize=8.0, color="white",
            weight="bold", rotation=90)

# ---- layout coords (column anchors) ----------------------------------------
COL_MAIN_X   = 16
COL_MAIN_W   = 50
COL_SIDE_X   = 71
COL_SIDE_W   = 27

# ---- phase bands -----------------------------------------------------------
phase_band(149.5, 116.0, "IDENTIFICATION")
phase_band(115.5,  72.0, "SCREENING")
phase_band( 71.5,  38.0, "ELIGIBILITY")
phase_band( 37.5,   3.0, "INCLUDED")

# =========================================================================
# IDENTIFICATION
# =========================================================================
main_box(COL_MAIN_X, 122, COL_MAIN_W, 26,
         ("Records identified from:\n"
          "  - Round 0 (primary, n=6 databases): 2,847 after dedup\n"
          "    arXiv, ACM DL, IEEE Xplore, Semantic Scholar, Scopus, WoS\n"
          "  - Round 1-4 (targeted expansions, same 6 databases): 450\n"
          "Total records identified: n = 3,297"),
         fontsize=6.4)

# =========================================================================
# SCREENING
# =========================================================================
# Title/abstract screening (round 0 only)
main_box(COL_MAIN_X, 100, COL_MAIN_W, 13,
         "Records screened by title and abstract\n"
         "Round 0:  n = 2,847\n"
         "Rounds 1-4 (targeted): went directly to full-text review",
         fontsize=6.4)
arrow_down(COL_MAIN_X + COL_MAIN_W/2, 122, COL_MAIN_X + COL_MAIN_W/2, 113)

side_box(COL_SIDE_X, 102, COL_SIDE_W, 9,
         "Records excluded\nat title/abstract\n(round 0): n = 2,435",
         fontsize=5.8)
arrow_right(COL_MAIN_X + COL_MAIN_W, 106.5, COL_SIDE_X, 106.5)

# Full-text screening (combined all rounds)
main_box(COL_MAIN_X, 80, COL_MAIN_W, 13,
         "Reports assessed for eligibility (full-text review)\n"
         "Round 0: 412     Rounds 1-4: 118 + 74 + 212 + 46 = 450\n"
         "Total full-text reviewed: n = 862",
         fontsize=6.4)
arrow_down(COL_MAIN_X + COL_MAIN_W/2, 100, COL_MAIN_X + COL_MAIN_W/2, 93)

# =========================================================================
# ELIGIBILITY
# =========================================================================
side_box(COL_SIDE_X, 76, COL_SIDE_W, 17,
         "Reports excluded at\nfull-text (n = 731):\n"
         "  - Prompting as tool: 181\n"
         "  - Domain-specific:    64\n"
         "  - No full-text:       24\n"
         "  - Non-English:        14\n"
         "  - Expansion rounds:  448",
         fontsize=5.4)
arrow_right(COL_MAIN_X + COL_MAIN_W, 86.5, COL_SIDE_X, 86.5)

# Venue filter on round-0 papers
main_box(COL_MAIN_X, 58, COL_MAIN_W, 13,
         "Reports that passed full-text review\n"
         "Round 0: 129    Rounds 1-4: 131\n"
         "Total passed full-text: n = 260",
         fontsize=6.4)
arrow_down(COL_MAIN_X + COL_MAIN_W/2, 80, COL_MAIN_X + COL_MAIN_W/2, 71)

side_box(COL_SIDE_X, 54, COL_SIDE_W, 17,
         "Round-0 venue filter\n(peer-review / venue tier):\n"
         "  - Excluded: 71\n"
         "  - Retained:  58\n"
         "Expansion rounds:\n"
         "venue-filtered at\nintake (all 131 kept)",
         fontsize=5.4)
arrow_right(COL_MAIN_X + COL_MAIN_W, 64.5, COL_SIDE_X, 64.5)

# =========================================================================
# INCLUDED
# =========================================================================
# Aggregated inclusion box
main_box(COL_MAIN_X, 36, COL_MAIN_W, 16,
         "Total reports for inclusion\n"
         "Round 0:  venue-filtered (58) + citation search (22) = 80\n"
         "Rounds 1-4 (targeted expansions): 20 + 11 + 35 + 7 = 73\n"
         "Total eligible: n = 153",
         fontsize=6.4)
arrow_down(COL_MAIN_X + COL_MAIN_W/2, 58, COL_MAIN_X + COL_MAIN_W/2, 52)

side_box(COL_SIDE_X, 36, COL_SIDE_W, 16,
         "Round 0 citation search:\n"
         "  Backward / forward,\n"
         "  +22 papers\n\n"
         "Rounds 1-4 (Table 4):\n"
         "  +73 papers",
         fontsize=5.4)
arrow_right(COL_MAIN_X + COL_MAIN_W, 44, COL_SIDE_X, 44)

# Final corpus box
main_box(COL_MAIN_X + 5, 12, COL_MAIN_W - 10, 14,
         "FINAL CORPUS\nn = 153 papers",
         fontsize=10.0, color=COL_FINAL, edge=COL_FINAL_EDGE, weight="bold")
arrow_down(COL_MAIN_X + COL_MAIN_W/2, 36, COL_MAIN_X + COL_MAIN_W/2, 26)

# ---- save ------------------------------------------------------------------
out_path = os.path.abspath("prisma_flowchart.png")
plt.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
print(f"wrote {out_path}")
print(f"  size: {os.path.getsize(out_path)} bytes")
