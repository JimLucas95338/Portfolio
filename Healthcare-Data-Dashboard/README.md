# Healthcare Data Dashboard

## Overview
This project demonstrates comprehensive healthcare data analysis combining Python-based analytics with enterprise-level SQL database skills. It showcases both statistical analysis and advanced database querying techniques used in real healthcare environments.

## Objectives
- Analyze healthcare data to uncover trends and insights using both Python and SQL
- Demonstrate enterprise database design and complex query optimization
- Showcase advanced analytics including patient risk stratification and health equity analysis
- Visualize key metrics (readmission rates, costs, outcomes, operational performance)
- Communicate findings to technical and non-technical audiences

## Project Structure
- `data/` – Sample healthcare datasets (synthetic data for demonstration)
- `notebooks/` – Jupyter notebooks for analysis and visualization
  - `healthcare_dashboard_example.ipynb` – Python-based analytics and visualizations
  - `sql_analysis.ipynb` – Advanced SQL analytics demonstration
- `sql/` – Enterprise database design and queries
  - `healthcare_schema.sql` – Normalized database schema with indexing
  - `sample_queries.sql` – Complex analytics queries for healthcare BI
- `dashboard/` – Exported charts or dashboard files
- `docs/` – Documentation and reports

## Getting Started
1. Install Python and required libraries:
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter sqlite3
   ```
2. Explore the analysis notebooks:
   - Start with `notebooks/healthcare_dashboard_example.ipynb` for Python analytics
   - Review `notebooks/sql_analysis.ipynb` for advanced SQL demonstrations
3. Examine the SQL files:
   - `sql/healthcare_schema.sql` shows enterprise database design
   - `sql/sample_queries.sql` contains complex healthcare analytics queries
4. Review executive summaries and findings in the `docs/` folder.

## Key Features Demonstrated

### 📊 Python Analytics
- Patient demographics and outcomes analysis
- Statistical visualizations with matplotlib and seaborn
- Healthcare KPI calculations and trending
- Executive reporting with business insights

### 🗄️ Advanced SQL Analytics
- **Enterprise Database Design**: Normalized healthcare schema with proper indexing
- **Patient Risk Stratification**: Complex scoring algorithms using window functions
- **Health Equity Analysis**: Statistical disparity detection across demographics
- **Operational Performance**: Department benchmarking with efficiency metrics
- **Financial Analytics**: Cost-effectiveness and revenue optimization queries

### 💡 Business Intelligence
- Executive dashboards with actionable insights
- Regulatory compliance monitoring (health equity, quality metrics)
- Operational efficiency analysis and recommendations
- Strategic planning support with data-driven insights

## Executive Summary
See `docs/executive-summary.md` for a summary of key findings. 