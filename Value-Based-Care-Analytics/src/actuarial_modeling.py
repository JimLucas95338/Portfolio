"""
Actuarial Risk Modeling & Shared Savings Calculations
====================================================

Actuarial modeling for value-based care contracts,
including shared savings calculations, risk adjustment, and financial forecasting.

Key Features:
- Medicare risk adjustment (HCC coding)
- Shared savings calculations for MSSP/ACO REACH
- Financial risk modeling and reserves
- Contract performance optimization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class ActuarialEngine:
    """
    Actuarial modeling engine for value-based care contracts.
    
    Provides comprehensive financial modeling including risk adjustment,
    shared savings calculations, and contract performance optimization.
    """
    
    def __init__(self):
        # Medicare HCC (Hierarchical Condition Categories) risk adjustment factors
        self.hcc_risk_factors = {
            # High-cost chronic conditions
            'hcc_8_metastatic_cancer': 2.505,
            'hcc_9_lung_cancer': 1.367,
            'hcc_17_diabetes_complications': 0.318,
            'hcc_18_diabetes_no_complications': 0.104,
            'hcc_85_heart_failure': 0.323,
            'hcc_86_acute_mi': 0.184,
            'hcc_87_unstable_angina': 0.143,
            'hcc_88_coronary_atherosclerosis': 0.095,
            'hcc_106_atherosclerosis': 0.187,
            'hcc_107_vascular_disease': 0.140,
            'hcc_108_copd': 0.335,
            'hcc_111_kidney_disease': 0.287,
            'hcc_134_dialysis_status': 1.398,
            'hcc_135_chronic_kidney_disease': 0.287,
            'hcc_157_pressure_ulcer': 0.445,
            'hcc_161_chronic_ulcer_skin': 0.213,
            'hcc_166_severe_hematological': 0.751,
            'hcc_167_multiple_sclerosis': 0.456,
            'hcc_169_parkinson_huntington': 0.438,
            'hcc_170_seizure_disorders': 0.151,
            'hcc_176_spinal_cord_disorders': 0.525
        }
        
        # Age and demographic factors
        self.demographic_factors = {
            'age_65_69': 0.435,
            'age_70_74': 0.715,
            'age_75_79': 1.018,
            'age_80_84': 1.334,
            'age_85_89': 1.597,
            'age_90_94': 1.948,
            'age_95_plus': 2.075,
            'male': 0.067,
            'female': 0.0,  # baseline
            'medicaid_dual': 0.146,
            'disability_status': 0.170
        }
        
        # Medicare benchmark costs (national averages)
        self.medicare_benchmarks = {
            'fee_for_service_pmpm': 850,  # Per member per month
            'quality_bonus_threshold': 3.5,  # Star rating threshold
            'shared_savings_rate': 0.50,  # 50% shared savings rate
            'minimum_savings_rate': 0.02,  # 2% minimum savings rate
            'maximum_sharing_rate': 0.10,  # 10% maximum sharing rate
            'quality_performance_threshold': 0.60  # 60% of quality measures
        }
        
        # Financial reserve requirements
        self.reserve_requirements = {
            'minimum_medical_loss_ratio': 0.85,
            'risk_corridor_upper': 0.08,  # 8% risk corridor
            'risk_corridor_lower': -0.08,
            'ibnr_reserve_rate': 0.12,  # Incurred but not reported
            'trend_factor_annual': 0.045  # 4.5% annual medical cost trend
        }
    
    def calculate_risk_adjustment(self, patient_panel: pd.DataFrame) -> Dict:
        """
        Calculate Medicare risk adjustment scores using HCC methodology.
        
        Args:
            patient_panel: DataFrame containing patient demographics and conditions
            
        Returns:
            Dictionary with risk scores and financial impact
        """
        total_risk_score = 0
        panel_size = len(patient_panel)
        risk_score_details = []
        
        for _, patient in patient_panel.iterrows():
            patient_risk_score = self._calculate_individual_risk_score(patient)
            total_risk_score += patient_risk_score['total_score']
            risk_score_details.append({
                'patient_id': patient.get('patient_id', ''),
                'risk_score': patient_risk_score['total_score'],
                'demographic_score': patient_risk_score['demographic_score'],
                'condition_score': patient_risk_score['condition_score'],
                'risk_factors': patient_risk_score['risk_factors']
            })
        
        average_risk_score = total_risk_score / panel_size if panel_size > 0 else 1.0
        
        # Calculate financial impact
        baseline_pmpm = self.medicare_benchmarks['fee_for_service_pmpm']
        risk_adjusted_pmpm = baseline_pmpm * average_risk_score
        annual_risk_adjustment = (risk_adjusted_pmpm - baseline_pmpm) * 12 * panel_size
        
        return {
            'panel_metrics': {
                'panel_size': panel_size,
                'average_risk_score': round(average_risk_score, 3),
                'total_risk_score': round(total_risk_score, 2),
                'baseline_pmpm': baseline_pmpm,
                'risk_adjusted_pmpm': round(risk_adjusted_pmpm, 2)
            },
            'financial_impact': {
                'annual_risk_adjustment': round(annual_risk_adjustment, 2),
                'monthly_adjustment': round(annual_risk_adjustment / 12, 2),
                'risk_adjustment_percentage': round((average_risk_score - 1.0) * 100, 1)
            },
            'patient_details': risk_score_details,
            'risk_distribution': self._analyze_risk_distribution(risk_score_details)
        }
    
    def _calculate_individual_risk_score(self, patient: pd.Series) -> Dict:
        """Calculate HCC risk score for individual patient."""
        demographic_score = 1.0  # Base score
        condition_score = 0.0
        risk_factors = []
        
        # Age-based scoring
        age = patient.get('age', 65)
        if age >= 95:
            demographic_score += self.demographic_factors['age_95_plus']
            risk_factors.append('Age 95+')
        elif age >= 90:
            demographic_score += self.demographic_factors['age_90_94']
            risk_factors.append('Age 90-94')
        elif age >= 85:
            demographic_score += self.demographic_factors['age_85_89']
            risk_factors.append('Age 85-89')
        elif age >= 80:
            demographic_score += self.demographic_factors['age_80_84']
            risk_factors.append('Age 80-84')
        elif age >= 75:
            demographic_score += self.demographic_factors['age_75_79']
            risk_factors.append('Age 75-79')
        elif age >= 70:
            demographic_score += self.demographic_factors['age_70_74']
            risk_factors.append('Age 70-74')
        elif age >= 65:
            demographic_score += self.demographic_factors['age_65_69']
            risk_factors.append('Age 65-69')
        
        # Gender
        gender = patient.get('gender', 'female').lower()
        if gender == 'male':
            demographic_score += self.demographic_factors['male']
        
        # Dual eligibility and disability
        if patient.get('medicaid_dual', False):
            demographic_score += self.demographic_factors['medicaid_dual']
            risk_factors.append('Medicaid Dual Eligible')
        
        if patient.get('disability_status', False):
            demographic_score += self.demographic_factors['disability_status']
            risk_factors.append('Disability Status')
        
        # HCC conditions
        conditions = patient.get('hcc_conditions', [])
        if isinstance(conditions, str):
            conditions = conditions.split(',') if conditions else []
        
        for condition in conditions:
            condition_key = f'hcc_{condition.strip()}'
            if condition_key in self.hcc_risk_factors:
                condition_score += self.hcc_risk_factors[condition_key]
                risk_factors.append(f'HCC {condition.strip()}')
        
        total_score = demographic_score + condition_score
        
        return {
            'total_score': round(total_score, 3),
            'demographic_score': round(demographic_score, 3),
            'condition_score': round(condition_score, 3),
            'risk_factors': risk_factors
        }
    
    def _analyze_risk_distribution(self, risk_details: List[Dict]) -> Dict:
        """Analyze risk score distribution across patient panel."""
        risk_scores = [patient['risk_score'] for patient in risk_details]
        
        return {
            'percentiles': {
                '10th': round(np.percentile(risk_scores, 10), 2),
                '25th': round(np.percentile(risk_scores, 25), 2),
                '50th': round(np.percentile(risk_scores, 50), 2),
                '75th': round(np.percentile(risk_scores, 75), 2),
                '90th': round(np.percentile(risk_scores, 90), 2)
            },
            'risk_categories': {
                'low_risk': len([s for s in risk_scores if s < 1.0]),
                'average_risk': len([s for s in risk_scores if 1.0 <= s < 2.0]),
                'high_risk': len([s for s in risk_scores if 2.0 <= s < 4.0]),
                'very_high_risk': len([s for s in risk_scores if s >= 4.0])
            },
            'statistics': {
                'mean': round(np.mean(risk_scores), 3),
                'std_dev': round(np.std(risk_scores), 3),
                'min': round(min(risk_scores), 3),
                'max': round(max(risk_scores), 3)
            }
        }
    
    def calculate_shared_savings(self, actual_costs: Dict, benchmark_costs: Dict, 
                                quality_scores: Dict) -> Dict:
        """
        Calculate shared savings for value-based care contracts (MSSP/ACO REACH).
        
        Args:
            actual_costs: Actual medical costs incurred
            benchmark_costs: Benchmark costs for comparison
            quality_scores: Quality performance metrics
            
        Returns:
            Comprehensive shared savings calculation
        """
        # Calculate gross savings
        total_actual = actual_costs['total_medical_costs']
        total_benchmark = benchmark_costs['total_benchmark_costs']
        gross_savings = total_benchmark - total_actual
        gross_savings_rate = gross_savings / total_benchmark if total_benchmark > 0 else 0
        
        # Check minimum savings rate requirement
        min_savings_rate = self.medicare_benchmarks['minimum_savings_rate']
        meets_minimum = gross_savings_rate >= min_savings_rate
        
        # Calculate quality performance
        quality_performance = self._assess_quality_performance(quality_scores)
        meets_quality_threshold = quality_performance['overall_score'] >= \
                                self.medicare_benchmarks['quality_performance_threshold']
        
        # Determine sharing rate based on quality performance
        if meets_quality_threshold:
            if quality_performance['overall_score'] >= 0.90:
                sharing_rate = 0.60  # Enhanced sharing rate
            elif quality_performance['overall_score'] >= 0.75:
                sharing_rate = 0.55
            else:
                sharing_rate = self.medicare_benchmarks['shared_savings_rate']
        else:
            sharing_rate = 0.0  # No sharing if quality thresholds not met
        
        # Calculate final shared savings
        if meets_minimum and meets_quality_threshold:
            # Apply maximum sharing cap
            max_sharing_amount = total_benchmark * self.medicare_benchmarks['maximum_sharing_rate']
            eligible_savings = min(gross_savings, max_sharing_amount)
            shared_savings_amount = eligible_savings * sharing_rate
        else:
            shared_savings_amount = 0
            eligible_savings = 0
        
        return {
            'savings_calculation': {
                'total_benchmark_costs': total_benchmark,
                'total_actual_costs': total_actual,
                'gross_savings': round(gross_savings, 2),
                'gross_savings_rate': round(gross_savings_rate * 100, 2),
                'meets_minimum_savings': meets_minimum,
                'minimum_savings_threshold': min_savings_rate * 100
            },
            'quality_assessment': quality_performance,
            'shared_savings_results': {
                'eligible_for_sharing': meets_minimum and meets_quality_threshold,
                'sharing_rate': sharing_rate * 100,
                'eligible_savings': round(eligible_savings, 2),
                'shared_savings_amount': round(shared_savings_amount, 2),
                'organization_retention': round(shared_savings_amount, 2),
                'medicare_savings': round(gross_savings - shared_savings_amount, 2)
            },
            'performance_summary': {
                'cost_performance': 'exceeds_benchmark' if gross_savings > 0 else 'above_benchmark',
                'quality_performance': quality_performance['performance_tier'],
                'overall_program_success': meets_minimum and meets_quality_threshold
            }
        }
    
    def _assess_quality_performance(self, quality_scores: Dict) -> Dict:
        """Assess quality performance for shared savings eligibility."""
        # Weight different quality domains
        quality_weights = {
            'patient_safety': 0.30,
            'care_coordination': 0.25,
            'patient_experience': 0.25,
            'preventive_health': 0.20
        }
        
        weighted_score = 0
        domain_scores = {}
        
        for domain, weight in quality_weights.items():
            domain_score = quality_scores.get(domain, 0)
            weighted_score += domain_score * weight
            domain_scores[domain] = domain_score
        
        # Determine performance tier
        if weighted_score >= 0.90:
            tier = 'exceptional'
        elif weighted_score >= 0.75:
            tier = 'high'
        elif weighted_score >= 0.60:
            tier = 'satisfactory'
        else:
            tier = 'needs_improvement'
        
        return {
            'overall_score': round(weighted_score, 3),
            'domain_scores': domain_scores,
            'performance_tier': tier,
            'quality_bonus_eligible': weighted_score >= self.medicare_benchmarks['quality_bonus_threshold']
        }
    
    def model_financial_reserves(self, contract_data: Dict) -> Dict:
        """
        Model financial reserves and risk corridors for VBC contracts.
        
        Args:
            contract_data: Contract terms and financial projections
            
        Returns:
            Reserve requirements and risk modeling
        """
        annual_revenue = contract_data['annual_capitation_revenue']
        projected_medical_costs = contract_data['projected_medical_costs']
        
        # Calculate medical loss ratio
        medical_loss_ratio = projected_medical_costs / annual_revenue
        
        # IBNR (Incurred But Not Reported) reserves
        ibnr_reserve = projected_medical_costs * self.reserve_requirements['ibnr_reserve_rate']
        
        # Risk corridor calculations
        target_mlr = 0.85  # Target medical loss ratio
        corridor_upper = target_mlr + self.reserve_requirements['risk_corridor_upper']
        corridor_lower = target_mlr + self.reserve_requirements['risk_corridor_lower']
        
        # Calculate risk exposure
        if medical_loss_ratio > corridor_upper:
            risk_exposure = (medical_loss_ratio - corridor_upper) * annual_revenue
            risk_level = 'high'
        elif medical_loss_ratio < corridor_lower:
            risk_exposure = (corridor_lower - medical_loss_ratio) * annual_revenue
            risk_level = 'favorable'
        else:
            risk_exposure = 0
            risk_level = 'within_corridor'
        
        # Total reserve requirement
        minimum_reserves = annual_revenue * 0.05  # 5% minimum
        recommended_reserves = max(minimum_reserves, ibnr_reserve + abs(risk_exposure))
        
        # Trend projections
        trend_factor = self.reserve_requirements['trend_factor_annual']
        next_year_costs = projected_medical_costs * (1 + trend_factor)
        trend_impact = next_year_costs - projected_medical_costs
        
        return {
            'current_performance': {
                'medical_loss_ratio': round(medical_loss_ratio, 3),
                'target_mlr': target_mlr,
                'performance_vs_target': round((medical_loss_ratio - target_mlr) * 100, 1)
            },
            'risk_corridor_analysis': {
                'corridor_upper_limit': round(corridor_upper, 3),
                'corridor_lower_limit': round(corridor_lower, 3),
                'current_position': risk_level,
                'risk_exposure': round(risk_exposure, 2),
                'within_corridor': corridor_lower <= medical_loss_ratio <= corridor_upper
            },
            'reserve_requirements': {
                'ibnr_reserve': round(ibnr_reserve, 2),
                'minimum_reserves': round(minimum_reserves, 2),
                'recommended_reserves': round(recommended_reserves, 2),
                'reserve_as_percent_revenue': round(recommended_reserves / annual_revenue * 100, 1)
            },
            'trend_projections': {
                'annual_trend_factor': trend_factor * 100,
                'current_year_costs': projected_medical_costs,
                'next_year_projected_costs': round(next_year_costs, 2),
                'trend_impact': round(trend_impact, 2)
            },
            'financial_stability': {
                'liquidity_adequate': recommended_reserves <= annual_revenue * 0.15,
                'risk_manageable': abs(risk_exposure) <= annual_revenue * 0.05,
                'trend_sustainable': trend_impact <= annual_revenue * 0.02
            }
        }
    
    def optimize_contract_performance(self, current_performance: Dict) -> Dict:
        """
        Generate recommendations for optimizing VBC contract performance.
        
        Args:
            current_performance: Current contract performance metrics
            
        Returns:
            Optimization recommendations and financial projections
        """
        recommendations = []
        potential_savings = 0
        
        # Cost optimization opportunities
        medical_costs = current_performance.get('medical_costs', {})
        
        # ED utilization optimization
        ed_rate = medical_costs.get('ed_visits_per_1000', 0)
        if ed_rate > 250:
            ed_savings = (ed_rate - 250) * current_performance.get('panel_size', 1000) / 1000 * 500
            recommendations.append({
                'category': 'Utilization Management',
                'opportunity': 'Emergency Department Visit Reduction',
                'current_performance': f"{ed_rate} visits per 1000 members",
                'target': '250 visits per 1000 members',
                'estimated_savings': round(ed_savings, 2),
                'implementation': 'After-hours clinic, urgent care partnerships, patient education'
            })
            potential_savings += ed_savings
        
        # Readmission rate optimization
        readmit_rate = medical_costs.get('readmission_rate', 0)
        if readmit_rate > 12:
            readmit_savings = (readmit_rate - 12) * 0.01 * current_performance.get('panel_size', 1000) * 15000
            recommendations.append({
                'category': 'Care Transitions',
                'opportunity': 'Readmission Rate Reduction',
                'current_performance': f"{readmit_rate}% readmission rate",
                'target': '12% readmission rate',
                'estimated_savings': round(readmit_savings, 2),
                'implementation': 'Enhanced discharge planning, 72-hour follow-up calls, TCM programs'
            })
            potential_savings += readmit_savings
        
        # Generic prescribing optimization
        generic_rate = medical_costs.get('generic_prescribing_rate', 0)
        if generic_rate < 85:
            pharmacy_savings = (85 - generic_rate) * 0.01 * current_performance.get('pharmacy_costs', 500000) * 0.3
            recommendations.append({
                'category': 'Pharmacy Management',
                'opportunity': 'Generic Prescribing Rate Improvement',
                'current_performance': f"{generic_rate}% generic rate",
                'target': '85% generic rate',
                'estimated_savings': round(pharmacy_savings, 2),
                'implementation': 'Provider education, EHR decision support, formulary management'
            })
            potential_savings += pharmacy_savings
        
        # Quality bonus opportunities
        quality_score = current_performance.get('quality_score', 0)
        if quality_score < 0.75:
            quality_bonus = current_performance.get('benchmark_revenue', 10000000) * 0.02
            recommendations.append({
                'category': 'Quality Improvement',
                'opportunity': 'Quality Bonus Achievement',
                'current_performance': f"{quality_score:.2f} quality score",
                'target': '0.75 quality score',
                'estimated_savings': round(quality_bonus, 2),
                'implementation': 'Care gap closure, preventive care campaigns, provider training'
            })
            potential_savings += quality_bonus
        
        # Risk adjustment optimization
        risk_score = current_performance.get('average_risk_score', 1.0)
        if risk_score < 1.2:  # Potentially under-coded
            risk_adjustment_opportunity = current_performance.get('panel_size', 1000) * 850 * 12 * 0.1
            recommendations.append({
                'category': 'Risk Adjustment',
                'opportunity': 'HCC Coding Optimization',
                'current_performance': f"{risk_score:.2f} average risk score",
                'target': 'Accurate risk score capture',
                'estimated_savings': round(risk_adjustment_opportunity, 2),
                'implementation': 'Provider coding education, HCC documentation, annual wellness visits'
            })
            potential_savings += risk_adjustment_opportunity
        
        # Calculate ROI for top opportunities
        top_opportunities = sorted(recommendations, key=lambda x: x['estimated_savings'], reverse=True)[:3]
        implementation_cost = potential_savings * 0.15  # Assume 15% implementation cost
        net_savings = potential_savings - implementation_cost
        roi = (net_savings / implementation_cost * 100) if implementation_cost > 0 else 0
        
        return {
            'optimization_summary': {
                'total_opportunities': len(recommendations),
                'potential_annual_savings': round(potential_savings, 2),
                'estimated_implementation_cost': round(implementation_cost, 2),
                'net_savings': round(net_savings, 2),
                'roi_percentage': round(roi, 1)
            },
            'top_opportunities': top_opportunities,
            'all_recommendations': recommendations,
            'implementation_timeline': {
                'immediate_0_3_months': [r for r in recommendations if r['category'] in ['Pharmacy Management', 'Risk Adjustment']],
                'short_term_3_6_months': [r for r in recommendations if r['category'] in ['Quality Improvement']],
                'medium_term_6_12_months': [r for r in recommendations if r['category'] in ['Utilization Management', 'Care Transitions']]
            }
        }

# Example usage and demonstration
if __name__ == "__main__":
    # Create sample patient panel for actuarial analysis
    np.random.seed(42)
    
    sample_panel = []
    for i in range(1000):
        # Generate realistic patient demographics and conditions
        age = max(65, int(np.random.normal(75, 8)))
        
        # HCC conditions (realistic prevalence)
        hcc_conditions = []
        if np.random.random() < 0.25:  # 25% have diabetes
            hcc_conditions.append('17_diabetes_complications' if np.random.random() < 0.3 else '18_diabetes_no_complications')
        if np.random.random() < 0.15:  # 15% have heart failure
            hcc_conditions.append('85_heart_failure')
        if np.random.random() < 0.20:  # 20% have COPD
            hcc_conditions.append('108_copd')
        if np.random.random() < 0.10:  # 10% have kidney disease
            hcc_conditions.append('135_chronic_kidney_disease')
        
        patient = {
            'patient_id': f'ACT_{i+1:04d}',
            'age': age,
            'gender': np.random.choice(['male', 'female']),
            'medicaid_dual': np.random.choice([True, False], p=[0.20, 0.80]),
            'disability_status': np.random.choice([True, False], p=[0.15, 0.85]),
            'hcc_conditions': hcc_conditions
        }
        sample_panel.append(patient)
    
    panel_df = pd.DataFrame(sample_panel)
    
    # Initialize actuarial engine
    actuarial_engine = ActuarialEngine()
    
    print("💰 Actuarial Modeling Demo")
    print("=" * 55)
    
    # Calculate risk adjustment
    risk_adjustment = actuarial_engine.calculate_risk_adjustment(panel_df)
    
    print(f"\n📊 Risk Adjustment Analysis:")
    panel_metrics = risk_adjustment['panel_metrics']
    print(f"Panel Size: {panel_metrics['panel_size']:,} patients")
    print(f"Average Risk Score: {panel_metrics['average_risk_score']}")
    print(f"Risk-Adjusted PMPM: ${panel_metrics['risk_adjusted_pmpm']:,}")
    
    financial_impact = risk_adjustment['financial_impact']
    print(f"Annual Risk Adjustment: ${financial_impact['annual_risk_adjustment']:,}")
    print(f"Risk Adjustment %: {financial_impact['risk_adjustment_percentage']}%")
    
    # Sample shared savings calculation
    actual_costs = {
        'total_medical_costs': 8500000  # $8.5M actual costs
    }
    benchmark_costs = {
        'total_benchmark_costs': 9200000  # $9.2M benchmark
    }
    quality_scores = {
        'patient_safety': 0.82,
        'care_coordination': 0.78,
        'patient_experience': 0.75,
        'preventive_health': 0.85
    }
    
    shared_savings = actuarial_engine.calculate_shared_savings(
        actual_costs, benchmark_costs, quality_scores
    )
    
    print(f"\n💰 Shared Savings Analysis:")
    savings_calc = shared_savings['savings_calculation']
    print(f"Benchmark Costs: ${savings_calc['total_benchmark_costs']:,}")
    print(f"Actual Costs: ${savings_calc['total_actual_costs']:,}")
    print(f"Gross Savings: ${savings_calc['gross_savings']:,} ({savings_calc['gross_savings_rate']}%)")
    
    sharing_results = shared_savings['shared_savings_results']
    print(f"Shared Savings Amount: ${sharing_results['shared_savings_amount']:,}")
    print(f"Sharing Rate: {sharing_results['sharing_rate']}%")
    print(f"Quality Performance: {shared_savings['quality_assessment']['performance_tier']}")
    
    # Sample financial reserves modeling
    contract_data = {
        'annual_capitation_revenue': 10200000,  # $10.2M revenue
        'projected_medical_costs': 8500000     # $8.5M costs
    }
    
    reserves = actuarial_engine.model_financial_reserves(contract_data)
    
    print(f"\n🏦 Financial Reserves Analysis:")
    current_perf = reserves['current_performance']
    print(f"Medical Loss Ratio: {current_perf['medical_loss_ratio']:.1%}")
    print(f"Performance vs Target: {current_perf['performance_vs_target']}% points")
    
    reserve_req = reserves['reserve_requirements']
    print(f"Recommended Reserves: ${reserve_req['recommended_reserves']:,}")
    print(f"Reserve % of Revenue: {reserve_req['reserve_as_percent_revenue']}%")
    
    print("\n" + "=" * 55)
    print("Actuarial Modeling Demo Complete! 🎉")
    print("This demonstrates financial modeling")
    print("for value-based care contract optimization.")
