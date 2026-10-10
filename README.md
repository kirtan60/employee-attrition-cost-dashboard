# Employee Attrition & Workforce Cost Dashboard

An interactive Streamlit dashboard that analyzes why employees leave and estimates what that attrition costs the business.

🔗 **Live demo:** https://employee-attrition-cost-dashboard-bk3xddct8pmagjghd6rrxs.streamlit.app/



## Problem Statement

Employee attrition is expensive: companies lose experience and pay to recruit and train replacements. This project answers three business questions:

1. How many employees leave, and who is most likely to leave?
2. Which salary levels and departments have the highest attrition?
3. What is the estimated cost of that attrition?

## Dataset

- **Source:** HR Analytics dataset from Kaggle (employee satisfaction, evaluation, projects, monthly hours, tenure, salary level, department, and whether the employee left).
- **Size:** 14,999 rows originally, **11,991 rows** after removing 3,008 duplicate/missing rows.
- Note: duplicate rows were removed on the assumption that they are repeated records. In a real company setting, I would confirm this with the data owner, since identical rows could be different employees.

## Tools Used

Python · pandas · Plotly · Streamlit

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

**Attrition by department (highest and lowest)**

- Highest: HR (18.8%), Accounting (17.6%), Technical (17.4%)
- Lowest: Management (11.9%), R&D (12.2%)

**Takeaways**

- Salary level is the strongest driver of attrition in this data: low-salary employees leave about 4x as often as high-salary employees.
- Differences between departments (11.9% to 18.8%) are much smaller than differences between salary levels.

## Cost Estimation Method

The dataset only has salary *levels* (low / medium / high), not actual pay, so the cost estimate relies on **assumptions** that can be changed in the dashboard sidebar:

- Assumed annual salary: Low ₹3,00,000 · Medium ₹6,00,000 · High ₹12,00,000
- Replacement cost: 50% of annual salary per employee who left

`Estimated cost = assumed annual salary × replacement cost % × employees who left`

These figures are illustrative. With real salary data, the estimate would be more accurate.

## Recommendations

Based on the findings, a company could:

1. Review pay and retention plans for low-salary roles, where attrition is highest.
2. Look into why HR, Accounting, and Technical teams have higher attrition than other departments.
3. Track satisfaction scores regularly, since satisfaction differs between employees who stayed and those who left.

*These patterns show association, not proof of cause. Further analysis (such as exit interviews) would be needed to confirm reasons.*

## Dashboard Features

- Upload your own CSV/Excel file or use the default `HR.csv`
- Filters by department and salary level
- KPIs: total employees, average satisfaction, attrition rate, estimated attrition cost
- Attrition tables by salary level and department
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
├── HR.csv             # Dataset
├── requirements.txt   # Dependencies
└── README.md
```

## Author

**Kirtan** · [GitHub](https://github.com/kirtan60)
