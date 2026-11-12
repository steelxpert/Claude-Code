# QA report - EN 1993-1-3 prototype (FLIN-008)

All sections S350GD (fyb = 350 MPa), E = 210 000 MPa, nu = 0.3, internal radius r = 1.5 t (ASSUMED, FLINS tooling unknown).

## Q1  Gross section constants: three independent routes

Route 1 = Annex C line model on the rounded midline (prototype). Route 2 = sharp-corner model with the 5.1(4) delta reduction. Route 3 = sectionproperties 2D finite-element area model of the real rounded outline (independent library). 

| section | quantity | route 1 | route 2 (5.1) | route 3 (FE) | r1/r3 - 1 | r2/r3 - 1 |
|---|---|---|---|---|---|---|
| C150x45x10x1.5 | A [mm2] | 373.2 | 372.2 | 373.3 | -0.01 % | -0.29 % |
| C150x45x10x1.5 | Iy [mm4] | 1.22e+06 | 1.208e+06 | 1.22e+06 | -0.03 % | -1.01 % |
| C150x45x10x1.5 | Iz [mm4] | 8.704e+04 | 8.731e+04 | 8.716e+04 | -0.13 % | +0.18 % |
| C150x45x10x1.5 | It [mm4] | 279.9 | 279.1 | 279.1 | +0.29 % | +0.01 % |
| C150x45x10x1.5 | Iw [mm6] | 3.656e+08 | 3.561e+08 | 3.659e+08 | -0.09 % | -2.67 % |
| C150x45x10x1.5 | ys - yc (shear centre) [mm] | -27.83 | nan | -27.83 | +0.02 % | +nan % |
| C200x60x15x2.0 | A [mm2] | 670.2 | 668.3 | 670.2 | -0.01 % | -0.28 % |
| C200x60x15x2.0 | Iy [mm4] | 3.905e+06 | 3.867e+06 | 3.906e+06 | -0.03 % | -1.01 % |
| C200x60x15x2.0 | Iz [mm4] | 2.88e+05 | 2.884e+05 | 2.883e+05 | -0.13 % | +0.02 % |
| C200x60x15x2.0 | It [mm4] | 893.6 | 891.1 | 890.7 | +0.33 % | +0.05 % |
| C200x60x15x2.0 | Iw [mm6] | 2.187e+09 | 2.127e+09 | 2.189e+09 | -0.08 % | -2.84 % |
| C200x60x15x2.0 | ys - yc (shear centre) [mm] | -38.21 | nan | -38.2 | +0.02 % | +nan % |
| C200x60x15x2.5 | A [mm2] | 828.4 | 825.2 | 828.5 | -0.01 % | -0.39 % |
| C200x60x15x2.5 | Iy [mm4] | 4.776e+06 | 4.714e+06 | 4.778e+06 | -0.04 % | -1.33 % |
| C200x60x15x2.5 | Iz [mm4] | 3.451e+05 | 3.458e+05 | 3.458e+05 | -0.20 % | +0.02 % |
| C200x60x15x2.5 | It [mm4] | 1726 | 1719 | 1719 | +0.42 % | +0.03 % |
| C200x60x15x2.5 | Iw [mm6] | 2.596e+09 | 2.506e+09 | 2.6e+09 | -0.13 % | -3.60 % |
| C200x60x15x2.5 | ys - yc (shear centre) [mm] | -37.54 | nan | -37.53 | +0.03 % | +nan % |
| U150x45x1.5 | A [mm2] | 349.4 | 348.9 | 349.4 | -0.00 % | -0.13 % |
| U150x45x1.5 | Iy [mm4] | 1.107e+06 | 1.102e+06 | 1.107e+06 | -0.02 % | -0.44 % |
| U150x45x1.5 | Iz [mm4] | 5.922e+04 | 5.84e+04 | 5.927e+04 | -0.09 % | -1.47 % |
| U150x45x1.5 | It [mm4] | 262 | 261.7 | 261.1 | +0.34 % | +0.22 % |
| U150x45x1.5 | Iw [mm6] | 2.317e+08 | 2.273e+08 | 2.319e+08 | -0.09 % | -2.00 % |
| U150x45x1.5 | ys - yc (shear centre) [mm] | -22.24 | nan | -22.23 | +0.05 % | +nan % |
| U150x40x2.0 | A [mm2] | 441.1 | 440.3 | 441.1 | -0.01 % | -0.20 % |
| U150x40x2.0 | Iy [mm4] | 1.334e+06 | 1.327e+06 | 1.335e+06 | -0.03 % | -0.59 % |
| U150x40x2.0 | Iz [mm4] | 5.42e+04 | 5.312e+04 | 5.431e+04 | -0.21 % | -2.20 % |
| U150x40x2.0 | It [mm4] | 588.1 | 587 | 585 | +0.53 % | +0.34 % |
| U150x40x2.0 | Iw [mm6] | 2.115e+08 | 2.059e+08 | 2.118e+08 | -0.18 % | -2.79 % |
| U150x40x2.0 | ys - yc (shear centre) [mm] | -18.37 | nan | -18.35 | +0.09 % | +nan % |

Q1 verdict: route 1 (prototype) vs independent FE area model within 2 % on all A, I, It, Iw: **PASS**. Route 2 (the 5.1(4) approximation) is shown for information; it is what a hand calculation would use.

## Q2  Elastic critical stresses: EN 1993-1-3 closed forms vs finite strip (CUFSM)

Finite strip (pycufsm, signature curve, S-S) on the rounded midline. Local minimum compared with the EN 1993-1-5 plate formula for the governing element (web, kσ = 4, uniform compression); distortional minimum compared with σcr,s of (5.15). EN 1993-1-3 5.5.3.1(8) explicitly allows σcr,s from such a numerical analysis, so a mismatch is a finding, not a failure.

| section | case | CUFSM local min: L_cr / σcr,l | EN plate σcr (web, kσ) | ratio | CUFSM dist. min: L_cr / σcr,d | σcr,s (5.15) | ratio |
|---|---|---|---|---|---|---|
| C150x45x10x1.5 | compression | 120 mm / 111 MPa | 82 MPa (kσ=4.00) | 1.35 | 300 mm / 147 MPa (no distinct minimum; curve value in 2h..8h) | 242 MPa | 0.61 |
| C150x45x10x1.5 | bending y-y | 88 mm / 586 MPa | 422 MPa (kσ=21.80) | 1.39 | 300 mm / 421 MPa | 287 MPa | 1.47 |
| C200x60x15x2.0 | compression | 150 mm / 111 MPa | 82 MPa (kσ=4.00) | 1.35 | 408 mm / 159 MPa (no distinct minimum; curve value in 2h..8h) | 285 MPa | 0.56 |
| C200x60x15x2.0 | bending y-y | 111 mm / 589 MPa | 430 MPa (kσ=22.20) | 1.37 | 441 mm / 459 MPa | 338 MPa | 1.36 |
| C200x60x15x2.5 | compression | 150 mm / 174 MPa | 131 MPa (kσ=4.00) | 1.33 | 408 mm / 216 MPa (no distinct minimum; curve value in 2h..8h) | 348 MPa | 0.62 |
| C200x60x15x2.5 | bending y-y | 120 mm / 918 MPa | 690 MPa (kσ=22.70) | 1.33 | 378 mm / 607 MPa | 414 MPa | 1.47 |
| U150x45x1.5 | compression | 150 mm / 85 MPa | 82 MPa (kσ=4.00) | 1.03 | 300 mm / 115 MPa (no distinct minimum; curve value in 2h..8h) | nan MPa | nan |
| U150x45x1.5 | bending y-y | 111 mm / 194 MPa | 107 MPa (kσ=18.99) | 1.81 | 300 mm / 364 MPa (no distinct minimum; curve value in 2h..8h) | nan MPa | nan |

Reading: ratio > 1 means the closed form is conservative against the finite strip. For the plain U in compression the second minimum is the flange-tip (outstand) mode, not a stiffener mode - no σcr,s exists.

## Q3  Hand checks of the formula layer

| check | prototype | expected | ok |
|---|---|---|---|
| χ(λ=1.0, curve b) | 0.5970 | 0.5970 | PASS |
| χ(λ=0.2, curve b) | 1.0000 | 1.0000 | PASS |
| χ(λ=1.5, curve c) | 0.3145 | 0.3145 | PASS |
| ρ internal, λp=1.0, ψ=1 (1-5 4.2) | 0.7800 | 0.7800 | PASS |
| ρ outstand, λp=1.0 (1-5 4.3) | 0.8120 | 0.8120 | PASS |
| kσ internal ψ=-1 (Table 4.1) | 23.9000 | 23.9000 | PASS |
| kσ internal ψ=-0.5 (Table 4.1) | 13.4000 | 13.4000 | PASS |
| χd(λd=1.0) (5.12b) | 0.7470 | 0.7470 | PASS |
| χd(λd=2.0) (5.12c) | 0.3300 | 0.3300 | PASS |
| σcr plate web C150 kσ=4 = 4·190000·(t/bp)² | 82.0848 | 82.0848 | PASS |

Q3 verdict: **PASS**

## Q4  Internal consistency and limit behaviour

| check | ok | detail |
|---|---|---|
| stocky C150x45x20x4: Aeff/Ag >= 0.95 (web rho = 0.962, flanges and lip fully effective) | PASS | Aeff/Ag = 0.998 |
| very stocky C150x45x20x6: Aeff = Ag | PASS | Aeff/Ag = 1.0000 |
| physical floor: Aeff(C150x45x10x1.5) >= Aeff(U150x45x1.5) (a lip cannot weaken the flange) | PASS | 217.4 >= 169.2 |
| stub lip C150x45x10x3 vs U150x45x3: lipped not weaker than plain (FINDING if FAIL: 5.5.3.2 has no floor) | PASS | 605 vs 595 mm2 |
| C150x45x10x1.5: Aeff <= Ag | PASS | 217.4 <= 373.2 |
| C150x45x10x1.5: Weff <= Wel | PASS | 14513 <= 16268 |
| C150x45x10x1.5: Aeff from line_props = sum(piece length x t) | PASS | 217.37 = 217.37; eN = -1.62 mm (+ toward the web) |
| C150x45x10x1.5: stiffener iteration converged, χd,n <= χd,n-1 | PASS | n = 2, χd = 0.600, λd = 1.204, σcr,s = 242 MPa |
| C200x60x15x2.0: Aeff <= Ag | PASS | 401.7 <= 670.2 |
| C200x60x15x2.0: Weff <= Wel | PASS | 35654 <= 39052 |
| C200x60x15x2.0: Aeff from line_props = sum(piece length x t) | PASS | 401.74 = 401.74; eN = -3.03 mm (+ toward the web) |
| C200x60x15x2.0: stiffener iteration converged, χd,n <= χd,n-1 | PASS | n = 2, χd = 0.668, λd = 1.109, σcr,s = 285 MPa |
| C200x60x15x2.5: Aeff <= Ag | PASS | 560.0 <= 828.4 |
| C200x60x15x2.5: Weff <= Wel | PASS | 44836 <= 47758 |
| C200x60x15x2.5: Aeff from line_props = sum(piece length x t) | PASS | 560.03 = 560.03; eN = -2.37 mm (+ toward the web) |
| C200x60x15x2.5: stiffener iteration converged, χd,n <= χd,n-1 | PASS | n = 2, χd = 0.745, λd = 1.003, σcr,s = 348 MPa |
| U150x45x1.5: Aeff <= Ag | PASS | 169.2 <= 349.4 |
| U150x45x1.5: Weff <= Wel | PASS | 10814 <= 14761 |
| U150x45x1.5: Aeff from line_props = sum(piece length x t) | PASS | 169.21 = 169.21; eN = +3.22 mm (+ toward the web) |
| U150x40x2.0: Aeff <= Ag | PASS | 286.6 <= 441.1 |
| U150x40x2.0: Weff <= Wel | PASS | 15879 <= 17789 |
| U150x40x2.0: Aeff from line_props = sum(piece length x t) | PASS | 286.64 = 286.64; eN = +0.45 mm (+ toward the web) |
| Nc,Rd increases with t (1.5 -> 2.0 mm) | PASS | 76.1 -> 117.2 kN |
| Nb,Rd decreases with Ly (bridging fixed at 0.92 m) | PASS | 63.4 > 61.6 > 56.2 kN |

Q4 verdict: **PASS**

## Q5  Plausibility band: EN 1993-1-3 effective width method vs AISI S100 Direct Strength Method

Same elastic inputs (CUFSM Pcrl, Pcrd; Ncr,TF from the prototype), different design method. Wall stud case: C150x45x10x1.5, Ly = 2.75 m (floor to roof), Lz = LT = 0.92 m (bridging rows), pinned, no sheathing. A DSM nominal within about ±20 % of the EN design value (γM1 = 1.0) is the expected band for lipped channels.

| section | Ly/Lz [m] | EN Nb,Rd [kN] (mode, λ, χ) | DSM Pne / Pnl / Pnd / Pn [kN] | Pn / Nb,Rd |
|---|---|---|---|---|
| C150x45x10x1.5 | 2.75 / 0.92 | 61.6 (torsional-flexural, λ=0.65, χ=0.81) | 96.1 / 61.2 / 66.1* / 61.2 | 0.99 |
| C150x45x10x1.5 | 2.75 / 1.38 | 49.8 (torsional-flexural, λ=0.91, χ=0.66) | 72.1 / 50.8 / 66.1* / 50.8 | 1.02 |
| C200x60x15x2.0 | 2.90 / 2.90 | 53.2 (flexural z, λ=1.41, χ=0.38) | 62.2 / 56.1 / 123.4* / 56.1 | 1.05 |
| C200x60x15x2.5 | 2.60 / 2.60 | 78.1 (flexural z, λ=1.36, χ=0.40) | 92.8 / 90.8 / 176.4* / 90.8 | 1.16 |

\* Pcrd taken from the signature-curve value in the 2h..8h range because no distinct distortional minimum exists for these narrow-flange sections.

## Q6  First numbers for the house members (PRELIMINARY, D-007) - for orientation only

| section | Nc,Rd | Mc,Rd,y | Vb,Rd | Rw,Rd end (ss=45) | Rw,Rd interior (ss=45) | Mb,Rd (L=0.92) | Mb,Rd (L=3.0, C1=1.13) | Nb,Rd (Ly 2.75 / Lz 0.92) |
|---|---|---|---|---|---|---|---|
| C150x45x10x1.5 | 76.1 kN | 5.08 kNm | 26.8 kN | 5.76 kN | 10.36 kN | 4.25 kNm | 1.34 kNm | 61.6 kN |
| C200x60x15x2.0 | 140.6 kN | 12.48 kNm | 47.6 kN | 9.65 kN | 17.61 kN | 11.31 kNm | 5.11 kNm | 124.7 kN |
| C200x60x15x2.5 | 196.0 kN | 15.69 kNm | 74.3 kN | 15.18 kN | 27.62 kN | 14.15 kNm | 6.35 kNm | 170.9 kN |
| U150x45x1.5 | 59.2 kN | 3.78 kNm | 26.8 kN | 4.03 kN | 10.36 kN | 3.09 kNm | 0.93 kNm | 47.9 kN |
| U150x40x2.0 | 100.3 kN | 5.56 kNm | 47.6 kN | 7.00 kN | 18.31 kN | 4.02 kNm | 1.05 kNm | 68.3 kN |

Limits of applicability (5.2 Table 5.1, 5.2a, 5.1(3), 6.14):

- C150x45x10x1.5: NOT satisfied: corners negligible for resistance (r<=5t and r<=0.10 bp) [5.1(3)] (value 2.25, limit 0.7128679656440359)
- C200x60x15x2.0: NOT satisfied: corners negligible for resistance (r<=5t and r<=0.10 bp) [5.1(3)] (value 3, limit 1.117157287525381)
- C200x60x15x2.5: NOT satisfied: corners negligible for resistance (r<=5t and r<=0.10 bp) [5.1(3)] (value 3.75, limit 1.0214466094067263)
- U150x45x1.5: all satisfied
- U150x40x2.0: all satisfied


Overall mechanical QA: Q1 PASS, Q3 PASS, Q4 PASS; Q2 and Q5 are comparisons against other methods and are read in the assessment memo.
