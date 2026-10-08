# Appendix 3: Mathematical Models, Financial Calculations & Sensitivity Analysis

This document provides the formal mathematical formulations, financial spreadsheets, unit economics, and multi-scenario sensitivity analyses supporting the business case for **Client B**.

---

## 1. Operating Baseline & Physical Steel Mix

### 1.1 Volume Breakdown
- **Annual Capacity ($T_{\text{total}}$):** $80,000\text{ tonnes / year}$ ($\approx 6,667\text{ tonnes / month}$).
- **Product Split:**
  - Structural Profiles ($T_{\text{prof}}$): $75\% \times 80,000 = 60,000\text{ tonnes / year}$.
  - Structural Steel Plates ($T_{\text{plate}}$): $25\% \times 80,000 = 20,000\text{ tonnes / year}$.

### 1.2 Baseline Wastage Metrics (from Client Discovery Notes)
- Profile baseline waste ($W_{\text{prof}}$): $6.0\%$ (client reported 5% to 10%).
- Plate baseline waste ($W_{\text{plate}}$): $22.5\%$ (client reported 20% to 25%).
- Total Annual Baseline Waste ($T_{\text{waste}}$):
  $$T_{\text{waste}} = (60,000 \times 0.060) + (20,000 \times 0.225) = 3,600 + 4,500 = 8,100\text{ tonnes / year}$$
- Overall Blended Baseline Waste Percentage:
  $$W_{\text{blended}} = \frac{8,100}{80,000} \times 100\% = 10.125\%$$
  *(Note: This matches the client’s stated baseline of “7 to 10% on average overall”.)*

---

## 2. Waste Decomposition & Avoidability Analysis

Waste is not a homogeneous bucket. To avoid over-promising savings, we decompose reported baseline waste into **unavoidable physical process loss**, **recoverable contract revisions**, and **avoidable nesting/remnant loss**:

### 2.1 Plate Waste Decomposition ($22.5\%$ Baseline $= 4,500\text{ tonnes/yr}$)
1. **Unavoidable Process Kerf & Skeleton ($3.5\%$ / $700\text{ t/yr}$):**
   - Torch width loss (oxyfuel/plasma: 4–6mm kerf): $\sim 1.5\%$.
   - Plate perimeter clamping margin (25–30mm edge clearance): $\sim 1.0\%$.
   - Skeleton structural integrity bridges (preventing cut parts from tipping into downdraft water tables): $\sim 1.0\%$.
2. **Client Revision Scrap ($4.0\%$ / $800\text{ t/yr}$):**
   - Steel cut prior to receipt of late client drawing revisions. Currently absorbed as internal loss due to lack of revision audit trails.
3. **Unrecovered / Abandoned Yard Remnants ($6.0\%$ / $1,200\text{ t/yr}$):**
   - Usable drops ($\ge 1.5\text{m} \times 1.5\text{m}$) logged in Strumis but abandoned in yard stacks due to retrieval friction.
4. **Avoidable Geometric Nesting Inefficiency ($9.0\%$ / $1,800\text{ t/yr}$):**
   - Suboptimal manual packing density, lack of part rotation testing, and failure to co-nest across projects.
- **Total Avoidable / Recoverable Plate Opportunity:** $4.0\% + 6.0\% + 9.0\% = 19.0\%$ ($3,800\text{ tonnes/year}$).

### 2.2 Profile Waste Decomposition ($6.0\%$ Baseline $= 3,600\text{ tonnes/yr}$)
1. **Unavoidable Saw Kerf & Mill Crop ($1.5\%$ / $900\text{ t/yr}$):**
   - Cold band saw kerf (5mm) and mill out-of-square end facing (25mm per 12m stick).
2. **Short Offcut Discards ($3.0\%$ / $1,800\text{ t/yr}$):**
   - Offcuts $<1.8\text{m}$ that cannot be used for primary structural framing.
3. **Avoidable 1D Linear Packing Inefficiency ($1.5\%$ / $900\text{ t/yr}$):**
   - Project-siloed cutting leaving sub-optimal drops.
- **Total Avoidable / Recoverable Profile Opportunity:** $1.5\% + 1.0\% = 2.5\%$ ($1,500\text{ tonnes/year}$).

---

## 3. Financial Unit Economics

- **Prime Steel Purchase Cost ($P_{\text{prime}}$):** $\$950\text{ / tonne}$.
- **Scrap Salvage Sale Recovery ($P_{\text{scrap}}$):** $\$300\text{ / tonne}$.
- **Net Economic Loss per Tonne Scrapped ($\Delta P_{\text{loss}}$):**
  $$\Delta P_{\text{loss}} = P_{\text{prime}} - P_{\text{scrap}} = \$950 - \$300 = \$650\text{ / tonne}$$
- **Current Total Annual Waste Economic Drain:**
  $$\text{Baseline Loss} = 8,100\text{ tonnes} \times \$650\text{ / tonne} = \$5,265,000\text{ / year}$$

---

## 4. Multi-Scenario Sensitivity Analysis

We evaluate three operational performance scenarios:
1. **Conservative Scenario:** Assumes limited cross-project adoption and modest operator pickup (0.50% profile waste reduction, 1.50% plate waste reduction; 150 tonnes client revision recovery).
2. **Base Scenario:** Target pilot expectation (1.00% profile waste reduction, 3.00% plate waste reduction; 350 tonnes client revision recovery).
3. **Upside Scenario:** Full cross-project co-nesting and high remnant recovery (1.50% profile waste reduction, 4.50% plate waste reduction; 550 tonnes client revision recovery).

### 4.1 Detailed Calculation Breakdown

$$\text{Material Saved} = (T_{\text{prof}} \times \Delta W_{\text{prof}}) + (T_{\text{plate}} \times \Delta W_{\text{plate}})$$
$$\text{Direct Steel Savings} = \text{Material Saved} \times \$650\text{/t}$$
$$\text{Revision Recovery} = T_{\text{rev\_recovered}} \times \$950\text{/t}$$
$$\text{Gross Annual Benefit} = \text{Direct Steel Savings} + \text{Revision Recovery}$$

| Parameter | Baseline (Current) | Conservative | Base Case (Target) | Upside Case |
| :--- | :--- | :--- | :--- | :--- |
| **Profile Waste Reduction** | $0.0\%$ | $0.50\%$ ($300\text{ t}$) | **$1.00\%$ ($600\text{ t}$)** | $1.50\%$ ($900\text{ t}$) |
| **Plate Waste Reduction** | $0.0\%$ | $1.50\%$ ($300\text{ t}$) | **$3.00\%$ ($600\text{ t}$)** | $4.50\%$ ($900\text{ t}$) |
| **Total Material Steel Saved** | $0\text{ tonnes}$ | $600\text{ tonnes}$ | **$1,200\text{ tonnes}$** | $1,800\text{ tonnes}$ |
| **Direct Steel Cost Savings** | $\$0$ | $\$390,000$ | **$\$780,000$** | $\$1,170,000$ |
| **Client Revision Scrap Recovered** | $0\text{ tonnes}$ | $150\text{ tonnes}$ | **$350\text{ tonnes}$** | $550\text{ tonnes}$ |
| **Revision Recovery Value (@ \$950/t)**| $\$0$ | $\$142,500$ | **$\$332,500$** | $\$522,500$ |
| **Gross Annual Value Created** | $\$0$ | $\$532,500$ | **$\$1,112,500$** | $\$1,692,500$ |
| **One-Time Implementation Cost** | — | $\$280,000$ | **$\$280,000$** | $\$280,000$ |
| **Annual Recurring SaaS / Support**| — | $\$60,000$ | **$\$60,000$** | $\$60,000$ |
| **Year 1 Total Cost** | — | $\$340,000$ | **$\$340,000$** | $\$340,000$ |
| **Year 1 Net Benefit** | — | $\$192,500$ | **$\$772,500$** | $\$1,352,500$ |
| **Year 1 ROI ($\%$)** | — | **$56.6\%$** | **$227.2\%$** | **$397.8\%$** |
| **Simple Payback Period** | — | **$7.7\text{ months}$** | **$3.7\text{ months}$** | **$2.4\text{ months}$** |
| **3-Year NPV (@ 10% Discount Rate)** | — | **$\$895,308$** | **$\$2,336,548$** | **$\$3,777,787$** |

### 4.2 3-Year Net Present Value (NPV) Formula
$$NPV = -C_{\text{one-time}} + \sum_{t=1}^{3} \frac{\text{Gross Benefit} - C_{\text{recurring}}}{(1 + r)^t}$$
Where $r = 10.0\%$, $C_{\text{one-time}} = \$280,000$, and $C_{\text{recurring}} = \$60,000$.

For the **Base Case**:
$$\text{Net Annual Cash Flow} = \$1,112,500 - \$60,000 = \$1,052,500$$
$$NPV = -280,000 + \frac{1,052,500}{1.10} + \frac{1,052,500}{1.10^2} + \frac{1,052,500}{1.10^3} = -280,000 + 956,818 + 869,835 + 790,759 = \$2,336,412$$

---

## 5. Mathematical Optimization Formulations

### 5.1 1D Cutting Stock Optimization (Profiles / Beams)
We formulate the multi-project profile cutting problem using the classical **Gilmore-Gomory Column Generation / Integer Linear Programming** framework:

- Let $I$ be the set of cut item requirements, where item $i \in I$ has cut length $l_i$, required quantity $d_i$, and kerf allowance $k$.
- Let $J$ be the set of feasible cutting patterns on standard stock length $L = 12,000\text{mm}$.
- A cutting pattern $j \in J$ specifies how many pieces $a_{ij}$ of item $i$ are cut from stock beam $j$, subject to:
  $$\sum_{i \in I} a_{ij} (l_i + k) \le L$$
- Decision variable $x_j \in \mathbb{Z}_{\ge 0}$ represents the number of stock beams cut using pattern $j$.

#### Objective Function:
$$\min \sum_{j \in J} c_j x_j - \sum_{j \in J} \lambda \cdot \mathbb{I}(\text{remnant}_j \ge L_{\text{min\_remnant}})$$
Subject to:
$$\sum_{j \in J} a_{ij} x_j \ge d_i \quad \forall i \in I \quad \text{(Demand satisfaction)}$$
Where $c_j$ is the stock cost, $\lambda$ is a credit incentive for leaving a single reusable remnant $\ge 2,500\text{mm}$, and $x_j$ are non-negative integers.

---

### 5.2 2D Plate Nesting & Remnant-Preserving Optimization
Unlike classical 2D strip packing that minimizes total bounding length, structural steel plate fabrication requires **Remnant-Preserving Nesting**:

- Let $P = \{p_1, p_2, \dots, p_n\}$ be the set of 2D polygonal parts to be nested onto master plate $M$ with dimensions $(W_M, L_M)$ and thickness $T$.
- Each part $p_i$ is placed at position $(x_i, y_i)$ with rotation $\theta_i \in \{0^\circ, 90^\circ, 180^\circ, 270^\circ\}$ (respecting grain orientation constraints).
- Let $NFP(p_i, p_k)$ be the No-Fit Polygon ensuring no geometric overlap between parts:
  $$(x_i - x_k, y_i - y_k) \notin \text{interior}(NFP(p_i, p_k))$$
- Minimum spacing between parts is enforced: $\text{dist}(p_i, p_k) \ge \text{kerf} + \text{thermal\_margin}$.

#### Objective Function:
$$\min \left[ \alpha \cdot \text{Area}(M_{\text{consumed}}) + \beta \cdot \text{EnclosingArea}(P) - \gamma \cdot \text{MaxRectRemnant}(\text{FreeArea}) + \delta \cdot \text{PiercePenalties} \right]$$
Where:
- $\text{EnclosingArea}(P)$ penalizes scattering parts across the plate, forcing parts to cluster tightly against the plate origin $(0,0)$.
- $\text{MaxRectRemnant}(\text{FreeArea})$ rewards the generation of a single, large, contiguous rectangular offcut drop.
- $\alpha, \beta, \gamma, \delta$ are calibrated weighting factors.

---

### 5.3 Remnant Retrieval Economic Decision Model
When part $p$ requires steel of grade $G$ and thickness $T$, the system evaluates all candidate remnants $R = \{r_1, r_2, \dots, r_m\}$ in the yard against pulling a fresh master plate:

$$\text{NetScore}(r) = V_{\text{steel}}(p) - C_{\text{unstack}}(r) - C_{\text{prep}}(r)$$
Where:
- $V_{\text{steel}}(p) = \text{Weight}(p) \times P_{\text{prime}}$ (value of virgin steel preserved).
- $C_{\text{unstack}}(r) = \max(0, \text{StackDepth}(r) - 1) \times C_{\text{crane\_move}}$ (crane cost penalty: $\$35$ per plate moved).
- $C_{\text{prep}}(r)$ is the torch edge squaring / prep penalty for irregular remnants ($\$15$).

**Decision Rule:**
$$\text{Action} = \begin{cases} 
\text{Retrieve Remnant } r^* & \text{if } \max_{r \in R} \text{NetScore}(r) > \text{Threshold } (\$25) \text{ and } \text{StackDepth}(r^*) \le 3 \\
\text{Cut from Virgin Stock} & \text{otherwise}
\end{cases}$$

This mathematical rule prevents the system from generating recommendations that shop-floor crane riggers will refuse to execute due to inaccessible yard stacking.
