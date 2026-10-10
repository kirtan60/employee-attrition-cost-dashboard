-- =====================================================================
-- Employee Attrition Analysis: SQL Queries
-- Dataset: HR Analytics (HR.csv), loaded into a table named `hr`
-- Dialect: SQLite (works in DB Browser for SQLite)
-- Note: "left" is a reserved word in SQL, so it is written in quotes.
-- =====================================================================


-- ---------------------------------------------------------------------
-- 0. DATA PREPARATION
-- The raw file has 14,999 rows including exact duplicates.
-- This view removes duplicates and renames `sales` to `department`
-- so results match the Streamlit dashboard (11,991 rows).
-- ---------------------------------------------------------------------
DROP VIEW IF EXISTS hr_clean;

CREATE VIEW hr_clean AS
SELECT DISTINCT
    satisfaction_level,
    last_evaluation,
    number_project,
    average_montly_hours,
    time_spend_company,
    Work_accident,
    "left",
    promotion_last_5years,
    sales AS department,
    salary
FROM hr;


-- ---------------------------------------------------------------------
-- 1. Data quality check: how many rows did cleaning remove?
-- ---------------------------------------------------------------------
SELECT
    (SELECT COUNT(*) FROM hr)       AS raw_rows,
    (SELECT COUNT(*) FROM hr_clean) AS clean_rows,
    (SELECT COUNT(*) FROM hr) - (SELECT COUNT(*) FROM hr_clean) AS rows_removed;


-- ---------------------------------------------------------------------
-- 2. Overall attrition rate
-- Business question: what share of employees leave?
-- ---------------------------------------------------------------------
SELECT
    COUNT(*)                          AS total_employees,
    SUM("left")                       AS employees_left,
    ROUND(AVG("left") * 100, 1)       AS attrition_pct,
    ROUND(AVG(satisfaction_level), 2) AS avg_satisfaction
FROM hr_clean;


-- ---------------------------------------------------------------------
-- 3. Attrition by salary level
-- Business question: do lower-paid employees leave more often?
-- ---------------------------------------------------------------------
SELECT
    salary,
    COUNT(*)                    AS employees,
    SUM("left")                 AS employees_left,
    ROUND(AVG("left") * 100, 1) AS attrition_pct
FROM hr_clean
GROUP BY salary
ORDER BY attrition_pct DESC;


-- ---------------------------------------------------------------------
-- 4. Attrition by department, with ranking (window function)
-- Business question: which departments lose the highest share of staff?
-- ---------------------------------------------------------------------
SELECT
    department,
    COUNT(*)                    AS employees,
    ROUND(AVG("left") * 100, 1) AS attrition_pct,
    RANK() OVER (ORDER BY AVG("left") DESC) AS attrition_rank
FROM hr_clean
GROUP BY department
ORDER BY attrition_rank;


-- ---------------------------------------------------------------------
-- 5. Stayed vs left: average hours, satisfaction, projects, tenure
-- Business question: how do employees who left differ from those who stayed?
-- ---------------------------------------------------------------------
SELECT
    CASE WHEN "left" = 1 THEN 'Left' ELSE 'Stayed' END AS status,
    COUNT(*)                              AS employees,
    ROUND(AVG(satisfaction_level), 2)     AS avg_satisfaction,
    ROUND(AVG(average_montly_hours), 1)   AS avg_monthly_hours,
    ROUND(AVG(number_project), 1)         AS avg_projects,
    ROUND(AVG(time_spend_company), 1)     AS avg_tenure_years
FROM hr_clean
GROUP BY "left";


-- ---------------------------------------------------------------------
-- 6. Attrition by number of projects
-- Business question: does workload relate to attrition?
-- ---------------------------------------------------------------------
SELECT
    number_project,
    COUNT(*)                    AS employees,
    ROUND(AVG("left") * 100, 1) AS attrition_pct
FROM hr_clean
GROUP BY number_project
ORDER BY number_project;


-- ---------------------------------------------------------------------
-- 7. Attrition by satisfaction band (CASE WHEN)
-- Business question: are low-satisfaction employees more likely to leave?
-- ---------------------------------------------------------------------
SELECT
    CASE
        WHEN satisfaction_level < 0.3 THEN '1. Low (< 0.3)'
        WHEN satisfaction_level < 0.5 THEN '2. Medium-low (0.3 - 0.49)'
        WHEN satisfaction_level < 0.7 THEN '3. Medium-high (0.5 - 0.69)'
        ELSE '4. High (0.7+)'
    END                         AS satisfaction_band,
    COUNT(*)                    AS employees,
    SUM("left")                 AS employees_left,
    ROUND(AVG("left") * 100, 1) AS attrition_pct
FROM hr_clean
GROUP BY satisfaction_band
ORDER BY satisfaction_band;


-- ---------------------------------------------------------------------
-- 8. Attrition by tenure (years at company)
-- Business question: at what point in their time at the company
-- do employees leave most?
-- ---------------------------------------------------------------------
SELECT
    time_spend_company          AS years_at_company,
    COUNT(*)                    AS employees,
    ROUND(AVG("left") * 100, 1) AS attrition_pct
FROM hr_clean
GROUP BY time_spend_company
ORDER BY time_spend_company;


-- ---------------------------------------------------------------------
-- 9. Estimated attrition cost by department
-- Same assumptions as the dashboard (illustrative, not real pay data):
--   Annual salary: low = 300,000 | medium = 600,000 | high = 1,200,000
--   Replacement cost = 50% of annual salary per employee who left
-- Business question: which departments cost the most in attrition?
-- ---------------------------------------------------------------------
SELECT
    department,
    SUM("left") AS employees_left,
    SUM(
        CASE salary
            WHEN 'low'    THEN 300000
            WHEN 'medium' THEN 600000
            WHEN 'high'   THEN 1200000
        END * 0.5 * "left"
    ) AS est_attrition_cost
FROM hr_clean
GROUP BY department
ORDER BY est_attrition_cost DESC;


-- ---------------------------------------------------------------------
-- 10. High performers who left (subquery)
-- Business question: are we losing our best people?
-- "High performer" = last evaluation above the company average.
-- ---------------------------------------------------------------------
SELECT
    department,
    COUNT(*) AS high_performers_left
FROM hr_clean
WHERE "left" = 1
  AND last_evaluation > (SELECT AVG(last_evaluation) FROM hr_clean)
GROUP BY department
ORDER BY high_performers_left DESC;
