"""
Provider Performance Scorecards & Benchmarking
==============================================

Pearl Health-style provider performance analytics with peer benchmarking,
quality metrics tracking, and performance improvement recommendations.

Key Features:
- Provider-level quality and cost metrics
- Peer benchmarking and percentile rankings
- Value-based care performance tracking
- Actionable improvement recommendations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class ProviderScorecardEngine:
    """
    Pearl Health-style provider performance tracking and benchmarking system.
    
    Generates comprehensive provider scorecards with quality metrics,
    cost performance, and peer comparisons for value-based care optimization.
    """
    
    def __init__(self):
        # Quality measures aligned with CMS and HEDIS
        self.quality_measures = {
            'preventive_care': {
                'colorectal_screening': {'target': 80, 'weight': 0.15},
                'breast_cancer_screening': {'target': 85, 'weight': 0.15},
                'cervical_cancer_screening': {'target': 85, 'weight': 0.10},
                'annual_wellness_visits': {'target': 70, 'weight': 0.20},
                'diabetes_eye_exam': {'target': 75, 'weight': 0.10},
                'blood_pressure_control': {'target': 70, 'weight': 0.15},
                'diabetes_control': {'target': 65, 'weight': 0.15}
            },
            'care_coordination': {
                'post_discharge_followup': {'target': 85, 'weight': 0.25},
                'medication_reconciliation': {'target': 90, 'weight': 0.20},
                'care_plan_documentation': {'target': 80, 'weight': 0.15},
                'specialist_communication': {'target': 75, 'weight': 0.20},
                'patient_portal_engagement': {'target': 60, 'weight': 0.20}
            },
            'patient_experience': {
                'patient_satisfaction': {'target': 4.2, 'weight': 0.30},
                'access_to_care': {'target': 4.0, 'weight': 0.25},
                'communication_rating': {'target': 4.3, 'weight': 0.25},
                'care_coordination_rating': {'target': 4.1, 'weight': 0.20}
            }
        }
        
        # Cost and utilization benchmarks
        self.cost_benchmarks = {
            'total_cost_per_patient': {'target': 8500, 'direction': 'lower'},
            'ed_visits_per_1000': {'target': 250, 'direction': 'lower'},
            'readmission_rate': {'target': 12, 'direction': 'lower'},
            'specialist_referral_rate': {'target': 35, 'direction': 'lower'},
            'generic_prescribing_rate': {'target': 85, 'direction': 'higher'},
            'preventable_hospitalization_rate': {'target': 8, 'direction': 'lower'}
        }
        
        # Performance tier thresholds (percentiles)
        self.performance_tiers = {
            'top_performer': 90,      # Top 10%
            'high_performer': 75,     # Top 25%
            'average_performer': 25,  # Middle 50%
            'needs_improvement': 0    # Bottom 25%
        }
    
    def calculate_quality_score(self, provider_metrics: Dict) -> Dict:
        """
        Calculate comprehensive quality score using Pearl Health methodology.
        
        Args:
            provider_metrics: Dictionary containing provider's quality metrics
            
        Returns:
            Dictionary with quality scores and component breakdowns
        """
        category_scores = {}
        
        for category, measures in self.quality_measures.items():
            category_score = 0
            total_weight = 0
            measure_details = {}
            
            for measure, config in measures.items():
                actual_value = provider_metrics.get(measure, 0)
                target_value = config['target']
                weight = config['weight']
                
                # Calculate measure score (0-100)
                if category == 'patient_experience':
                    # For experience scores (1-5 scale), convert to percentage
                    measure_score = min((actual_value / target_value) * 100, 100)
                else:
                    # For percentage-based measures
                    measure_score = min((actual_value / target_value) * 100, 100)
                
                category_score += measure_score * weight
                total_weight += weight
                
                measure_details[measure] = {
                    'actual': actual_value,
                    'target': target_value,
                    'score': round(measure_score, 1),
                    'weight': weight,
                    'gap': round(target_value - actual_value, 1) if actual_value < target_value else 0
                }
            
            category_scores[category] = {
                'score': round(category_score / total_weight if total_weight > 0 else 0, 1),
                'measures': measure_details
            }
        
        # Calculate overall quality score (weighted average)
        overall_score = (
            category_scores['preventive_care']['score'] * 0.4 +
            category_scores['care_coordination']['score'] * 0.35 +
            category_scores['patient_experience']['score'] * 0.25
        )
        
        return {
            'overall_quality_score': round(overall_score, 1),
            'category_scores': category_scores,
            'quality_tier': self._determine_performance_tier(overall_score)
        }
    
    def calculate_cost_performance(self, provider_metrics: Dict) -> Dict:
        """
        Calculate cost and utilization performance vs benchmarks.
        
        Args:
            provider_metrics: Dictionary containing provider's cost and utilization data
            
        Returns:
            Dictionary with cost performance scores and analysis
        """
        cost_performance = {}
        performance_scores = []
        
        for metric, config in self.cost_benchmarks.items():
            actual_value = provider_metrics.get(metric, 0)
            target_value = config['target']
            direction = config['direction']
            
            # Calculate performance score
            if direction == 'lower':
                # Lower is better (costs, utilization)
                if actual_value <= target_value:
                    score = 100
                else:
                    # Penalize based on how much over target
                    score = max(100 - ((actual_value - target_value) / target_value * 100), 0)
            else:
                # Higher is better (generic prescribing)
                if actual_value >= target_value:
                    score = 100
                else:
                    score = (actual_value / target_value) * 100
            
            cost_performance[metric] = {
                'actual': actual_value,
                'target': target_value,
                'score': round(score, 1),
                'performance': 'meets_target' if score >= 95 else 'needs_improvement',
                'variance_from_target': round(((actual_value - target_value) / target_value * 100), 1)
            }
            
            performance_scores.append(score)
        
        overall_cost_score = np.mean(performance_scores)
        
        return {
            'overall_cost_score': round(overall_cost_score, 1),
            'metric_performance': cost_performance,
            'cost_tier': self._determine_performance_tier(overall_cost_score),
            'cost_savings_opportunity': self._calculate_savings_opportunity(provider_metrics)
        }
    
    def generate_provider_scorecard(self, provider_data: Dict, peer_benchmarks: Dict) -> Dict:
        """
        Generate comprehensive provider scorecard with benchmarking.
        
        Args:
            provider_data: Complete provider performance data
            peer_benchmarks: Peer group performance statistics
            
        Returns:
            Complete provider scorecard with scores, rankings, and recommendations
        """
        # Calculate core performance scores
        quality_analysis = self.calculate_quality_score(provider_data)
        cost_analysis = self.calculate_cost_performance(provider_data)
        
        # Calculate peer rankings
        peer_rankings = self._calculate_peer_rankings(provider_data, peer_benchmarks)
        
        # Generate improvement recommendations
        recommendations = self._generate_improvement_recommendations(
            quality_analysis, cost_analysis, peer_rankings
        )
        
        # Calculate overall VBC performance score
        vbc_score = (quality_analysis['overall_quality_score'] * 0.6 + 
                    cost_analysis['overall_cost_score'] * 0.4)
        
        scorecard = {
            'provider_info': {
                'provider_id': provider_data.get('provider_id'),
                'provider_name': provider_data.get('provider_name'),
                'specialty': provider_data.get('specialty', 'Primary Care'),
                'panel_size': provider_data.get('panel_size', 0),
                'reporting_period': provider_data.get('reporting_period', 'Q4 2024')
            },
            'overall_performance': {
                'vbc_composite_score': round(vbc_score, 1),
                'performance_tier': self._determine_performance_tier(vbc_score),
                'peer_percentile': peer_rankings.get('overall_percentile', 50)
            },
            'quality_performance': quality_analysis,
            'cost_performance': cost_analysis,
            'peer_benchmarking': peer_rankings,
            'improvement_opportunities': recommendations,
            'key_metrics_summary': self._create_metrics_summary(provider_data, peer_benchmarks),
            'action_items': self._prioritize_action_items(recommendations)
        }
        
        return scorecard
    
    def _determine_performance_tier(self, score: float) -> str:
        """Determine performance tier based on score."""
        if score >= 90:
            return 'top_performer'
        elif score >= 75:
            return 'high_performer'
        elif score >= 50:
            return 'average_performer'
        else:
            return 'needs_improvement'
    
    def _calculate_peer_rankings(self, provider_data: Dict, peer_benchmarks: Dict) -> Dict:
        """Calculate provider's percentile rankings vs peers."""
        rankings = {}
        
        # Quality measure rankings
        for measure in ['overall_quality_score', 'preventive_care_score', 'care_coordination_score']:
            provider_value = provider_data.get(measure, 0)
            peer_values = peer_benchmarks.get(f'{measure}_distribution', [])
            
            if peer_values:
                percentile = np.percentile(peer_values, 
                                        sum(1 for x in peer_values if x <= provider_value) / len(peer_values) * 100)
                rankings[f'{measure}_percentile'] = round(percentile, 1)
        
        # Cost measure rankings
        for measure in ['total_cost_per_patient', 'ed_visits_per_1000', 'readmission_rate']:
            provider_value = provider_data.get(measure, 0)
            peer_values = peer_benchmarks.get(f'{measure}_distribution', [])
            
            if peer_values:
                # For cost measures, lower is better, so invert percentile
                percentile = 100 - np.percentile(peer_values, 
                                               sum(1 for x in peer_values if x <= provider_value) / len(peer_values) * 100)
                rankings[f'{measure}_percentile'] = round(percentile, 1)
        
        # Overall percentile (composite)
        quality_pct = rankings.get('overall_quality_score_percentile', 50)
        cost_pct = rankings.get('total_cost_per_patient_percentile', 50)
        rankings['overall_percentile'] = round((quality_pct * 0.6 + cost_pct * 0.4), 1)
        
        return rankings
    
    def _calculate_savings_opportunity(self, provider_metrics: Dict) -> Dict:
        """Calculate potential cost savings opportunities."""
        savings_opportunities = {}
        
        # ED visit reduction opportunity
        actual_ed_rate = provider_metrics.get('ed_visits_per_1000', 0)
        target_ed_rate = self.cost_benchmarks['ed_visits_per_1000']['target']
        if actual_ed_rate > target_ed_rate:
            ed_reduction = actual_ed_rate - target_ed_rate
            savings_opportunities['ed_visit_reduction'] = {
                'excess_visits_per_1000': ed_reduction,
                'potential_annual_savings': round(ed_reduction * 500, 0)  # $500 avg savings per avoided ED visit
            }
        
        # Readmission reduction opportunity
        actual_readmit_rate = provider_metrics.get('readmission_rate', 0)
        target_readmit_rate = self.cost_benchmarks['readmission_rate']['target']
        if actual_readmit_rate > target_readmit_rate:
            readmit_reduction = actual_readmit_rate - target_readmit_rate
            savings_opportunities['readmission_reduction'] = {
                'excess_readmission_rate': readmit_reduction,
                'potential_annual_savings': round(readmit_reduction * 0.01 * provider_metrics.get('panel_size', 1000) * 12000, 0)
            }
        
        total_opportunity = sum(opp.get('potential_annual_savings', 0) for opp in savings_opportunities.values())
        savings_opportunities['total_annual_opportunity'] = total_opportunity
        
        return savings_opportunities
    
    def _generate_improvement_recommendations(self, quality_analysis: Dict, cost_analysis: Dict, peer_rankings: Dict) -> List[Dict]:
        """Generate specific improvement recommendations based on performance gaps."""
        recommendations = []
        
        # Quality improvement recommendations
        for category, data in quality_analysis['category_scores'].items():
            if data['score'] < 75:  # Below target threshold
                for measure, details in data['measures'].items():
                    if details['gap'] > 0:
                        recommendations.append({
                            'category': 'Quality Improvement',
                            'focus_area': measure,
                            'current_performance': details['actual'],
                            'target': details['target'],
                            'gap': details['gap'],
                            'priority': 'High' if details['gap'] > 10 else 'Medium',
                            'recommended_actions': self._get_quality_improvement_actions(measure),
                            'estimated_impact': f"Potential {details['gap']}% improvement"
                        })
        
        # Cost improvement recommendations
        for metric, data in cost_analysis['metric_performance'].items():
            if data['score'] < 80:
                recommendations.append({
                    'category': 'Cost Optimization',
                    'focus_area': metric,
                    'current_performance': data['actual'],
                    'target': data['target'],
                    'variance': data['variance_from_target'],
                    'priority': 'High' if abs(data['variance_from_target']) > 20 else 'Medium',
                    'recommended_actions': self._get_cost_improvement_actions(metric),
                    'estimated_impact': f"Potential ${abs(data['variance_from_target']) * 100:,.0f} annual savings"
                })
        
        # Peer comparison recommendations
        for metric, percentile in peer_rankings.items():
            if percentile < 25 and 'percentile' in metric:
                base_metric = metric.replace('_percentile', '')
                recommendations.append({
                    'category': 'Peer Benchmarking',
                    'focus_area': base_metric,
                    'current_percentile': percentile,
                    'target_percentile': 50,
                    'priority': 'Medium',
                    'recommended_actions': [f"Benchmark against top quartile performers in {base_metric}"],
                    'estimated_impact': f"Move from {percentile}th to 50th percentile"
                })
        
        return sorted(recommendations, key=lambda x: x['priority'] == 'High', reverse=True)[:10]
    
    def _get_quality_improvement_actions(self, measure: str) -> List[str]:
        """Get specific improvement actions for quality measures."""
        action_map = {
            'colorectal_screening': [
                "Implement automated screening reminders in EHR",
                "Patient outreach campaign for overdue screenings",
                "Provider education on screening guidelines"
            ],
            'annual_wellness_visits': [
                "Proactive AWV scheduling for eligible patients",
                "Patient education on AWV benefits",
                "Care coordinator outreach to unscheduled patients"
            ],
            'post_discharge_followup': [
                "Implement TCM protocols for all discharges",
                "Automated post-discharge call program",
                "Care coordinator follow-up within 48 hours"
            ],
            'diabetes_control': [
                "Diabetes self-management education program",
                "Continuous glucose monitoring for high-risk patients",
                "Endocrinology consultation for uncontrolled patients"
            ]
        }
        
        return action_map.get(measure, ["Develop targeted improvement plan", "Regular monitoring and follow-up"])
    
    def _get_cost_improvement_actions(self, metric: str) -> List[str]:
        """Get specific improvement actions for cost metrics."""
        action_map = {
            'ed_visits_per_1000': [
                "After-hours care access improvement",
                "Patient education on appropriate ED use",
                "Urgent care partnerships"
            ],
            'readmission_rate': [
                "Enhanced discharge planning",
                "Post-discharge follow-up within 72 hours",
                "Medication reconciliation process"
            ],
            'total_cost_per_patient': [
                "Care management for high-cost patients",
                "Preventive care focus",
                "Generic medication formulary optimization"
            ]
        }
        
        return action_map.get(metric, ["Cost analysis and targeted interventions"])
    
    def _create_metrics_summary(self, provider_data: Dict, peer_benchmarks: Dict) -> Dict:
        """Create executive summary of key metrics."""
        return {
            'top_strengths': [
                f"Quality Score: {provider_data.get('overall_quality_score', 0):.1f}%",
                f"Patient Satisfaction: {provider_data.get('patient_satisfaction', 0):.1f}/5.0",
                f"Generic Prescribing: {provider_data.get('generic_prescribing_rate', 0):.1f}%"
            ],
            'improvement_areas': [
                f"Cost per Patient: ${provider_data.get('total_cost_per_patient', 0):,.0f}",
                f"ED Visit Rate: {provider_data.get('ed_visits_per_1000', 0):.0f}/1000",
                f"Readmission Rate: {provider_data.get('readmission_rate', 0):.1f}%"
            ],
            'peer_comparison': {
                'above_average': sum(1 for k, v in peer_benchmarks.items() 
                                   if 'percentile' in k and provider_data.get(k, 50) > 50),
                'below_average': sum(1 for k, v in peer_benchmarks.items() 
                                   if 'percentile' in k and provider_data.get(k, 50) < 50)
            }
        }
    
    def _prioritize_action_items(self, recommendations: List[Dict]) -> List[Dict]:
        """Prioritize top 5 action items for provider focus."""
        high_priority = [r for r in recommendations if r['priority'] == 'High']
        medium_priority = [r for r in recommendations if r['priority'] == 'Medium']
        
        action_items = (high_priority + medium_priority)[:5]
        
        for i, item in enumerate(action_items, 1):
            item['rank'] = i
            item['timeline'] = '30 days' if item['priority'] == 'High' else '90 days'
        
        return action_items

# Example usage and demonstration
if __name__ == "__main__":
    # Create sample provider data
    np.random.seed(42)
    
    # Sample provider performance data
    sample_provider = {
        'provider_id': 'PROV_001',
        'provider_name': 'Dr. Sarah Johnson, MD',
        'specialty': 'Family Medicine',
        'panel_size': 1850,
        'reporting_period': 'Q4 2024',
        
        # Quality measures (percentages)
        'colorectal_screening': 72,
        'breast_cancer_screening': 88,
        'cervical_cancer_screening': 82,
        'annual_wellness_visits': 65,
        'diabetes_eye_exam': 68,
        'blood_pressure_control': 74,
        'diabetes_control': 58,
        
        # Care coordination
        'post_discharge_followup': 78,
        'medication_reconciliation': 85,
        'care_plan_documentation': 75,
        'specialist_communication': 70,
        'patient_portal_engagement': 55,
        
        # Patient experience (1-5 scale)
        'patient_satisfaction': 4.1,
        'access_to_care': 3.9,
        'communication_rating': 4.3,
        'care_coordination_rating': 4.0,
        
        # Cost and utilization
        'total_cost_per_patient': 9200,
        'ed_visits_per_1000': 280,
        'readmission_rate': 14.5,
        'specialist_referral_rate': 38,
        'generic_prescribing_rate': 82,
        'preventable_hospitalization_rate': 9.2
    }
    
    # Sample peer benchmarks (distributions)
    sample_benchmarks = {
        'overall_quality_score_distribution': np.random.normal(75, 15, 100).tolist(),
        'total_cost_per_patient_distribution': np.random.normal(8500, 1500, 100).tolist(),
        'ed_visits_per_1000_distribution': np.random.normal(250, 50, 100).tolist(),
        'readmission_rate_distribution': np.random.normal(12, 3, 100).tolist()
    }
    
    # Initialize scorecard engine
    scorecard_engine = ProviderScorecardEngine()
    
    print("📊 Pearl Health-Style Provider Scorecard Demo")
    print("=" * 55)
    
    # Generate comprehensive scorecard
    scorecard = scorecard_engine.generate_provider_scorecard(sample_provider, sample_benchmarks)
    
    # Display key results
    print(f"\n👨‍⚕️ Provider: {scorecard['provider_info']['provider_name']}")
    print(f"Panel Size: {scorecard['provider_info']['panel_size']:,} patients")
    print("-" * 55)
    
    overall = scorecard['overall_performance']
    print(f"VBC Composite Score: {overall['vbc_composite_score']}")
    print(f"Performance Tier: {overall['performance_tier'].replace('_', ' ').title()}")
    print(f"Peer Percentile: {overall['peer_percentile']}th")
    
    print(f"\n📈 Quality Performance:")
    quality = scorecard['quality_performance']
    print(f"  Overall Quality Score: {quality['overall_quality_score']}%")
    for category, data in quality['category_scores'].items():
        print(f"  {category.replace('_', ' ').title()}: {data['score']}%")
    
    print(f"\n💰 Cost Performance:")
    cost = scorecard['cost_performance']
    print(f"  Overall Cost Score: {cost['overall_cost_score']}%")
    print(f"  Cost Tier: {cost['cost_tier'].replace('_', ' ').title()}")
    
    savings = cost.get('cost_savings_opportunity', {})
    if savings.get('total_annual_opportunity', 0) > 0:
        print(f"  Savings Opportunity: ${savings['total_annual_opportunity']:,}")
    
    print(f"\n🎯 Top 3 Improvement Opportunities:")
    for i, item in enumerate(scorecard['action_items'][:3], 1):
        print(f"  {i}. {item['focus_area'].replace('_', ' ').title()}")
        print(f"     Priority: {item['priority']} | Timeline: {item['timeline']}")
    
    print("\n" + "=" * 55)
    print("Provider Scorecard Demo Complete! 🎉")
    print("This demonstrates Pearl Health-style provider performance analytics")
