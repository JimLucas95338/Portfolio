-- =====================================================
-- HEALTHCARE ANALYTICS: ADVANCED SQL QUERIES
-- Demonstrating complex healthcare data analysis patterns
-- 
-- SQLite Compatibility Note:
-- These queries are designed to work with SQLite for portability.
-- In production environments (PostgreSQL/MySQL/SQL Server), you would
-- use additional statistical functions like STDDEV, PERCENTILE_CONT,
-- LAG/LEAD for time series analysis, etc.
-- =====================================================

-- =====================================================
-- 1. PATIENT COHORT ANALYSIS
-- =====================================================

-- Find high-risk patients with multiple comorbidities
WITH patient_comorbidities AS (
    SELECT 
        p.patient_id,
        p.gender,
        p.race_ethnicity,
        p.insurance_type,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) as age,
        COUNT(DISTINCT d.icd10_code) as comorbidity_count,
        AVG(d.severity_score) as avg_severity,
        STRING_AGG(DISTINCT d.diagnosis_description, '; ') as conditions
    FROM patients p
    JOIN diagnoses d ON p.patient_id = d.patient_id
    WHERE d.diagnosis_type IN ('Primary', 'Comorbidity')
    GROUP BY p.patient_id, p.gender, p.race_ethnicity, p.insurance_type, p.date_of_birth
)
SELECT 
    patient_id,
    age,
    gender,
    race_ethnicity,
    insurance_type,
    comorbidity_count,
    ROUND(avg_severity, 2) as avg_severity_score,
    conditions
FROM patient_comorbidities
WHERE comorbidity_count >= 3 
    AND avg_severity > 3.0
ORDER BY comorbidity_count DESC, avg_severity DESC
LIMIT 100;

-- =====================================================
-- 2. READMISSION RISK ANALYSIS
-- =====================================================

-- Identify patients at high risk for 30-day readmission
WITH readmission_history AS (
    SELECT 
        e.patient_id,
        COUNT(r.readmission_id) as historical_readmissions,
        AVG(r.days_between_admissions) as avg_days_between,
        MAX(r.risk_score) as max_risk_score
    FROM encounters e
    LEFT JOIN readmissions r ON e.patient_id = r.patient_id
    WHERE e.discharge_date >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY e.patient_id
),
recent_encounters AS (
    SELECT 
        e.patient_id,
        e.encounter_id,
        e.discharge_date,
        e.length_of_stay_days,
        e.department,
        d.diagnosis_description as primary_diagnosis,
        d.severity_score
    FROM encounters e
    JOIN diagnoses d ON e.encounter_id = d.encounter_id 
        AND d.diagnosis_type = 'Primary'
    WHERE e.discharge_date IS NOT NULL
        AND e.discharge_date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT 
    re.patient_id,
    ps.age,
    ps.insurance_type,
    re.department,
    re.primary_diagnosis,
    re.length_of_stay_days,
    re.severity_score,
    COALESCE(rh.historical_readmissions, 0) as prior_readmissions,
    COALESCE(rh.max_risk_score, 0) as historical_risk_score,
    CASE 
        WHEN rh.historical_readmissions > 2 THEN 'High'
        WHEN rh.historical_readmissions > 0 OR re.severity_score > 4 THEN 'Medium'
        ELSE 'Low'
    END as readmission_risk_level
FROM recent_encounters re
JOIN patient_summary ps ON re.patient_id = ps.patient_id
LEFT JOIN readmission_history rh ON re.patient_id = rh.patient_id
ORDER BY rh.historical_readmissions DESC NULLS LAST, re.severity_score DESC;

-- =====================================================
-- 3. PROVIDER PERFORMANCE ANALYTICS
-- =====================================================

-- Provider performance scorecard with statistical significance
WITH provider_outcomes AS (
    SELECT 
        ep.provider_id,
        pr.provider_name,
        pr.specialty,
        pr.department,
        COUNT(DISTINCT e.encounter_id) as total_encounters,
        AVG(e.length_of_stay_days) as avg_los,
        AVG(po.outcome_score) as avg_outcome_score,
        -- Note: SQLite doesn't have STDDEV, using range as variability measure
        (MAX(po.outcome_score) - MIN(po.outcome_score)) as outcome_score_range,
        COUNT(r.readmission_id) as readmissions_30_day,
        SUM(e.total_charges) as total_revenue
    FROM encounter_providers ep
    JOIN providers pr ON ep.provider_id = pr.provider_id
    JOIN encounters e ON ep.encounter_id = e.encounter_id
    LEFT JOIN patient_outcomes po ON e.encounter_id = po.encounter_id
    LEFT JOIN readmissions r ON e.encounter_id = r.original_encounter_id 
        AND r.days_between_admissions <= 30
    WHERE e.admission_date >= CURRENT_DATE - INTERVAL '1 year'
        AND ep.role = 'Attending'
    GROUP BY ep.provider_id, pr.provider_name, pr.specialty, pr.department
    HAVING COUNT(DISTINCT e.encounter_id) >= 20  -- Minimum case volume for statistical relevance
),
department_benchmarks AS (
    SELECT 
        department,
        AVG(avg_los) as dept_avg_los,
        AVG(avg_outcome_score) as dept_avg_outcome,
        AVG(readmissions_30_day * 100.0 / total_encounters) as dept_readmission_rate
    FROM provider_outcomes
    GROUP BY department
)
SELECT 
    po.provider_name,
    po.specialty,
    po.department,
    po.total_encounters,
    ROUND(po.avg_los, 1) as avg_length_of_stay,
    ROUND(db.dept_avg_los, 1) as dept_benchmark_los,
    ROUND(po.avg_outcome_score, 2) as avg_patient_outcome,
    ROUND(db.dept_avg_outcome, 2) as dept_benchmark_outcome,
    ROUND(po.readmissions_30_day * 100.0 / po.total_encounters, 2) as readmission_rate_percent,
    ROUND(db.dept_readmission_rate, 2) as dept_benchmark_readmission,
    -- Performance indicators
    CASE 
        WHEN po.avg_los < db.dept_avg_los * 0.9 THEN 'Above Average'
        WHEN po.avg_los > db.dept_avg_los * 1.1 THEN 'Below Average'
        ELSE 'Average'
    END as los_performance,
    CASE 
        WHEN po.avg_outcome_score > db.dept_avg_outcome * 1.05 THEN 'Above Average'
        WHEN po.avg_outcome_score < db.dept_avg_outcome * 0.95 THEN 'Below Average'
        ELSE 'Average'
    END as outcome_performance
FROM provider_outcomes po
JOIN department_benchmarks db ON po.department = db.department
ORDER BY po.department, po.avg_outcome_score DESC;

-- =====================================================
-- 4. HEALTH EQUITY ANALYSIS
-- =====================================================

-- Analyze healthcare disparities by demographics
WITH outcome_by_demographics AS (
    SELECT 
        p.race_ethnicity,
        p.insurance_type,
        p.gender,
        CASE 
            WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) < 30 THEN 'Under 30'
            WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) < 50 THEN '30-49'
            WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) < 70 THEN '50-69'
            ELSE '70+'
        END as age_group,
        COUNT(DISTINCT e.encounter_id) as encounter_count,
        AVG(po.outcome_score) as avg_outcome_score,
        AVG(e.length_of_stay_days) as avg_length_of_stay,
        COUNT(r.readmission_id) as readmissions,
        AVG(e.total_charges) as avg_charges
    FROM patients p
    JOIN encounters e ON p.patient_id = e.patient_id
    LEFT JOIN patient_outcomes po ON e.encounter_id = po.encounter_id
    LEFT JOIN readmissions r ON e.encounter_id = r.original_encounter_id 
        AND r.days_between_admissions <= 30
    WHERE e.admission_date >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY p.race_ethnicity, p.insurance_type, p.gender, age_group
    HAVING COUNT(DISTINCT e.encounter_id) >= 10  -- Minimum for statistical relevance
),
overall_averages AS (
    SELECT 
        AVG(avg_outcome_score) as overall_avg_outcome,
        AVG(avg_length_of_stay) as overall_avg_los,
        AVG(readmissions * 100.0 / encounter_count) as overall_readmission_rate
    FROM outcome_by_demographics
)
SELECT 
    obd.race_ethnicity,
    obd.insurance_type,
    obd.gender,
    obd.age_group,
    obd.encounter_count,
    ROUND(obd.avg_outcome_score, 2) as avg_outcome_score,
    ROUND(oa.overall_avg_outcome, 2) as system_avg_outcome,
    ROUND(obd.avg_length_of_stay, 1) as avg_los,
    ROUND(oa.overall_avg_los, 1) as system_avg_los,
    ROUND(obd.readmissions * 100.0 / obd.encounter_count, 2) as readmission_rate,
    ROUND(oa.overall_readmission_rate, 2) as system_readmission_rate,
    -- Disparity indicators
    ROUND((obd.avg_outcome_score - oa.overall_avg_outcome), 2) as outcome_disparity,
    ROUND((obd.avg_length_of_stay - oa.overall_avg_los), 1) as los_disparity,
    CASE 
        WHEN obd.avg_outcome_score < oa.overall_avg_outcome * 0.95 THEN 'Concerning'
        WHEN obd.avg_outcome_score > oa.overall_avg_outcome * 1.05 THEN 'Above Average'
        ELSE 'On Par'
    END as equity_status
FROM outcome_by_demographics obd
CROSS JOIN overall_averages oa
ORDER BY obd.race_ethnicity, obd.insurance_type;

-- =====================================================
-- 5. SEASONAL TRENDS AND CAPACITY PLANNING
-- =====================================================

-- Monthly admission patterns with forecasting insights
WITH monthly_trends AS (
    SELECT 
        DATE_TRUNC('month', e.admission_date) as month_year,
        e.department,
        COUNT(*) as admissions,
        AVG(e.length_of_stay_days) as avg_los,
        SUM(e.length_of_stay_days) as total_patient_days,
        COUNT(DISTINCT e.patient_id) as unique_patients
    FROM encounters e
    WHERE e.admission_date >= CURRENT_DATE - INTERVAL '2 years'
    GROUP BY DATE_TRUNC('month', e.admission_date), e.department
),
seasonal_patterns AS (
    SELECT 
        department,
        EXTRACT(MONTH FROM month_year) as month_number,
        TO_CHAR(month_year, 'Month') as month_name,
        AVG(admissions) as avg_monthly_admissions,
        STDDEV(admissions) as admission_volatility,
        AVG(total_patient_days) as avg_patient_days,
        COUNT(*) as data_points
    FROM monthly_trends
    GROUP BY department, EXTRACT(MONTH FROM month_year), TO_CHAR(month_year, 'Month')
)
SELECT 
    department,
    month_name,
    ROUND(avg_monthly_admissions, 0) as avg_admissions,
    ROUND(admission_volatility, 1) as volatility,
    ROUND(avg_patient_days, 0) as avg_patient_days,
    CASE 
        WHEN avg_monthly_admissions > (
            SELECT AVG(avg_monthly_admissions) * 1.2 
            FROM seasonal_patterns sp2 
            WHERE sp2.department = seasonal_patterns.department
        ) THEN 'High Season'
        WHEN avg_monthly_admissions < (
            SELECT AVG(avg_monthly_admissions) * 0.8 
            FROM seasonal_patterns sp2 
            WHERE sp2.department = seasonal_patterns.department
        ) THEN 'Low Season'
        ELSE 'Normal'
    END as season_category,
    data_points as months_of_data
FROM seasonal_patterns
WHERE data_points >= 4  -- At least 4 months of data for reliability
ORDER BY department, EXTRACT(MONTH FROM TO_DATE(month_name, 'Month'));

-- =====================================================
-- 6. FINANCIAL IMPACT ANALYSIS
-- =====================================================

-- Cost analysis with risk adjustment
WITH encounter_financials AS (
    SELECT 
        e.encounter_id,
        e.patient_id,
        e.department,
        e.total_charges,
        e.length_of_stay_days,
        d.severity_score,
        CASE WHEN r.readmission_id IS NOT NULL THEN 1 ELSE 0 END as had_readmission,
        -- Risk adjustment based on patient complexity
        CASE 
            WHEN d.severity_score >= 4 THEN 'High Complexity'
            WHEN d.severity_score >= 2 THEN 'Medium Complexity'
            ELSE 'Low Complexity'
        END as case_complexity
    FROM encounters e
    LEFT JOIN diagnoses d ON e.encounter_id = d.encounter_id 
        AND d.diagnosis_type = 'Primary'
    LEFT JOIN readmissions r ON e.encounter_id = r.original_encounter_id 
        AND r.days_between_admissions <= 30
    WHERE e.discharge_date IS NOT NULL
        AND e.admission_date >= CURRENT_DATE - INTERVAL '1 year'
),
department_metrics AS (
    SELECT 
        department,
        case_complexity,
        COUNT(*) as case_count,
        AVG(total_charges) as avg_revenue_per_case,
        AVG(length_of_stay_days) as avg_los,
        SUM(had_readmission) as readmission_count,
        SUM(total_charges) as total_revenue,
        -- Cost estimates (simplified)
        AVG(total_charges / length_of_stay_days) as revenue_per_day,
        AVG(length_of_stay_days * 2000) as estimated_cost_per_case  -- $2000/day estimate
    FROM encounter_financials
    WHERE total_charges > 0
    GROUP BY department, case_complexity
)
SELECT 
    department,
    case_complexity,
    case_count,
    ROUND(avg_revenue_per_case, 0) as avg_revenue,
    ROUND(avg_los, 1) as avg_length_of_stay,
    ROUND(total_revenue, 0) as total_revenue,
    ROUND(estimated_cost_per_case, 0) as estimated_cost,
    ROUND(avg_revenue_per_case - estimated_cost_per_case, 0) as estimated_margin,
    ROUND(readmission_count * 100.0 / case_count, 2) as readmission_rate,
    -- Financial impact of readmissions (penalty estimate)
    ROUND(readmission_count * avg_revenue_per_case * 0.01, 0) as readmission_penalty_estimate
FROM department_metrics
ORDER BY department, case_complexity;