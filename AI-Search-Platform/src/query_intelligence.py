"""
Query Intelligence Engine
========================

Advanced query understanding, intent detection, and context-aware search enhancement.
Transforms natural language queries into optimized search parameters.
"""

import re
import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np

@dataclass
class QueryIntent:
    """Detected user intent and context."""
    intent_type: str  # informational, transactional, navigational, analytical
    confidence: float
    entities: List[str]
    keywords: List[str]
    filters: Dict[str, Any]
    department_scope: Optional[str] = None
    time_scope: Optional[str] = None

@dataclass
class QueryAnalysis:
    """Complete query analysis results."""
    original_query: str
    processed_query: str
    intent: QueryIntent
    suggestions: List[str]
    expected_result_types: List[str]
    complexity_score: float

class QueryIntelligenceEngine:
    """
    Advanced query understanding and optimization engine.
    
    Features:
    - Intent detection and classification
    - Entity extraction and keyword identification
    - Department and time-based scoping
    - Query expansion and synonym handling
    - Context-aware filtering
    """
    
    def __init__(self):
        self.department_keywords = {
            'engineering': ['api', 'code', 'development', 'technical', 'architecture', 'deployment', 'bug', 'feature'],
            'product': ['roadmap', 'strategy', 'features', 'user', 'customer', 'feedback', 'requirements', 'launch'],
            'sales': ['revenue', 'deals', 'pipeline', 'customers', 'targets', 'performance', 'commission', 'quotas'],
            'marketing': ['campaign', 'ads', 'conversion', 'leads', 'brand', 'content', 'social', 'email'],
            'hr': ['employee', 'onboarding', 'training', 'benefits', 'performance', 'hiring', 'culture', 'policy'],
            'finance': ['budget', 'forecast', 'revenue', 'expenses', 'profit', 'costs', 'financial', 'accounting'],
            'security': ['breach', 'incident', 'vulnerability', 'compliance', 'risk', 'audit', 'access', 'permissions'],
            'support': ['ticket', 'issue', 'escalation', 'resolution', 'customer', 'bug', 'problem', 'help']
        }
        
        self.intent_patterns = {
            'informational': [
                r'what is', r'how to', r'explain', r'define', r'tell me about',
                r'information about', r'details on', r'overview of'
            ],
            'analytical': [
                r'analyze', r'compare', r'metrics', r'performance', r'statistics',
                r'report on', r'trends in', r'data about', r'insights'
            ],
            'procedural': [
                r'how do i', r'steps to', r'process for', r'procedure',
                r'guide to', r'tutorial', r'instructions'
            ],
            'troubleshooting': [
                r'problem with', r'error', r'not working', r'issue',
                r'bug', r'troubleshoot', r'fix', r'resolve'
            ]
        }
        
        self.time_patterns = {
            'recent': [r'recent', r'latest', r'new', r'current', r'this week', r'this month'],
            'quarterly': [r'q1', r'q2', r'q3', r'q4', r'quarter', r'quarterly'],
            'yearly': [r'2024', r'2025', r'this year', r'last year', r'annual'],
            'historical': [r'historical', r'past', r'previous', r'old', r'archived']
        }
        
        self.synonyms = {
            'client': ['customer', 'account', 'user'],
            'revenue': ['sales', 'income', 'earnings'],
            'issue': ['problem', 'bug', 'error', 'incident'],
            'meeting': ['call', 'discussion', 'session'],
            'document': ['file', 'report', 'paper', 'manual']
        }
        
        print("🧠 Query Intelligence Engine initialized")
    
    def analyze_query(self, query: str, user_context: Dict[str, Any] = None) -> QueryAnalysis:
        """
        Perform comprehensive query analysis.
        
        Args:
            query: User's natural language query
            user_context: Additional context (department, role, recent searches)
        
        Returns:
            Complete query analysis with intent, entities, and optimization suggestions
        """
        # Normalize query
        processed_query = self._preprocess_query(query)
        
        # Detect intent
        intent = self._detect_intent(processed_query)
        
        # Apply user context
        if user_context:
            intent = self._apply_user_context(intent, user_context)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(processed_query, intent)
        
        # Determine expected result types
        result_types = self._predict_result_types(intent)
        
        # Calculate complexity
        complexity = self._calculate_complexity(processed_query, intent)
        
        analysis = QueryAnalysis(
            original_query=query,
            processed_query=processed_query,
            intent=intent,
            suggestions=suggestions,
            expected_result_types=result_types,
            complexity_score=complexity
        )
        
        return analysis
    
    def _preprocess_query(self, query: str) -> str:
        """Clean and normalize the query."""
        # Convert to lowercase
        processed = query.lower().strip()
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', processed)
        
        # Handle common contractions
        contractions = {
            "what's": "what is",
            "how's": "how is", 
            "where's": "where is",
            "don't": "do not",
            "can't": "cannot"
        }
        
        for contraction, expansion in contractions.items():
            processed = processed.replace(contraction, expansion)
        
        return processed
    
    def _detect_intent(self, query: str) -> QueryIntent:
        """Detect user intent from query."""
        intent_scores = {}
        
        # Score each intent type
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, query):
                    score += 1
            intent_scores[intent_type] = score
        
        # Determine primary intent
        if not any(intent_scores.values()):
            primary_intent = 'informational'  # Default
            confidence = 0.5
        else:
            primary_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(0.95, 0.6 + (intent_scores[primary_intent] * 0.15))
        
        # Extract entities and keywords
        entities = self._extract_entities(query)
        keywords = self._extract_keywords(query)
        
        # Detect department scope
        department = self._detect_department(query, keywords)
        
        # Detect time scope
        time_scope = self._detect_time_scope(query)
        
        # Generate filters
        filters = self._generate_filters(query, entities, department, time_scope)
        
        return QueryIntent(
            intent_type=primary_intent,
            confidence=confidence,
            entities=entities,
            keywords=keywords,
            filters=filters,
            department_scope=department,
            time_scope=time_scope
        )
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract named entities from query."""
        entities = []
        
        # Company names (common patterns)
        company_pattern = r'\b[A-Z][a-z]+ (?:Corp|Inc|LLC|Ltd|Solutions|Technologies|Systems)\b'
        companies = re.findall(company_pattern, query)
        entities.extend(companies)
        
        # Dates
        date_patterns = [
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]
        for pattern in date_patterns:
            dates = re.findall(pattern, query)
            entities.extend(dates)
        
        # Numbers/metrics
        number_pattern = r'\b\d+(?:\.\d+)?%?\b'
        numbers = re.findall(number_pattern, query)
        entities.extend(numbers)
        
        return entities
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query."""
        # Remove stop words
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'what', 'how', 'where', 'when'
        }
        
        words = query.split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Expand with synonyms
        expanded_keywords = keywords.copy()
        for keyword in keywords:
            if keyword in self.synonyms:
                expanded_keywords.extend(self.synonyms[keyword])
        
        return list(set(expanded_keywords))
    
    def _detect_department(self, query: str, keywords: List[str]) -> Optional[str]:
        """Detect relevant department based on query content."""
        department_scores = {}
        
        for dept, dept_keywords in self.department_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in dept_keywords:
                    score += 1
            # Also check for direct mentions
            if dept in query:
                score += 2
            department_scores[dept] = score
        
        if max(department_scores.values()) > 0:
            return max(department_scores, key=department_scores.get)
        return None
    
    def _detect_time_scope(self, query: str) -> Optional[str]:
        """Detect time-related context in query."""
        for time_type, patterns in self.time_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return time_type
        return None
    
    def _generate_filters(self, query: str, entities: List[str], 
                         department: Optional[str], time_scope: Optional[str]) -> Dict[str, Any]:
        """Generate search filters based on analysis."""
        filters = {}
        
        if department:
            filters['department'] = department
        
        if time_scope:
            filters['time_scope'] = time_scope
        
        # Document type hints
        if any(word in query for word in ['report', 'analysis', 'dashboard']):
            filters['document_types'] = ['analysis', 'dashboard', 'technical_report']
        elif any(word in query for word in ['procedure', 'process', 'how to']):
            filters['document_types'] = ['procedure', 'playbook', 'checklist']
        elif any(word in query for word in ['strategy', 'plan', 'roadmap']):
            filters['document_types'] = ['strategic_plan', 'financial_plan']
        
        # Classification level
        if any(word in query for word in ['confidential', 'sensitive', 'restricted']):
            filters['classification'] = ['confidential', 'restricted']
        
        return filters
    
    def _apply_user_context(self, intent: QueryIntent, user_context: Dict[str, Any]) -> QueryIntent:
        """Apply user context to refine intent."""
        # If user has a department, bias towards that department
        if 'department' in user_context and not intent.department_scope:
            user_dept = user_context['department'].lower()
            if user_dept in self.department_keywords:
                intent.department_scope = user_dept
                intent.filters['department'] = user_dept
        
        # Consider user's recent searches for context
        if 'recent_searches' in user_context:
            # Could implement query expansion based on search history
            pass
        
        return intent
    
    def _generate_suggestions(self, query: str, intent: QueryIntent) -> List[str]:
        """Generate helpful query suggestions."""
        suggestions = []
        
        # Department-specific suggestions
        if intent.department_scope:
            dept = intent.department_scope
            suggestions.append(f"Search only in {dept.title()} documents")
            suggestions.append(f"Recent {dept} updates")
        
        # Intent-specific suggestions
        if intent.intent_type == 'informational':
            suggestions.extend([
                f"Latest information about {' '.join(intent.keywords[:2])}",
                f"Overview of {' '.join(intent.keywords[:2])}"
            ])
        elif intent.intent_type == 'analytical':
            suggestions.extend([
                f"Performance metrics for {' '.join(intent.keywords[:2])}",
                f"Trends in {' '.join(intent.keywords[:2])}"
            ])
        elif intent.intent_type == 'procedural':
            suggestions.extend([
                f"Step-by-step guide for {' '.join(intent.keywords[:2])}",
                f"Best practices for {' '.join(intent.keywords[:2])}"
            ])
        
        return suggestions[:3]  # Limit to top 3
    
    def _predict_result_types(self, intent: QueryIntent) -> List[str]:
        """Predict expected document types for results."""
        result_types = []
        
        if intent.intent_type == 'analytical':
            result_types.extend(['analysis', 'dashboard', 'technical_report'])
        elif intent.intent_type == 'procedural':
            result_types.extend(['procedure', 'playbook', 'checklist'])
        elif intent.intent_type == 'informational':
            result_types.extend(['strategic_plan', 'technical_documentation'])
        
        # Department-specific types
        if intent.department_scope == 'finance':
            result_types.append('financial_plan')
        elif intent.department_scope == 'engineering':
            result_types.append('technical_documentation')
        
        return list(set(result_types)) if result_types else ['any']
    
    def _calculate_complexity(self, query: str, intent: QueryIntent) -> float:
        """Calculate query complexity score (0-1)."""
        complexity = 0.0
        
        # Length factor
        complexity += min(0.3, len(query.split()) / 20)
        
        # Entity count factor  
        complexity += min(0.2, len(intent.entities) / 5)
        
        # Keyword count factor
        complexity += min(0.2, len(intent.keywords) / 10)
        
        # Intent complexity
        intent_complexity = {
            'informational': 0.1,
            'procedural': 0.2,
            'analytical': 0.3,
            'troubleshooting': 0.2
        }
        complexity += intent_complexity.get(intent.intent_type, 0.1)
        
        # Filter complexity
        complexity += min(0.2, len(intent.filters) / 5)
        
        return min(1.0, complexity)

def demo_query_intelligence():
    """Demonstrate query intelligence capabilities."""
    engine = QueryIntelligenceEngine()
    
    test_queries = [
        "What is our Q4 sales performance?",
        "How do I escalate a customer support issue?",
        "Show me recent security incidents",
        "API documentation for authentication",
        "Employee onboarding checklist",
        "Marketing campaign ROI analysis",
        "Product roadmap for 2025"
    ]
    
    print("\n🔍 Query Intelligence Demo")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        analysis = engine.analyze_query(query)
        
        print(f"🎯 Intent: {analysis.intent.intent_type} (confidence: {analysis.intent.confidence:.2f})")
        print(f"🏢 Department: {analysis.intent.department_scope or 'Any'}")
        print(f"🕒 Time Scope: {analysis.intent.time_scope or 'Any'}")
        print(f"🔑 Keywords: {', '.join(analysis.intent.keywords[:3])}")
        print(f"📊 Complexity: {analysis.complexity_score:.2f}")
        if analysis.suggestions:
            print(f"💡 Suggestions: {analysis.suggestions[0]}")

if __name__ == "__main__":
    demo_query_intelligence()
