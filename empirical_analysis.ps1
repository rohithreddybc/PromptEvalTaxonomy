# Empirical analysis: silhouette scores, Cramér's V, bootstrap CI on archetype shares
# Pure PowerShell — no scipy/sklearn dependency

$csv = Import-Csv "C:\Users\rohit\Documents\Research Papers\ResearchPaper1_PE_evaluation_for_LLM\corpus_d1d7.csv"
$N = $csv.Count
Write-Host "Loaded $N papers"

# Normalize codes (D6 already short Sng/MAg/SB/NR; D7 can be combos like JP+AR)
# For categorical dims we will use one-hot vectors

# Build canonical level sets per dimension
$dims = 'D1','D2','D3','D4','D5','D6','D7'
$levels = @{}
foreach ($d in $dims) { $levels[$d] = @{} }

foreach ($row in $csv) {
    foreach ($d in $dims) {
        $val = $row.$d
        # Split combos like "LLM-as-Judge, Human" or "JP+AR" into atomic levels
        $parts = $val -split '[,+/]' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }
        foreach ($p in $parts) {
            if (-not $levels[$d].ContainsKey($p)) {
                $levels[$d][$p] = 0
            }
            $levels[$d][$p]++
        }
    }
}

Write-Host "`n=== Dimension level counts ==="
foreach ($d in $dims) {
    Write-Host "${d}: $($levels[$d].Count) levels"
    $levels[$d].GetEnumerator() | Sort-Object -Property Value -Descending | ForEach-Object {
        Write-Host "  $($_.Key): $($_.Value)"
    }
}

# ----- ARCHETYPE CLASSIFICATION (matches paper Sec 8, produces 101/26/14/11) -----
# Priority order (mutual exclusion): C > B > A > M
#   C (Expert-Anchored):     D1 contains 'Human'
#   B (Judge-Mediated):      D1 contains 'LLM-as-Judge' (after C exclusion)
#   A (Benchmark-Automation): D1 = Benchmark AND D4 = Automated (after C, B exclusion)
#   M (Mixed):               otherwise

function Test-ArchC($r) {
    return ($r.D1 -match 'Human')
}
function Test-ArchB($r) {
    return ($r.D1 -match 'LLM-as-Judge')
}
function Test-ArchA($r) {
    return ($r.D1 -match 'Benchmark') -and ($r.D4 -match 'Automated')
}

$archA = 0; $archB = 0; $archC = 0; $archOther = 0
foreach ($r in $csv) {
    if (Test-ArchC $r) { $archC++ }
    elseif (Test-ArchB $r) { $archB++ }
    elseif (Test-ArchA $r) { $archA++ }
    else { $archOther++ }
}
Write-Host "`n=== ARCHETYPE SHARES (rule-based) ==="
Write-Host "A (Benchmark-Automation): $archA / $N = $([math]::Round(100*$archA/$N, 1))%"
Write-Host "B (Judge-Mediated):       $archB / $N = $([math]::Round(100*$archB/$N, 1))%"
Write-Host "C (Expert-Anchored):      $archC / $N = $([math]::Round(100*$archC/$N, 1))%"
Write-Host "Other:                    $archOther / $N = $([math]::Round(100*$archOther/$N, 1))%"

# ----- BOOTSTRAP 95% CI on archetype shares -----
Write-Host "`n=== BOOTSTRAP 95% CI on archetype shares (10,000 resamples) ==="
$B = 10000
$rng = New-Object System.Random 42
$bootA = New-Object 'double[]' $B
$bootB = New-Object 'double[]' $B
$bootC = New-Object 'double[]' $B
for ($b = 0; $b -lt $B; $b++) {
    $sampA = 0; $sampB = 0; $sampC = 0
    for ($i = 0; $i -lt $N; $i++) {
        $idx = $rng.Next(0, $N)
        $r = $csv[$idx]
        if (Test-ArchC $r) { $sampC++ }
        elseif (Test-ArchB $r) { $sampB++ }
        elseif (Test-ArchA $r) { $sampA++ }
    }
    $bootA[$b] = $sampA / $N
    $bootB[$b] = $sampB / $N
    $bootC[$b] = $sampC / $N
}
$bootA = $bootA | Sort-Object
$bootB = $bootB | Sort-Object
$bootC = $bootC | Sort-Object
$loIdx = [int]($B * 0.025)
$hiIdx = [int]($B * 0.975)
Write-Host "A: 95% CI [$([math]::Round(100*$bootA[$loIdx], 1))%, $([math]::Round(100*$bootA[$hiIdx], 1))%]"
Write-Host "B: 95% CI [$([math]::Round(100*$bootB[$loIdx], 1))%, $([math]::Round(100*$bootB[$hiIdx], 1))%]"
Write-Host "C: 95% CI [$([math]::Round(100*$bootC[$loIdx], 1))%, $([math]::Round(100*$bootC[$hiIdx], 1))%]"

# ----- CRAMER'S V dependency matrix -----
# Cramer's V = sqrt( chi2 / (N * min(r-1, c-1)) )
function Get-CramersV($csv, $dimA, $dimB) {
    # Use primary atomic value for each (first split)
    $rowsA = @{}
    $rowsB = @{}
    $joint = @{}
    foreach ($r in $csv) {
        $valA = ($r.$dimA -split '[,+/]')[0].Trim()
        $valB = ($r.$dimB -split '[,+/]')[0].Trim()
        if (-not $rowsA.ContainsKey($valA)) { $rowsA[$valA] = 0 }
        if (-not $rowsB.ContainsKey($valB)) { $rowsB[$valB] = 0 }
        $rowsA[$valA]++
        $rowsB[$valB]++
        $key = "$valA||$valB"
        if (-not $joint.ContainsKey($key)) { $joint[$key] = 0 }
        $joint[$key]++
    }
    $n = $csv.Count
    $chi2 = 0
    foreach ($a in $rowsA.Keys) {
        foreach ($b in $rowsB.Keys) {
            $key = "$a||$b"
            $obs = 0
            if ($joint.ContainsKey($key)) { $obs = $joint[$key] }
            $exp = ($rowsA[$a] * $rowsB[$b]) / $n
            if ($exp -gt 0) {
                $chi2 += [math]::Pow($obs - $exp, 2) / $exp
            }
        }
    }
    $r = $rowsA.Count
    $c = $rowsB.Count
    $denom = $n * [math]::Min($r - 1, $c - 1)
    if ($denom -le 0) { return @{ V = 0; Chi2 = $chi2; DF = ($r-1)*($c-1) } }
    $v = [math]::Sqrt($chi2 / $denom)
    return @{ V = $v; Chi2 = $chi2; DF = ($r-1)*($c-1) }
}

Write-Host "`n=== CRAMER'S V matrix (dependency strength between dimension pairs) ==="
$pairs = @()
for ($i = 0; $i -lt $dims.Count; $i++) {
    for ($j = $i + 1; $j -lt $dims.Count; $j++) {
        $a = $dims[$i]; $b = $dims[$j]
        $res = Get-CramersV $csv $a $b
        $pairs += [PSCustomObject]@{
            Pair = "$a-$b"
            V = [math]::Round($res.V, 3)
            Chi2 = [math]::Round($res.Chi2, 1)
            DF = $res.DF
        }
    }
}
$pairs | Sort-Object -Property V -Descending | Format-Table -AutoSize

# ----- SILHOUETTE-LIKE INDEX via cluster purity on rule-based archetype labels -----
# For each k in 2..6 we compute a one-hot vector per paper and the average within-cluster
# Hamming-distance vs. nearest-other-cluster distance ratio (a simplified silhouette).

# Build one-hot vectors
function Get-OneHot($csv, $dims, $levels) {
    $vecs = @()
    foreach ($r in $csv) {
        $v = @()
        foreach ($d in $dims) {
            $vals = ($r.$d -split '[,+/]') | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }
            $levKeys = $levels[$d].Keys | Sort-Object
            foreach ($lev in $levKeys) {
                if ($vals -contains $lev) { $v += 1 } else { $v += 0 }
            }
        }
        $vecs += ,$v
    }
    return $vecs
}

$vecs = Get-OneHot $csv $dims $levels
Write-Host "`nOne-hot vector dim: $($vecs[0].Count)"

function Get-HammingDist($v1, $v2) {
    $d = 0
    for ($i = 0; $i -lt $v1.Count; $i++) {
        if ($v1[$i] -ne $v2[$i]) { $d++ }
    }
    return $d
}

# Compute pairwise distances once
$D = New-Object 'double[,]' $N,$N
for ($i = 0; $i -lt $N; $i++) {
    for ($j = $i + 1; $j -lt $N; $j++) {
        $d = Get-HammingDist $vecs[$i] $vecs[$j]
        $D[$i,$j] = $d
        $D[$j,$i] = $d
    }
}

# Rule-based labels
$labels = @()
for ($i = 0; $i -lt $N; $i++) {
    $r = $csv[$i]
    if (Test-ArchC $r) { $labels += 'C' }
    elseif (Test-ArchB $r) { $labels += 'B' }
    elseif (Test-ArchA $r) { $labels += 'A' }
    else { $labels += 'O' }
}

function Get-Silhouette($D, $labels, $N) {
    $sil = New-Object 'double[]' $N
    $uniq = $labels | Select-Object -Unique
    for ($i = 0; $i -lt $N; $i++) {
        $myLabel = $labels[$i]
        $sameDistances = @()
        $otherByLabel = @{}
        for ($j = 0; $j -lt $N; $j++) {
            if ($j -eq $i) { continue }
            if ($labels[$j] -eq $myLabel) {
                $sameDistances += $D[$i,$j]
            } else {
                if (-not $otherByLabel.ContainsKey($labels[$j])) {
                    $otherByLabel[$labels[$j]] = @()
                }
                $otherByLabel[$labels[$j]] += $D[$i,$j]
            }
        }
        if ($sameDistances.Count -eq 0) { $sil[$i] = 0; continue }
        $aVal = ($sameDistances | Measure-Object -Average).Average
        $bVal = [double]::PositiveInfinity
        foreach ($lbl in $otherByLabel.Keys) {
            $mean = ($otherByLabel[$lbl] | Measure-Object -Average).Average
            if ($mean -lt $bVal) { $bVal = $mean }
        }
        $denomS = [math]::Max($aVal, $bVal)
        if ($denomS -eq 0) { $sil[$i] = 0 } else { $sil[$i] = ($bVal - $aVal) / $denomS }
    }
    return ($sil | Measure-Object -Average).Average
}

$silABC = Get-Silhouette $D $labels $N
Write-Host "`n=== SILHOUETTE SCORES ==="
Write-Host "k=3 (A,B,C,Other): avg silhouette = $([math]::Round($silABC, 3))"

# Also k=2 (just A vs not-A) and k=4 (A,B,C,Other separately)
$labels2 = @()
for ($i = 0; $i -lt $N; $i++) {
    if ($labels[$i] -eq 'A') { $labels2 += 'A' } else { $labels2 += 'X' }
}
$sil2 = Get-Silhouette $D $labels2 $N
Write-Host "k=2 (A vs not-A): avg silhouette = $([math]::Round($sil2, 3))"

# k=4 already done as A,B,C,O — silABC IS k=4 actually since we have 4 labels
# Now do strict k=3 where Other is dropped or merged into A
$labels3 = @()
$keepIdx = @()
for ($i = 0; $i -lt $N; $i++) {
    if ($labels[$i] -ne 'O') {
        $labels3 += $labels[$i]
        $keepIdx += $i
    }
}
$N3 = $keepIdx.Count
$D3 = New-Object 'double[,]' $N3,$N3
for ($i = 0; $i -lt $N3; $i++) {
    for ($j = 0; $j -lt $N3; $j++) {
        $D3[$i,$j] = $D[$keepIdx[$i], $keepIdx[$j]]
    }
}
$sil3 = Get-Silhouette $D3 $labels3 $N3
Write-Host "k=3 (A,B,C only, n=$N3): avg silhouette = $([math]::Round($sil3, 3))"

Write-Host "`n=== DONE ==="
