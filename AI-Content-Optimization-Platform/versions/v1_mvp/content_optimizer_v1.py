"""
AI Content Optimizer - Version 1.0 MVP
======================================

Initial release focusing on core content analysis functionality.
Simple, focused features to validate product-market fit.

Version 1.0 Features:
- Basic content analysis (readability, sentiment)
- Simple optimization recommendations
- Command-line interface
- Single-user functionality
"""

import re
import math
from textstat import flesch_reading_ease, flesch_kincaid_grade
from textblob import TextBlob
from collections import Counter
import argparse
from datetime import datetime
import json

class ContentOptimizerV1:
    """
    MVP version of the AI Content Optimizer.
    
    Provides basic content analysis and optimization recommendations
    to validate core product concepts with early users.
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.launch_date = "2024-01-15"
        
        # Simple keyword categories for optimization
        self.power_words = {
            'emotional': ['amazing', 'incredible', 'stunning', 'brilliant', 'extraordinary'],
            'urgency': ['now', 'today', 'immediately', 'urgent', 'deadline'],
            'social_proof': ['proven', 'trusted', 'verified', 'certified', 'recommended'],
            'benefit': ['free', 'save', 'gain', 'profit', 'bonus', 'advantage']
        }
        
        # Basic content best practices
        self.optimization_rules = {
            'title_length': {'min': 30, 'max': 60},
            'paragraph_length': {'max': 150},
            'sentence_length': {'max': 20},
            'reading_grade': {'max': 8}
        }
    
    def analyze_content(self, content: str, title: str = "") -> dict:
        """
        Analyze content for basic optimization opportunities.
        
        Args:
            content: Main content text
            title: Optional title/headline
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        analysis_results = {
            'version': self.version,
            'analyzed_at': datetime.now().isoformat(),
            'content_stats': self._get_content_stats(content),
            'readability': self._analyze_readability(content),
            'sentiment': self._analyze_sentiment(content),
            'power_words': self._analyze_power_words(content),
            'recommendations': []
        }
        
        # Add title analysis if provided
        if title:
            analysis_results['title_analysis'] = self._analyze_title(title)
        
        # Generate optimization recommendations
        analysis_results['recommendations'] = self._generate_recommendations(analysis_results, title)
        
        return analysis_results
    
    def _get_content_stats(self, content: str) -> dict:
        """Calculate basic content statistics."""
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = content.split('\n\n')
        
        return {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len([p for p in paragraphs if p.strip()]),
            'character_count': len(content),
            'avg_words_per_sentence': len(words) / max(1, len(sentences)) if sentences else 0,
            'avg_sentences_per_paragraph': len(sentences) / max(1, len(paragraphs)) if paragraphs else 0
        }
    
    def _analyze_readability(self, content: str) -> dict:
        """Analyze content readability using standard metrics."""
        try:
            flesch_score = flesch_reading_ease(content)
            grade_level = flesch_kincaid_grade(content)
            
            # Determine readability level
            if flesch_score >= 90:
                level = 'Very Easy'
            elif flesch_score >= 80:
                level = 'Easy'
            elif flesch_score >= 70:
                level = 'Fairly Easy'
            elif flesch_score >= 60:
                level = 'Standard'
            elif flesch_score >= 50:
                level = 'Fairly Difficult'
            elif flesch_score >= 30:
                level = 'Difficult'
            else:
                level = 'Very Difficult'
            
            return {
                'flesch_reading_ease': round(flesch_score, 1),
                'flesch_kincaid_grade': round(grade_level, 1),
                'readability_level': level,
                'is_optimal': 60 <= flesch_score <= 80  # Target range for general audience
            }
        except:
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'readability_level': 'Unknown',
                'is_optimal': False
            }
    
    def _analyze_sentiment(self, content: str) -> dict:
        """Analyze content sentiment and emotional tone."""
        blob = TextBlob(content)
        
        # Sentiment polarity: -1 (negative) to 1 (positive)
        polarity = blob.sentiment.polarity
        
        # Sentiment subjectivity: 0 (objective) to 1 (subjective)
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment category
        if polarity > 0.1:
            sentiment_label = 'Positive'
        elif polarity < -0.1:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'
        
        # Determine tone
        if subjectivity > 0.5:
            tone = 'Subjective'
        else:
            tone = 'Objective'
        
        return {
            'polarity_score': round(polarity, 3),
            'subjectivity_score': round(subjectivity, 3),
            'sentiment_label': sentiment_label,
            'tone': tone,
            'is_engaging': polarity > 0 and subjectivity > 0.3  # Positive and somewhat subjective
        }
    
    def _analyze_power_words(self, content: str) -> dict:
        """Identify power words that can improve engagement."""
        content_lower = content.lower()
        words = re.findall(r'\b\w+\b', content_lower)
        
        found_power_words = {category: [] for category in self.power_words}
        total_power_words = 0
        
        for category, power_word_list in self.power_words.items():
            for word in power_word_list:
                if word in words:
                    found_power_words[category].append(word)
                    total_power_words += words.count(word)
        
        power_word_density = (total_power_words / len(words) * 100) if words else 0
        
        return {
            'total_power_words': total_power_words,
            'power_word_density': round(power_word_density, 2),
            'found_by_category': found_power_words,
            'is_optimal': 1 <= power_word_density <= 3  # 1-3% is good balance
        }
    
    def _analyze_title(self, title: str) -> dict:
        """Analyze title/headline effectiveness."""
        title_length = len(title)
        word_count = len(title.split())
        
        # Check for power words in title
        title_lower = title.lower()
        title_power_words = []
        for category, words in self.power_words.items():
            for word in words:
                if word in title_lower:
                    title_power_words.append(word)
        
        # Check for numbers (often increase click-through)
        has_numbers = bool(re.search(r'\d', title))
        
        return {
            'character_length': title_length,
            'word_count': word_count,
            'power_words': title_power_words,
            'has_numbers': has_numbers,
            'is_optimal_length': self.optimization_rules['title_length']['min'] <= title_length <= self.optimization_rules['title_length']['max'],
            'estimated_ctr_score': self._calculate_title_ctr_score(title, title_power_words, has_numbers)
        }
    
    def _calculate_title_ctr_score(self, title: str, power_words: list, has_numbers: bool) -> float:
        """Calculate estimated click-through rate score for title."""
        base_score = 5.0  # Base CTR of 5%
        
        # Length optimization
        length = len(title)
        if 30 <= length <= 60:
            base_score += 1.0
        elif length < 30 or length > 80:
            base_score -= 0.5
        
        # Power words boost
        base_score += len(power_words) * 0.3
        
        # Numbers boost
        if has_numbers:
            base_score += 0.5
        
        # Question marks can increase engagement
        if '?' in title:
            base_score += 0.3
        
        return round(min(base_score, 10.0), 1)  # Cap at 10%
    
    def _generate_recommendations(self, analysis: dict, title: str = "") -> list:
        """Generate actionable optimization recommendations."""
        recommendations = []
        
        # Readability recommendations
        readability = analysis['readability']
        if not readability['is_optimal']:
            if readability['flesch_reading_ease'] < 60:
                recommendations.append({
                    'category': 'Readability',
                    'priority': 'High',
                    'issue': 'Content is too difficult to read',
                    'recommendation': 'Use shorter sentences and simpler words to improve readability',
                    'target_metric': 'Flesch Reading Ease: 60-80'
                })
            elif readability['flesch_reading_ease'] > 80:
                recommendations.append({
                    'category': 'Readability',
                    'priority': 'Medium',
                    'issue': 'Content may be too simple',
                    'recommendation': 'Consider adding more sophisticated vocabulary for your target audience',
                    'target_metric': 'Flesch Reading Ease: 60-80'
                })
        
        # Sentiment recommendations
        sentiment = analysis['sentiment']
        if not sentiment['is_engaging']:
            recommendations.append({
                'category': 'Engagement',
                'priority': 'High',
                'issue': 'Content lacks emotional engagement',
                'recommendation': 'Add more positive language and personal opinions to connect with readers',
                'target_metric': 'Positive sentiment with moderate subjectivity'
            })
        
        # Power words recommendations
        power_words = analysis['power_words']
        if not power_words['is_optimal']:
            if power_words['power_word_density'] < 1:
                recommendations.append({
                    'category': 'Persuasion',
                    'priority': 'Medium',
                    'issue': 'Low usage of persuasive language',
                    'recommendation': 'Include more power words to increase persuasiveness and engagement',
                    'target_metric': 'Power word density: 1-3%'
                })
            elif power_words['power_word_density'] > 3:
                recommendations.append({
                    'category': 'Persuasion',
                    'priority': 'Medium',
                    'issue': 'Overuse of power words may seem pushy',
                    'recommendation': 'Reduce power word usage to maintain authenticity',
                    'target_metric': 'Power word density: 1-3%'
                })
        
        # Content structure recommendations
        stats = analysis['content_stats']
        if stats['avg_words_per_sentence'] > 20:
            recommendations.append({
                'category': 'Structure',
                'priority': 'Medium',
                'issue': 'Sentences are too long',
                'recommendation': 'Break up long sentences to improve readability',
                'target_metric': 'Average words per sentence: <20'
            })
        
        # Title recommendations
        if title and 'title_analysis' in analysis:
            title_analysis = analysis['title_analysis']
            if not title_analysis['is_optimal_length']:
                recommendations.append({
                    'category': 'Title',
                    'priority': 'High',
                    'issue': 'Title length is not optimal for search and social',
                    'recommendation': 'Adjust title to 30-60 characters for better visibility',
                    'target_metric': 'Title length: 30-60 characters'
                })
            
            if not title_analysis['power_words']:
                recommendations.append({
                    'category': 'Title',
                    'priority': 'Medium',
                    'issue': 'Title lacks persuasive elements',
                    'recommendation': 'Add power words to make your title more compelling',
                    'target_metric': 'Include 1-2 power words in title'
                })
        
        return recommendations

def main():
    """Command-line interface for Content Optimizer v1.0"""
    parser = argparse.ArgumentParser(description='AI Content Optimizer v1.0 - MVP')
    parser.add_argument('--content', required=True, help='Content text to analyze')
    parser.add_argument('--title', help='Optional title/headline')
    parser.add_argument('--output', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    # Initialize optimizer
    optimizer = ContentOptimizerV1()
    
    print("🚀 AI Content Optimizer v1.0 - MVP")
    print("=" * 50)
    
    # Analyze content
    results = optimizer.analyze_content(args.content, args.title or "")
    
    # Display results
    print(f"\n📊 Content Analysis Results:")
    print(f"Word Count: {results['content_stats']['word_count']}")
    print(f"Readability: {results['readability']['readability_level']} (Flesch: {results['readability']['flesch_reading_ease']})")
    print(f"Sentiment: {results['sentiment']['sentiment_label']} (Score: {results['sentiment']['polarity_score']})")
    print(f"Power Words: {results['power_words']['total_power_words']} ({results['power_words']['power_word_density']}% density)")
    
    if 'title_analysis' in results:
        print(f"Title CTR Score: {results['title_analysis']['estimated_ctr_score']}%")
    
    print(f"\n💡 Optimization Recommendations ({len(results['recommendations'])}):")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")
    
    print("\n" + "=" * 50)
    print("Analysis complete! 🎉")

if __name__ == "__main__":
    main()

# Example usage:
"""
python content_optimizer_v1.py \
    --content "This is amazing content that will help you grow your business today. Studies show that our proven method increases engagement by 300%. Don't wait - start now!" \
    --title "Amazing Business Growth Secrets That Work" \
    --output results_v1.json
"""
