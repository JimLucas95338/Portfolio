-- Healthcare Analytics Database Schema
-- Designed for healthcare KPI tracking and patient outcome analysis
-- 
-- SQLite Compatibility Note:
-- This schema is designed to work with SQLite for demonstration purposes.
-- For production use with PostgreSQL/MySQL/SQL Server, you can leverage additional
-- functions like STDDEV, PERCENTILE_CONT, advanced window functions, etc.

-- =====================================================
-- PATIENT DEMOGRAPHICS AND CORE INFO
-- =====================================================

CREATE TABLE patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    race_ethnicity VARCHAR(50),
    insurance_type VARCHAR(30) CHECK (insurance_type IN ('Private', 'Medicare', 'Medicaid', 'Uninsured')),
    zip_code VARCHAR(10),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- CLINICAL ENCOUNTERS AND VISITS
-- =====================================================

CREATE TABLE encounters (
    encounter_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    encounter_type VARCHAR(30) NOT NULL CHECK (encounter_type IN ('Inpatient', 'Outpatient', 'Emergency', 'Telehealth')),
    admission_date TIMESTAMP NOT NULL,
    discharge_date TIMESTAMP,
    department VARCHAR(50),
    primary_diagnosis_code VARCHAR(10),
    length_of_stay_days INTEGER,
    total_charges DECIMAL(10,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- =====================================================
-- DIAGNOSES AND CONDITIONS
-- =====================================================

CREATE TABLE diagnoses (
    diagnosis_id VARCHAR(20) PRIMARY KEY,
    encounter_id VARCHAR(20) NOT NULL,
    patient_id VARCHAR(20) NOT NULL,
    icd10_code VARCHAR(10) NOT NULL,
    diagnosis_description TEXT,
    diagnosis_type VARCHAR(20) CHECK (diagnosis_type IN ('Primary', 'Secondary', 'Comorbidity')),
    severity_score INTEGER CHECK (severity_score BETWEEN 1 AND 5),
    diagnosis_date DATE NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- =====================================================
-- CLINICAL OUTCOMES AND SCORES
-- =====================================================

CREATE TABLE patient_outcomes (
    outcome_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    encounter_id VARCHAR(20),
    outcome_type VARCHAR(30) NOT NULL,
    outcome_score DECIMAL(5,2),
    outcome_date DATE NOT NULL,
    assessment_method VARCHAR(50),
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
);

-- =====================================================
-- READMISSIONS TRACKING
-- =====================================================

CREATE TABLE readmissions (
    readmission_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    original_encounter_id VARCHAR(20) NOT NULL,
    readmission_encounter_id VARCHAR(20) NOT NULL,
    days_between_admissions INTEGER NOT NULL,
    readmission_type VARCHAR(30) CHECK (readmission_type IN ('Planned', 'Unplanned', 'Same Condition', 'Related Condition')),
    preventable_flag BOOLEAN DEFAULT FALSE,
    risk_score DECIMAL(5,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (original_encounter_id) REFERENCES encounters(encounter_id),
    FOREIGN KEY (readmission_encounter_id) REFERENCES encounters(encounter_id)
);

-- =====================================================
-- PROVIDER AND DEPARTMENT INFO
-- =====================================================

CREATE TABLE providers (
    provider_id VARCHAR(20) PRIMARY KEY,
    provider_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(50),
    department VARCHAR(50),
    years_experience INTEGER,
    quality_rating DECIMAL(3,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE encounter_providers (
    encounter_id VARCHAR(20),
    provider_id VARCHAR(20),
    role VARCHAR(30) CHECK (role IN ('Attending', 'Resident', 'Consulting', 'Primary')),
    PRIMARY KEY (encounter_id, provider_id),
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

-- =====================================================
-- QUALITY METRICS AND KPIs
-- =====================================================

CREATE TABLE quality_metrics (
    metric_id VARCHAR(20) PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_category VARCHAR(50) CHECK (metric_category IN ('Safety', 'Effectiveness', 'Timeliness', 'Efficiency', 'Equity', 'Patient Experience')),
    target_value DECIMAL(8,4),
    measurement_period VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE metric_results (
    result_id VARCHAR(20) PRIMARY KEY,
    metric_id VARCHAR(20) NOT NULL,
    measurement_date DATE NOT NULL,
    actual_value DECIMAL(8,4),
    patient_population_size INTEGER,
    department VARCHAR(50),
    provider_id VARCHAR(20),
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (metric_id) REFERENCES quality_metrics(metric_id),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

-- =====================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- =====================================================

-- Patient demographics indexes
CREATE INDEX idx_patients_insurance ON patients(insurance_type);
CREATE INDEX idx_patients_race ON patients(race_ethnicity);
CREATE INDEX idx_patients_zip ON patients(zip_code);

-- Encounter indexes for common queries
CREATE INDEX idx_encounters_patient ON encounters(patient_id);
CREATE INDEX idx_encounters_date ON encounters(admission_date);
CREATE INDEX idx_encounters_type ON encounters(encounter_type);
CREATE INDEX idx_encounters_department ON encounters(department);
CREATE INDEX idx_encounters_discharge ON encounters(discharge_date);

-- Diagnosis indexes
CREATE INDEX idx_diagnoses_patient ON diagnoses(patient_id);
CREATE INDEX idx_diagnoses_encounter ON diagnoses(encounter_id);
CREATE INDEX idx_diagnoses_icd10 ON diagnoses(icd10_code);
CREATE INDEX idx_diagnoses_date ON diagnoses(diagnosis_date);

-- Outcome indexes
CREATE INDEX idx_outcomes_patient ON patient_outcomes(patient_id);
CREATE INDEX idx_outcomes_date ON patient_outcomes(outcome_date);
CREATE INDEX idx_outcomes_type ON patient_outcomes(outcome_type);

-- Readmission indexes
CREATE INDEX idx_readmissions_patient ON readmissions(patient_id);
CREATE INDEX idx_readmissions_days ON readmissions(days_between_admissions);
CREATE INDEX idx_readmissions_type ON readmissions(readmission_type);

-- Quality metrics indexes
CREATE INDEX idx_metric_results_date ON metric_results(measurement_date);
CREATE INDEX idx_metric_results_dept ON metric_results(department);
CREATE INDEX idx_metric_results_provider ON metric_results(provider_id);

-- =====================================================
-- VIEWS FOR COMMON BUSINESS QUERIES
-- =====================================================

-- Patient summary view with demographics and latest encounter
CREATE VIEW patient_summary AS
SELECT 
    p.patient_id,
    p.gender,
    p.race_ethnicity,
    p.insurance_type,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) as age,
    COUNT(e.encounter_id) as total_encounters,
    MAX(e.admission_date) as last_encounter_date,
    AVG(e.length_of_stay_days) as avg_length_of_stay
FROM patients p
LEFT JOIN encounters e ON p.patient_id = e.patient_id
GROUP BY p.patient_id, p.gender, p.race_ethnicity, p.insurance_type, p.date_of_birth;

-- 30-day readmission rate by department
CREATE VIEW readmission_rates_by_dept AS
SELECT 
    e.department,
    COUNT(DISTINCT e.encounter_id) as total_discharges,
    COUNT(DISTINCT r.readmission_id) as readmissions_30_day,
    ROUND(
        COUNT(DISTINCT r.readmission_id) * 100.0 / COUNT(DISTINCT e.encounter_id), 
        2
    ) as readmission_rate_percent
FROM encounters e
LEFT JOIN readmissions r ON e.encounter_id = r.original_encounter_id 
    AND r.days_between_admissions <= 30
WHERE e.discharge_date IS NOT NULL
GROUP BY e.department
ORDER BY readmission_rate_percent DESC;

-- Quality metrics dashboard view
CREATE VIEW quality_dashboard AS
SELECT 
    qm.metric_name,
    qm.metric_category,
    mr.measurement_date,
    mr.actual_value,
    qm.target_value,
    CASE 
        WHEN mr.actual_value >= qm.target_value THEN 'Met Target'
        WHEN mr.actual_value >= qm.target_value * 0.9 THEN 'Near Target'
        ELSE 'Below Target'
    END as performance_status,
    mr.department
FROM quality_metrics qm
JOIN metric_results mr ON qm.metric_id = mr.metric_id
WHERE mr.measurement_date >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY mr.measurement_date DESC, qm.metric_category;