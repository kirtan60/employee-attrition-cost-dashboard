# Employee Attrition & Workforce Cost Dashboard

An interactive Streamlit dashboard, backed by SQL analysis, that shows which employees leave and estimates what that attrition costs the business.

🔗 **Live demo:** <https://employee-attrition-cost-dashboard-bk3xddct8pmagjghd6rrxs.streamlit.app/>

## Problem Statement

Employee attrition is expensive: companies lose experience and pay to recruit and train replacements. This project answers four business questions:

1. How many employees leave, and who is most likely to leave?
2. Which salary levels, departments, workloads and tenure groups have the highest attrition?
3. How do employees who left differ from those who stayed?
4. What is the estimated cost of that attrition?

## Dataset

- **Source:** HR Analytics dataset from Kaggle (employee satisfaction, evaluation, projects, monthly hours, tenure, salary level, department, and whether the employee left).
- **Size:** 14,999 rows originally, **11,991 rows** after removing 3,008 duplicate/missing rows.
- Note: duplicate rows were removed on the assumption that they are repeated records. In a real company setting, I would confirm this with the data owner, since identical rows could be different employees.

## Tools Used

Python · pandas · Plotly · Streamlit · SQL (SQLite)

## Key Findings

| Metric | Value |
|---|---|
| Total employees (after cleaning) | 11,991 |
| Average satisfaction | 0.63 |
| Overall attrition rate | 16.6% |
| Estimated attrition cost | ₹435,600,000 (~₹43.56 crore) |

**Attrition by salary level**

| Salary level | Attrition % |
|---|---|
| Low | 20.5% |
| Medium | 14.6% |
| High | 4.8% |

**Attrition by department**

- Highest: HR (18.8%), Accounting (17.6%), Technical (17.4%)
- Lowest: Management (11.9%), R&D (12.2%)

**Takeaways**

- **Salary matters most.** Low-salary employees leave about 4x as often as high-salary employees (20.5% vs 4.8%). Differences between departments (11.9% to 18.8%) are much smaller.
- **Workload has a U-shape.** Attrition is 54.2% for employees with 2 projects, only 1.1% with 3 projects, 44.9% with 6 projects, and 100% with 7 projects (145 employees). Both under-used and overloaded employees leave.
- **Satisfaction separates leavers from stayers.** Average satisfaction was 0.44 for employees who left vs 0.67 for those who stayed. Attrition is 48.3% for satisfaction of 0.3 to 0.49 and 39.1% below 0.3, but 9.8% of highly satisfied employees (0.7+) also left, so satisfaction alone does not explain attrition.
- **Year 5 is the peak.** Attrition is 45.4% for employees in their 5th year, and none of the employees with 7+ years left.
- **Sales has the highest estimated attrition cost** (about ₹12.08 crore), followed by Technical (₹8.43 crore) and Support (₹6.65 crore). Sales ranks first mainly because it is the largest department, not because it has the highest attrition rate (HR does).

## SQL Analysis

`queries.sql` contains 10 commented queries (GROUP BY, CASE WHEN, window functions, subqueries) that reproduce and extend the dashboard analysis: attrition by salary, department, projects, satisfaction band and tenure; stayed vs left comparison; estimated cost by department; and high performers who left. The queries run on SQLite (DB Browser for SQLite works).

## Cost Estimation Method

The dataset only has salary *levels* (low / medium / high), not actual pay, so the cost estimate relies on **assumptions** that can be changed in the dashboard sidebar:

- Assumed annual salary: Low ₹3,00,000 · Medium ₹6,00,000 · High ₹12,00,000
- Replacement cost: 50% of annual salary per employee who left

`Estimated cost = assumed annual salary × replacement cost % × employees who left`

These figures are illustrative. With real salary data, the estimate would be more accurate.

## Recommendations

Based on the findings, a company could:

1. Review pay and retention plans for low-salary roles, where attrition is highest.
2. Review workload balance: employees with very few or very many projects leave far more often than those with 3 to 4.
3. Pay attention to employees in their 4th and 5th year, where attrition peaks.
4. Track satisfaction regularly, but not on its own: most leavers had low satisfaction, yet a smaller group left despite high scores.

*These patterns show association, not proof of cause. Further analysis (such as exit interviews) would be needed to confirm reasons.*

## Dashboard Features

- Upload your own CSV/Excel file or use the default `HR.csv`
- Filters by department and salary level
- KPIs: total employees, average satisfaction, attrition rate, estimated attrition cost
- Attrition tables by salary level and department
- Estimated attrition cost by department
- Charts: satisfaction distribution, projects vs monthly hours, salary distribution, employees by department, satisfaction of employees who stayed vs left
- Adjustable cost assumptions
- Download cleaned data

## How to Run Locally

```bash
git clone https://github.com/kirtan60/employee-attrition-cost-dashboard.git
cd employee-attrition-cost-dashboard
pip install -r requirements.txt
streamlit run app2.py
```

## Project Structure

```
├── app2.py            # Streamlit dashboard
├── queries.sql        # SQL analysis (10 queries)
├── HR.csv             # Dataset
├── requirements.txt   # Dependencies
└── README.md
```

## Author

**Kirtan** · [GitHub](https://github.com/kirtan60) · [LinkedIn](https://www.linkedin.com/in/kirtan-patel-b01692290/)
