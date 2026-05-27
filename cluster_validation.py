"""
cluster_validation.py — Reproduce the cluster-validation checks reported in
Section 8.6 of the paper:

  * Check 1: Silhouette score of the rule-based 3-archetype partition against
             random-baseline shuffles (target: ~0.398 vs ~-0.037 baseline).
  * Check 2: ARI between the rule-based partition and unsupervised clusterings
             produced by KMeans, AgglomerativeClustering (Ward, average),
             GaussianMixture, and SpectralClustering at k=3.
  * Check 3: Silhouette curve for KMeans at k in {2,3,4}.
  * Check 4: Bootstrap co-cluster stability (200 resamples) of the rule-based
             archetypes.

The script consumes corpus_d1d7.csv (152 rows x D1-D7 codings) and prints all
numerical results to stdout. Random seeds are fixed for reproducibility; small
deviations from the paper values are possible depending on scikit-learn
version (tested on scikit-learn >= 1.3).

Usage:
    python cluster_validation.py
"""
from __future__ import annotations

import csv
import sys
from collections import Counter

import numpy as np
from sklearn.cluster import (
    AgglomerativeClustering,
    KMeans,
    SpectralClustering,
)
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.mixture import GaussianMixture


RNG_SEED = 42
CSV_PATH = "corpus_d1d7.csv"
DIMENSIONS = ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]


def load_corpus(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split_combo(value: str) -> list[str]:
    """Split combo codes (e.g. 'JP+AR' or 'LLM-as-Judge, Human') into atoms."""
    parts = []
    for sep in [",", "+", "/"]:
        value = value.replace(sep, "|")
    for p in value.split("|"):
        p = p.strip()
        if p:
            parts.append(p)
    return parts


def one_hot_encode(rows: list[dict]) -> tuple[np.ndarray, list[str]]:
    # Collect canonical levels per dimension
    levels: dict[str, list[str]] = {}
    for d in DIMENSIONS:
        seen: list[str] = []
        seen_set: set[str] = set()
        for row in rows:
            for atom in split_combo(row[d]):
                if atom not in seen_set:
                    seen.append(atom)
                    seen_set.add(atom)
        levels[d] = seen
    feature_names = [f"{d}={lvl}" for d in DIMENSIONS for lvl in levels[d]]
    feature_index: dict[str, int] = {name: i for i, name in enumerate(feature_names)}

    X = np.zeros((len(rows), len(feature_names)), dtype=np.float64)
    for i, row in enumerate(rows):
        for d in DIMENSIONS:
            for atom in split_combo(row[d]):
                X[i, feature_index[f"{d}={atom}"]] = 1.0
    return X, feature_names


def rule_based_archetype(row: dict) -> str:
    """Mutually exclusive A/B/C assignment per Section 8 of the paper.

    Priority order (matches the paper's 101/26/14/11 count):
      1. D1 contains 'Human'                  -> C (Expert-Anchored)
      2. D1 contains 'LLM-as-Judge'           -> B (Judge-Mediated)
      3. D1 = Benchmark and D4 = Automated    -> A (Benchmark-Automation)
      4. otherwise                            -> M (mixed)
    """
    d1 = row["D1"]
    d4 = row["D4"]
    if "Human" in d1:
        return "C"
    if "LLM-as-Judge" in d1:
        return "B"
    if "Benchmark" in d1 and "Automated" in d4:
        return "A"
    return "M"


def random_baseline_silhouette(X: np.ndarray, runs: int = 100) -> float:
    rng = np.random.default_rng(RNG_SEED)
    n = X.shape[0]
    scores: list[float] = []
    for _ in range(runs):
        # Random partition into 3 roughly equal classes
        labels = rng.integers(0, 3, size=n)
        if len(set(labels)) < 2:
            continue
        try:
            scores.append(silhouette_score(X, labels, metric="hamming"))
        except ValueError:
            continue
    return float(np.mean(scores)) if scores else float("nan")


def bootstrap_costability(X: np.ndarray, labels: np.ndarray, n_iter: int = 200) -> dict[str, float]:
    rng = np.random.default_rng(RNG_SEED)
    n = X.shape[0]
    archetypes = {a: np.where(labels == a)[0] for a in ["A", "B", "C"]}
    co_cluster = {a: [] for a in archetypes}
    for _ in range(n_iter):
        idx = rng.choice(n, size=n, replace=True)
        Xb = X[idx]
        lb = labels[idx]
        try:
            km = KMeans(n_clusters=3, n_init=10, random_state=int(rng.integers(1, 10**6))).fit(Xb)
        except Exception:
            continue
        clusters = km.labels_
        for a, members in archetypes.items():
            paired = [i for i, src in enumerate(idx) if src in set(members)]
            if len(paired) < 2:
                continue
            cluster_ids = clusters[paired]
            top = Counter(cluster_ids).most_common(1)[0][1]
            co_cluster[a].append(top / len(paired))
    return {a: float(np.mean(v)) if v else float("nan") for a, v in co_cluster.items()}


def main() -> int:
    rows = load_corpus(CSV_PATH)
    n = len(rows)
    print(f"Loaded n={n} papers from {CSV_PATH}")

    X, _ = one_hot_encode(rows)
    rule_labels = np.array([rule_based_archetype(r) for r in rows])

    counts = Counter(rule_labels)
    print(
        "Rule-based archetype counts: "
        + ", ".join(f"{k}={v} ({v/n:.1%})" for k, v in sorted(counts.items()))
    )

    # Restrict to A/B/C (drop mixed) for the silhouette + ARI checks
    keep = np.isin(rule_labels, ["A", "B", "C"])
    Xk = X[keep]
    yk = rule_labels[keep]
    yk_num = np.array([{"A": 0, "B": 1, "C": 2}[c] for c in yk])
    print(f"Cluster validation set (A/B/C only): n={Xk.shape[0]}")

    # CHECK 1: silhouette of rule-based partition + random baseline
    sil_rule = silhouette_score(Xk, yk_num, metric="hamming")
    sil_random = random_baseline_silhouette(Xk)
    print(f"\nCheck 1: silhouette(rule-based) = {sil_rule:.3f}")
    print(f"         silhouette(random baseline, 100 shuffles) = {sil_random:.3f}")

    # CHECK 2: ARI of unsupervised clusterings vs rule-based labels at k=3
    print("\nCheck 2: ARI of unsupervised k=3 clusterings vs rule-based partition")
    algorithms = {
        "k-means": KMeans(n_clusters=3, n_init=10, random_state=RNG_SEED),
        "Ward": AgglomerativeClustering(n_clusters=3, linkage="ward"),
        "average linkage": AgglomerativeClustering(n_clusters=3, linkage="average"),
        "GMM": GaussianMixture(n_components=3, random_state=RNG_SEED, n_init=5),
        "spectral": SpectralClustering(n_clusters=3, random_state=RNG_SEED, affinity="nearest_neighbors"),
    }
    for name, model in algorithms.items():
        try:
            if isinstance(model, GaussianMixture):
                pred = model.fit_predict(Xk)
            else:
                pred = model.fit_predict(Xk)
            ari = adjusted_rand_score(yk_num, pred)
            sil = silhouette_score(Xk, pred, metric="hamming") if len(set(pred)) > 1 else float("nan")
            print(f"  {name:18s} ARI={ari:.2f}  silhouette={sil:.3f}")
        except Exception as e:
            print(f"  {name:18s} (failed: {e})")

    # CHECK 3: silhouette curve for KMeans at k=2,3,4
    print("\nCheck 3: KMeans silhouette curve (Hamming distance)")
    for k in (2, 3, 4):
        km = KMeans(n_clusters=k, n_init=10, random_state=RNG_SEED).fit(Xk)
        sil_k = silhouette_score(Xk, km.labels_, metric="hamming")
        print(f"  k={k}: silhouette = {sil_k:.3f}")

    # CHECK 4: bootstrap co-cluster stability
    print("\nCheck 4: bootstrap co-cluster stability of rule-based archetypes (200 iters)")
    stab = bootstrap_costability(Xk, yk, n_iter=200)
    for a in ("A", "B", "C"):
        print(f"  Archetype {a}: within-archetype co-cluster probability = {stab[a]:.2f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
