"""
📊 Quality Measures Tracking System for Value-Based Care

This module implements HEDIS, CMS Star Ratings, and other quality measure
calculations essential for value-based care contracts.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class QualityMeasureTracker:
    """
    Comprehensive quality measures tracking and calculation system
    for healthcare organizations in value-based care contracts.
    """
    
    def __init__(self):
        self.hedis_measures = {
            'HbA1c-9': {
                'name': 'Diabetes: HbA1c Poor Control',
                'description': 'Percentage of patients with diabetes with HbA1c >9%',
                'target': 'Lower is better',
                'benchmark': 23.5
            },
            'CBP': {
                'name': 'Controlling High Blood Pressure',
                'description': 'Percentage of patients with controlled blood pressure',
                'target': 'Higher is better',
                'benchmark': 70.2
            },
            'BCS': {
                'name': 'Breast Cancer Screening',
                'description': 'Percentage of women screened for breast cancer',
                'target': 'Higher is better',
                'benchmark': 75.4
            },
            'CCS': {
                'name': 'Cervical Cancer Screening',
                'description': 'Percentage of women screened for cervical cancer',
                'target': 'Higher is better',
                'benchmark': 80.1
            },
            'COL': {
                'name': 'Colorectal Cancer Screening',
                'description': 'Percentage of patients screened for colorectal cancer',
                'target': 'Higher is better',
                'benchmark': 72.8
            }
        }
        
        self.cms_measures = {
            'AWC': {
                'name': 'Annual Wellness Visits',
                'description': 'Percentage of Medicare patients with annual wellness visit',
                'target': 'Higher is better',
                'benchmark': 65.0
            },
            'PCR': {
                'name': 'Plan All-Cause Readmissions',
                'description': 'Percentage of unplanned readmissions within 30 days',
                'target': 'Lower is better',
                'benchmark': 14.2
            },
            'HOS': {
                'name': 'Health Outcomes Survey',
                'description': 'Patient-reported health outcomes and functional status',
                'target': 'Higher is better',
                'benchmark': 75.0
            }
        }
    
    def calculate_hedis_measure(self, measure_code, numerator, denominator):
        """
        Calculate HEDIS measure performance and quality score
        
        Args:
            measure_code (str): HEDIS measure code
            numerator (int): Number of patients meeting criteria
            denominator (int): Total eligible patients
            
        Returns:
            dict: Calculated measure performance and scoring
        """
        if denominator == 0:
            return {
                'measure_code': measure_code,
                'performance_rate': 0,
                'quality_score': 0,
                'benchmark_comparison': 'No eligible patients',
                'star_rating': 1
            }
        
        performance_rate = (numerator / denominator) * 100
        measure_info = self.hedis_measures.get(measure_code, {})
        benchmark = measure_info.get('benchmark', 50)
        target_direction = measure_info.get('target', 'Higher is better')
        
        # Calculate quality score (0-100 scale)
        if target_direction == 'Higher is better':
            if performance_rate >= benchmark:
                quality_score = 85 + (performance_rate - benchmark) / benchmark * 15
            else:
                quality_score = (performance_rate / benchmark) * 85
        else:  # Lower is better
            if performance_rate <= benchmark:
                quality_score = 85 + (benchmark - performance_rate) / benchmark * 15
            else:
                quality_score = max(0, 85 - (performance_rate - benchmark) / benchmark * 40)
        
        quality_score = min(100, max(0, quality_score))
        
        # Calculate star rating (1-5 stars)
        if quality_score >= 95:
            star_rating = 5
        elif quality_score >= 85:
            star_rating = 4
        elif quality_score >= 75:
            star_rating = 3
        elif quality_score >= 60:
            star_rating = 2
        else:
            star_rating = 1
        
        # Benchmark comparison
        if target_direction == 'Higher is better':
            comparison = 'Above benchmark' if performance_rate > benchmark else 'Below benchmark'
        else:
            comparison = 'Above benchmark' if performance_rate < benchmark else 'Below benchmark'
        
        return {
            'measure_code': measure_code,
            'measure_name': measure_info.get('name', 'Unknown Measure'),
            'numerator': numerator,
            'denominator': denominator,
            'performance_rate': round(performance_rate, 2),
            'benchmark_rate': benchmark,
            'quality_score': round(quality_score, 1),
            'star_rating': star_rating,
            'benchmark_comparison': comparison,
            'gap_to_benchmark': round(performance_rate - benchmark, 2)
        }
    
    def calculate_provider_scorecard(self, provider_measures_df):
        """
        Calculate comprehensive provider scorecard
        
        Args:
            provider_measures_df (DataFrame): Provider quality measures data
            
        Returns:
            dict: Provider performance scorecard
        """
        total_measures = len(provider_measures_df)
        avg_quality_score = provider_measures_df['quality_score'].mean()
        avg_star_rating = provider_measures_df['star_rating'].mean()
        
        measures_above_benchmark = (
            provider_measures_df['performance_rate'] > provider_measures_df['benchmark_rate']
        ).sum()
        
        percentage_above_benchmark = (measures_above_benchmark / total_measures) * 100
        
        # Calculate weighted score by measure importance
        high_priority_measures = ['HbA1c-9', 'CBP', 'PCR', 'AWC']
        priority_scores = []
        
        for _, measure in provider_measures_df.iterrows():
            weight = 2.0 if measure['measure_code'] in high_priority_measures else 1.0
            priority_scores.extend([measure['quality_score']] * int(weight))
        
        weighted_avg_score = np.mean(priority_scores)
        
        # Performance tier
        if weighted_avg_score >= 90:
            performance_tier = 'Excellent'
        elif weighted_avg_score >= 80:
            performance_tier = 'Good'
        elif weighted_avg_score >= 70:
            performance_tier = 'Satisfactory'
        else:
            performance_tier = 'Needs Improvement'
        
        return {
            'total_measures': total_measures,
            'avg_quality_score': round(avg_quality_score, 1),
            'avg_star_rating': round(avg_star_rating, 1),
            'measures_above_benchmark': measures_above_benchmark,
            'percentage_above_benchmark': round(percentage_above_benchmark, 1),
            'weighted_avg_score': round(weighted_avg_score, 1),
            'performance_tier': performance_tier
        }
    
    def identify_quality_gaps(self, measures_df):
        """
        Identify quality improvement opportunities
        
        Args:
            measures_df (DataFrame): Quality measures data
            
        Returns:
            DataFrame: Prioritized quality improvement opportunities
        """
        gaps_df = measures_df.copy()
        
        # Calculate improvement potential
        gaps_df['care_gap_count'] = gaps_df['denominator'] - gaps_df['numerator']
        gaps_df['improvement_potential'] = (
            gaps_df['care_gap_count'] / gaps_df['denominator'] * 100
        )
        
        # Calculate priority score
        gaps_df['benchmark_gap'] = abs(gaps_df['performance_rate'] - gaps_df['benchmark_rate'])
        gaps_df['priority_score'] = (
            gaps_df['care_gap_count'] * 0.4 +  # Volume weight
            gaps_df['improvement_potential'] * 0.3 +  # Potential impact
            gaps_df['benchmark_gap'] * 0.3  # Performance gap
        )
        
        # Add recommendations
        recommendations = []
        for _, row in gaps_df.iterrows():
            if row['care_gap_count'] > 10:
                if 'Diabetes' in row['measure_name']:
                    rec = "Implement diabetes care management program with regular HbA1c monitoring"
                elif 'Blood Pressure' in row['measure_name']:
                    rec = "Deploy home blood pressure monitoring and medication adherence program"
                elif 'Cancer Screening' in row['measure_name']:
                    rec = "Automated screening reminders and patient outreach campaigns"
                elif 'Wellness' in row['measure_name']:
                    rec = "Enhanced care coordination and patient engagement initiatives"
                else:
                    rec = "Targeted intervention program with care coordinator support"
            else:
                rec = "Monitor and provide individualized patient outreach"
            
            recommendations.append(rec)
        
        gaps_df['recommendation'] = recommendations
        
        return gaps_df.sort_values('priority_score', ascending=False)
    
    def calculate_quality_bonus(self, quality_scores, base_payment, bonus_structure):
        """
        Calculate quality bonus payments based on performance
        
        Args:
            quality_scores (list): List of quality scores
            base_payment (float): Base payment amount
            bonus_structure (dict): Bonus payment structure
            
        Returns:
            dict: Quality bonus calculation details
        """
        avg_quality_score = np.mean(quality_scores)
        
        # Default bonus structure if not provided
        if not bonus_structure:
            bonus_structure = {
                95: 0.05,  # 5% bonus for 95+ score
                90: 0.03,  # 3% bonus for 90+ score
                85: 0.02,  # 2% bonus for 85+ score
                80: 0.01   # 1% bonus for 80+ score
            }
        
        bonus_percentage = 0
        bonus_tier = 'No Bonus'
        
        for threshold, percentage in sorted(bonus_structure.items(), reverse=True):
            if avg_quality_score >= threshold:
                bonus_percentage = percentage
                bonus_tier = f'{threshold}+ Performance Tier'
                break
        
        bonus_amount = base_payment * bonus_percentage
        
        return {
            'avg_quality_score': round(avg_quality_score, 1),
            'bonus_percentage': bonus_percentage * 100,
            'bonus_tier': bonus_tier,
            'bonus_amount': bonus_amount,
            'total_payment': base_payment + bonus_amount
        }
    
    def generate_quality_report(self, provider_id, measures_df, financial_data=None):
        """
        Generate comprehensive quality performance report
        
        Args:
            provider_id (str): Provider identifier
            measures_df (DataFrame): Quality measures data
            financial_data (dict): Financial performance data
            
        Returns:
            dict: Comprehensive quality report
        """
        # Calculate scorecard
        scorecard = self.calculate_provider_scorecard(measures_df)
        
        # Identify gaps
        quality_gaps = self.identify_quality_gaps(measures_df)
        top_gaps = quality_gaps.head(5)
        
        # Performance trends (simulated for demo)
        trend_data = {
            'current_quarter': scorecard['avg_quality_score'],
            'previous_quarter': scorecard['avg_quality_score'] - np.random.uniform(-5, 5),
            'year_over_year': scorecard['avg_quality_score'] - np.random.uniform(-10, 10)
        }
        
        # Quality bonus calculation
        quality_bonus = None
        if financial_data:
            quality_bonus = self.calculate_quality_bonus(
                measures_df['quality_score'].tolist(),
                financial_data.get('base_payment', 100000),
                financial_data.get('bonus_structure', {})
            )
        
        report = {
            'provider_id': provider_id,
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'performance_summary': scorecard,
            'quality_trends': trend_data,
            'top_quality_gaps': top_gaps[['measure_name', 'care_gap_count', 
                                         'improvement_potential', 'recommendation']].to_dict('records'),
            'quality_bonus': quality_bonus,
            'recommendations': self._generate_action_plan(scorecard, top_gaps)
        }
        
        return report
    
    def _generate_action_plan(self, scorecard, quality_gaps):
        """Generate action plan based on performance"""
        action_plan = []
        
        if scorecard['performance_tier'] == 'Needs Improvement':
            action_plan.append("Priority: Implement comprehensive quality improvement program")
            action_plan.append("Focus on top 3 quality gaps with highest volume")
            action_plan.append("Assign dedicated care coordinator for high-risk patients")
        
        elif scorecard['performance_tier'] == 'Satisfactory':
            action_plan.append("Focus on measures below benchmark")
            action_plan.append("Implement targeted interventions for care gaps")
            action_plan.append("Enhance patient engagement strategies")
        
        elif scorecard['performance_tier'] in ['Good', 'Excellent']:
            action_plan.append("Maintain current performance levels")
            action_plan.append("Share best practices with other providers")
            action_plan.append("Focus on achieving 5-star ratings on all measures")
        
        # Add specific recommendations based on gaps
        for _, gap in quality_gaps.head(3).iterrows():
            action_plan.append(f"Target: {gap['measure_name']} - {gap['recommendation']}")
        
        return action_plan

# Example usage and demonstration
if __name__ == "__main__":
    # Initialize quality tracker
    tracker = QualityMeasureTracker()
    
    print("📊 Quality Measures Tracking System")
    print("=" * 50)
    
    # Sample quality measures data
    sample_measures = [
        {'measure_code': 'HbA1c-9', 'numerator': 8, 'denominator': 35},
        {'measure_code': 'CBP', 'numerator': 42, 'denominator': 58},
        {'measure_code': 'BCS', 'numerator': 22, 'denominator': 28},
        {'measure_code': 'AWC', 'numerator': 45, 'denominator': 65}
    ]
    
    # Calculate measures
    calculated_measures = []
    for measure in sample_measures:
        result = tracker.calculate_hedis_measure(
            measure['measure_code'],
            measure['numerator'],
            measure['denominator']
        )
        calculated_measures.append(result)
        
        print(f"✅ {result['measure_name']}")
        print(f"   📊 Performance: {result['performance_rate']}% (Benchmark: {result['benchmark_rate']}%)")
        print(f"   ⭐ Quality Score: {result['quality_score']}% ({result['star_rating']} stars)")
        print(f"   📈 Status: {result['benchmark_comparison']}")
        print()
    
    # Generate provider scorecard
    measures_df = pd.DataFrame(calculated_measures)
    scorecard = tracker.calculate_provider_scorecard(measures_df)
    
    print(f"🏆 Provider Performance Scorecard")
    print(f"   📊 Average Quality Score: {scorecard['avg_quality_score']}%")
    print(f"   ⭐ Average Star Rating: {scorecard['avg_star_rating']}")
    print(f"   🎯 Performance Tier: {scorecard['performance_tier']}")
    print(f"   📈 Measures Above Benchmark: {scorecard['measures_above_benchmark']}/{scorecard['total_measures']}")
    
    # Calculate quality bonus
    financial_data = {'base_payment': 100000}
    bonus = tracker.calculate_quality_bonus(
        measures_df['quality_score'].tolist(),
        financial_data['base_payment'],
        {}
    )
    
    print(f"\\n💰 Quality Bonus Calculation")
    print(f"   🎯 Average Score: {bonus['avg_quality_score']}%")
    print(f"   💵 Bonus Percentage: {bonus['bonus_percentage']}%")
    print(f"   💰 Bonus Amount: ${bonus['bonus_amount']:,.0f}")
    print(f"   💳 Total Payment: ${bonus['total_payment']:,.0f}")