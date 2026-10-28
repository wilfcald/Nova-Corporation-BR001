
# BR001 | Analytical Plan

## 1. Document Control

| Field | Value |
|---|---|
| Project | BR001 — Executive Performance Review |
| Document | Analytical Plan & KPI Contract |
| Document ID | AP-BR001 |
| Organization | Nova Corporation |
| Prepared By | Data Analyst |
| Status | Draft — Pending Review |
| Primary Reference | IRDS-BR001 |
| Supporting References | Approved Business Clarifications |
| Scope | H1 2025 vs H1 2026 |

## 2. Business Objective & Scope

### 2.1 Business Context

Nova Corporation is a fictional regional omnichannel retailer operating across Costa Rica, Panama, Guatemala, and the Dominican Republic.

Management has observed revenue growth with weaker-than-expected gross profit growth and requires an evidence-based performance review.

### 2.2 Business Objective

Determine whether revenue growth is profitable and sustainable, identify the principal performance drivers, quantify material risks and opportunities, and recommend prioritized management actions.

### 2.3 In Scope

- H1 2025 vs H1 2026 performance comparison.
- Sales-line transactions and approved business dimensions.
- Revenue, discounts, direct costs, and gross profit.
- Descriptive and diagnostic business analysis.
- Executive findings and actionable recommendations.

### 2.4 Out of Scope

- Forecasting and predictive modeling.
- Inventory optimization.
- Marketing attribution.
- HR and workforce analytics.
- Production data-engineering changes.
- Unapproved external data or metrics.

### 2.5 Governing References

- IRDS-BR001 — Primary operational baseline.
- Approved Business Clarifications — Specific approved exceptions and decisions.
- Controlled analytical dataset — Validated analytical data source.

## 3. Requirements Traceability

### 3.1 Business Requirements Traceability Matrix

| Business Question | Analytical Requirements | KPIs | Dimensions | Planned Analysis | Validation |
|---|---|---|---|---|---|

| BQ01 — Profitability Growth | AR01, AR03, AR04, AR06, AR08, AR09 | Net Revenue; Gross Profit; Gross Margin % | Year; Month | Compare H1 2025 vs H1 2026 revenue, gross profit, and gross margin. Examine profitability drivers and distinguish supported findings from hypotheses. | Reconcile KPI totals to the controlled analytical dataset; disclose data-quality limitations. |

| BQ02 — Sales Channel Performance | AR01, AR02, AR03, AR05, AR06, AR08 | Net Revenue; Gross Profit; Gross Margin % | Year; Month; Channel | Compare channel performance, year-over-year growth, profitability, and contribution to company results. Identify strongest and weakest channels. | Validate channel classifications, KPI calculations, and reconciliation to company totals. |

| BQ03 — Product & Category Performance | AR01, AR02, AR03, AR05, AR06, AR08 | Net Revenue; Gross Profit; Gross Margin %; Units Sold | Year; Category; Product | Evaluate revenue and gross profit contributions by category and product. Identify top and bottom contributors and changes in product mix. | Validate product relationships, ranking criteria, and KPI reconciliation to company totals. |

| BQ04 — Customer Segment Performance | AR01, AR02, AR03, AR05, AR06, AR08 | Net Revenue; Gross Profit; Gross Margin % | Year; Customer Segment | Compare customer segment contributions, growth, and profitability. Identify high-value and underperforming segments. | Validate segment attribution, retain approved unknown-customer classifications, and reconcile totals. |

| BQ05 — Regional Performance | AR01, AR02, AR03, AR05, AR06, AR08 | Net Revenue; Gross Profit; Gross Margin % | Year; Country; Region | Compare geographic performance, growth, profitability, and contribution. Identify regions requiring management attention. | Validate geographic relationships, regional classifications, and reconciliation to company totals. |

| BQ06 — Discount Impact | AR01, AR02, AR04, AR06, AR08, AR09 | Gross Revenue; Discount Amount; Discount Rate; Net Revenue; Gross Profit; Gross Margin % | Year; Month; Channel; Category | Examine discount patterns and their association with revenue and profitability. Identify areas of elevated discount exposure without assuming causation. | Validate discount calculations, financial relationships, and KPI reconciliation; disclose analytical limitations. |

| BQ07 — Management Recommendations | AR03, AR05, AR06, AR07, AR08, AR09 | Relevant approved KPIs from BQ01–BQ06 | Company; Channel; Category; Customer Segment; Region | Consolidate findings, prioritize material risks and opportunities, and propose evidence-based management actions. | Trace every recommendation to validated findings, approved KPI definitions, and documented limitations. |

## 4. KPI Contract

### 4.1 KPI Governance

All analytical KPIs must follow the definitions, eligibility rules, and approved clarifications established in IRDS-BR001.

Financial KPIs must be calculated from the controlled analytical dataset using the approved analytical population.

Ratios must be calculated from aggregated numerators and denominators, not by averaging row-level percentages.

All reported KPIs must be reconcilable to validated source totals.

### 4.2 Approved KPI Definitions

| KPI | Business Definition | Calculation |
|---|---|---|
| Gross Revenue | Revenue before discounts | SUM(gross_revenue) |
| Discount Amount | Total discounts applied | SUM(discount_amount) |
| Net Revenue | Revenue after discounts | SUM(net_revenue) |
| Total Cost | Direct cost of sales | SUM(total_cost) |
| Gross Profit | Revenue remaining after direct costs | SUM(gross_profit) |
| Gross Margin % | Gross profit relative to net revenue | Gross Profit / Net Revenue |
| Units Sold | Total eligible units sold | SUM(quantity) |
| Discount Rate | Discounts relative to gross revenue | Discount Amount / Gross Revenue |

### 4.3 Restricted KPIs

| KPI | Status | Restriction |
|---|---|---|
| Order Count | BLOCKED | Source order identity conflicts prevent reliable distinct-order calculations. |
| Average Order Value | BLOCKED | Depends on Order Count, which is currently blocked. |

### 4.4 Calculation Controls

- Apply the approved reporting population and transaction-status rules.
- Use certified records for official financial reporting.
- Handle zero denominators explicitly.
- Preserve approved unknown dimension classifications.
- Do not calculate blocked KPIs.
- Document exceptions and analytical limitations.
- Reconcile results against approved control totals.


### 4.5 Certified Analytical Population

**Source Dataset:** br001_clean_analytical_dataset.csv

**Dataset Grain:** One sales line per customer order.

**Total Records:** 23,530

**Certified Records:** 21,342

**Excluded Records:** 2,188

**Eligibility Field:** certified_sales_eligible

**Official Reporting Filter:** certified_sales_eligible = True

All official financial KPIs must be calculated using the certified analytical population.

The provisional return-inclusive population must not be combined with the certified population or presented as an additional, additive reporting population.

Order Count and Average Order Value remain blocked because no records qualify for order-level KPI reporting.


#### Eligibility Rules

**Certified Reporting Population**

certified_sales_eligible =
(order_status == "Completed") AND
(invalid_numeric_flag == False)

**Provisional Return-Inclusive Population**

provisional_return_inclusive_eligible =
(order_status IN ["Completed", "Partially Returned"]) AND
(invalid_numeric_flag == False)

**Excluded Transaction Statuses**

- Pending
- Cancelled

**Numeric Validity Requirements**

- quantity > 0
- unit_price > 0
- unit_cost >= 0
- discount_pct between 0 and 1, inclusive
- Required numeric fields must not be null or non-numeric.

**Reporting Restrictions**

- The certified and provisional populations must be reported separately.
- Provisional results must not be presented as certified financial performance.
- Ratios must use consistent numerator and denominator populations.
- Source exceptions must remain traceable.
- Additional eligibility restrictions require an approved business rule.

### 4.6 Financial Reconciliation Baseline

The following control totals were verified against the certified analytical population.

**Source:** br001_clean_analytical_dataset.csv

**Eligibility Filter:** certified_sales_eligible = True

**Certified Records:** 21,342

| KPI | Certified Control Total |
|---|---:|
| Gross Revenue | 16,068,562.07 |
| Discount Amount | 2,504,281.22 |
| Net Revenue | 13,564,280.85 |
| Total Cost | 9,483,638.54 |
| Gross Profit | 4,080,642.31 |

**Financial Integrity Checks:**

- Gross Revenue - Discount Amount = Net Revenue
- Net Revenue - Total Cost = Gross Profit

**Reconciliation Requirements:**

- Recalculate all control totals independently in Python.
- Apply the certified population filter consistently.
- Compare calculated values against the documented baseline.
- Investigate and document any discrepancies.
- Do not begin business interpretation until reconciliation passes.


### 4.7 Approved Clarification Controls

| Clarification | Analytical Rule | Source Issue Status |
|---|---|---|
| CL-001 | Block certified order-level KPIs until an authoritative order mapping is validated. | OPEN |
| CL-002 | Use valid Completed sales for certified reporting. Keep partial returns in a separate provisional view. | Return verification OPEN |
| CL-003 | Preserve unrecognized payment methods as Unmapped without automatic financial exclusion. | OPEN |
| CL-004 | Preserve duplicate source line IDs and use a stable analytical row key. | OPEN |
| CL-005 | Exclude invalid numeric records from certified KPIs while retaining source evidence. | OPEN |
| CL-006 | Preserve missing customer and channel references using explicit Unknown attribution. | OPEN |
| CL-007 | Retain eligible high-cost and negative-margin transactions without automatic exclusion. | Commercial explanation pending |

**Governing Document:** BR001 — Business Clarification Response & Approved Cleaning Decisions.

**Implementation Principle:** Approved reporting treatments do not constitute source-data corrections.

**Validation Requirement:** Confirm that each approved clarification is correctly implemented in the controlled analytical dataset before releasing executive KPIs.


## 5. Analytical Methodology

### 5.1 Analytical Approach

The analysis will follow a structured, evidence-based workflow using the controlled analytical dataset and approved business requirements.

The primary approach will be descriptive and diagnostic analysis, with prescriptive recommendations supported by validated findings.

### 5.2 Execution Workflow

1. **Data Loading:** Load the controlled analytical dataset into Python.
2. **Population Validation:** Verify reporting periods, record eligibility, and approved classifications.
3. **KPI Calculation:** Calculate approved KPIs using the documented KPI Contract.
4. **Baseline Reconciliation:** Compare financial totals and record counts against approved control totals.
5. **Descriptive Analysis:** Evaluate performance trends, contributions, growth, and rankings.
6. **Diagnostic Analysis:** Investigate profitability differences, performance drivers, and discount patterns.
7. **Cross-Dimensional Analysis:** Compare findings across channels, products, customer segments, and regions.
8. **Findings Validation:** Verify material findings, assess limitations, and avoid unsupported causal claims.
9. **Management Recommendations:** Prioritize actions based on business impact and supporting evidence.
10. **Reporting:** Prepare executive findings and Power BI reporting outputs.

### 5.3 Analytical Techniques

- Year-over-year comparison.
- Absolute and percentage variance analysis.
- Revenue and gross profit contribution analysis.
- Gross margin and discount rate analysis.
- Top and bottom contributor rankings.
- Product and channel mix analysis.
- Segmentation and geographic comparisons.
- Diagnostic drill-down and hypothesis evaluation.

### 5.4 Quality Assurance

- Apply consistent eligibility rules across all analyses.
- Calculate ratios from aggregated values.
- Reconcile company totals with dimensional breakdowns.
- Validate unexpected results before reporting them.
- Separate confirmed findings from hypotheses.
- Document unresolved data-quality limitations.
- Maintain traceability between findings, KPIs, and business questions.

## 6. Risks, Assumptions & Dependencies

### 6.1 Known Risks and Limitations

| ID | Risk or Limitation | Analytical Impact | Mitigation |
|---|---|---|---|
| R01 | Source order identity conflicts | Order Count and Average Order Value cannot be reported reliably. | Keep both KPIs blocked until the underlying issue is resolved and revalidated. |
| R02 | Records with unresolved data-quality issues | Results may vary depending on the selected reporting population. | Use the approved certified population for official reporting and disclose exclusions. |
| R03 | Unknown customer attribution | Customer segment analysis may include unattributed revenue and profit. | Preserve approved Unknown Customer classifications and report their contribution transparently. |
| R04 | Aggregation and calculation inconsistencies | Incorrect ratios or dimensional totals may misrepresent performance. | Apply standardized KPI formulas and reconcile results across analytical dimensions. |
| R05 | Unsupported causal interpretations | Observed relationships may be incorrectly presented as proven causes. | Distinguish descriptive evidence, diagnostic hypotheses, and confirmed findings. |
| R06 | Sales target granularity limitations | Targets may be incorrectly attributed to unsupported dimensions. | Respect the approved month-by-channel, All Markets target grain. |

### 6.2 Assumptions

- IRDS-BR001 and approved Business Clarifications govern the analysis.
- The controlled analytical dataset is the starting point for analytical execution.
- Only approved reporting populations and KPI definitions will be used.
- No additional business rules will be introduced without documented justification and approval.

### 6.3 Dependencies

- Availability of the controlled analytical dataset.
- Access to approved business requirements and clarifications.
- Availability of reconciliation and data-quality evidence.
- Successful validation of KPI calculations before business interpretation.
- Review of analytical findings before executive reporting.

## 7. Review & Approval


### 7.1 Review Checklist

- [ ] Business objectives and scope align with IRDS-BR001.
- [ ] All seven business questions are covered.
- [ ] Analytical requirements are correctly mapped.
- [ ] KPI definitions match approved business rules.
- [ ] Reporting populations and eligibility rules are verified.
- [ ] Restricted KPIs remain blocked.
- [ ] Analytical methods address the business questions.
- [ ] Known risks, assumptions, and dependencies are documented.
- [ ] Reconciliation and validation criteria are established.
- [ ] Approved Business Clarifications are incorporated.

### 7.2 Approval Status

| Field | Value |
|---|---|
| Document Status | Draft — Pending Review |
| Technical Review | Pending |
| Business Requirements Review | Pending |
| KPI Contract Validation | Pending |
| Execution Authorization | Not Yet Granted |

### 7.3 Approval Criteria

The analytical plan may be considered ready for execution only after all review checklist items have been verified and any material discrepancies have been resolved or formally documented.

Approval must be explicitly recorded and must not be assumed.

### 7.4 Execution Readiness Criteria

The analytical phase may begin only when:

1. All seven business questions are mapped to approved analytical requirements.
2. KPI definitions and eligibility rules are consistent with IRDS-BR001 and approved clarifications.
3. The certified analytical population is verified against the controlled dataset.
4. Financial control totals are independently reproduced.
5. Restricted KPIs remain disabled.
6. Known source-data limitations are documented.
7. Analytical methods and validation procedures are defined.
8. All material review findings are resolved or formally accepted.
9. Technical review is completed and execution authorization is recorded.

**Current Status:** PENDING VALIDATION

**Authorization:** NOT YET GRANTED

**Outstanding Activities:**
- Verify the updated Analytical Plan.
- Independently reproduce certified population counts and financial totals.
- Confirm implementation of CL-001 through CL-007.
- Complete the technical review checklist.
- Record the simulated execution authorization.
