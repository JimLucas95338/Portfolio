"""
Enhanced AI Search Platform Demo
==============================

Demonstrates the improved AI Search Platform with:
- Realistic enterprise knowledge base
- Advanced query intelligence
- Department-specific filtering
- Intent detection and analysis
"""

import sys
import os
sys.path.append('src')

from src.rag_engine import AdvancedRAGEngine
from src.query_intelligence import QueryIntelligenceEngine
import asyncio
import time

def demo_query_intelligence():
    """Demonstrate query intelligence capabilities."""
    print("🧠 Query Intelligence Demo")
    print("=" * 60)
    
    intelligence_engine = QueryIntelligenceEngine()
    
    test_queries = [
        "What is our Q4 sales performance?",
        "How do I escalate a customer support issue?", 
        "Show me recent security incidents",
        "API documentation for authentication",
        "Employee onboarding process",
        "Marketing campaign ROI analysis for 2024",
        "Product roadmap and strategy",
        "Financial forecast budget planning",
        "Machine learning model performance metrics",
        "IT security breach response procedures"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        analysis = intelligence_engine.analyze_query(query)
        
        print(f"   🎯 Intent: {analysis.intent.intent_type} (confidence: {analysis.intent.confidence:.2f})")
        print(f"   🏢 Department: {analysis.intent.department_scope or 'Any'}")
        print(f"   🕒 Time Scope: {analysis.intent.time_scope or 'Any'}")
        print(f"   🔑 Keywords: {', '.join(analysis.intent.keywords[:4])}")
        print(f"   📊 Complexity: {analysis.complexity_score:.2f}")
        if analysis.intent.filters:
            print(f"   🔧 Filters: {analysis.intent.filters}")

async def demo_enhanced_search():
    """Demonstrate enhanced search with realistic enterprise data."""
    print("\n🔍 Enhanced Enterprise Search Demo")
    print("=" * 60)
    
    rag_engine = AdvancedRAGEngine()
    
    # Test queries that should find relevant enterprise documents
    enterprise_queries = [
        "Q4 sales performance",
        "customer support escalation procedure", 
        "security incident response",
        "API authentication documentation",
        "employee onboarding checklist",
        "marketing campaign analysis",
        "machine learning model performance",
        "financial budget forecast"
    ]
    
    for query in enterprise_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 40)
        
        start_time = time.time()
        try:
            response = await rag_engine.search(query, max_results=3)
            search_time = (time.time() - start_time) * 1000
            
            print(f"⚡ Search completed in {search_time:.1f}ms")
            print(f"📊 Confidence: {response.confidence_score:.3f}")
            print(f"🎯 Intent: {response.intent_type}")
            
            print(f"\n📚 Found {len(response.search_results)} results:")
            for i, result in enumerate(response.search_results, 1):
                print(f"  {i}. {result.source} (Score: {result.relevance_score:.3f})")
                print(f"     📂 {result.metadata.get('department', 'General')} • {result.metadata.get('document_type', 'Document')}")
                print(f"     👤 {result.metadata.get('author', 'Unknown')}")
                # Show first 100 characters of content
                content_preview = result.content[:100] + "..." if len(result.content) > 100 else result.content
                print(f"     📄 {content_preview}")
            
            if response.answer:
                print(f"\n💬 AI Response Preview:")
                answer_preview = response.answer[:150] + "..." if len(response.answer) > 150 else response.answer
                print(f"   {answer_preview}")
                
        except Exception as e:
            print(f"❌ Search failed: {e}")

def demo_department_filtering():
    """Demonstrate department-specific search filtering."""
    print("\n🏢 Department Filtering Demo")
    print("=" * 60)
    
    intelligence_engine = QueryIntelligenceEngine()
    
    # Test queries that should be routed to specific departments
    department_queries = [
        ("sales performance metrics", "sales"),
        ("engineering API documentation", "engineering"), 
        ("HR employee policies", "hr"),
        ("marketing campaign results", "marketing"),
        ("financial budget analysis", "finance"),
        ("security breach protocols", "security"),
        ("product strategy roadmap", "product"),
        ("customer support procedures", "support")
    ]
    
    for query, expected_dept in department_queries:
        print(f"\n📝 Query: '{query}'")
        analysis = intelligence_engine.analyze_query(query)
        detected_dept = analysis.intent.department_scope
        
        status = "✅" if detected_dept == expected_dept else "❌"
        print(f"   {status} Expected: {expected_dept} | Detected: {detected_dept or 'None'}")
        
        if analysis.intent.filters:
            print(f"   🔧 Applied Filters: {analysis.intent.filters}")

def demo_document_type_detection():
    """Demonstrate document type prediction."""
    print("\n📄 Document Type Detection Demo")
    print("=" * 60)
    
    intelligence_engine = QueryIntelligenceEngine()
    
    # Test queries for different document types
    type_queries = [
        ("step by step onboarding process", "procedure"),
        ("quarterly sales analysis report", "analysis"),
        ("security incident response playbook", "playbook"), 
        ("product strategy planning document", "strategic_plan"),
        ("API reference documentation", "technical_documentation"),
        ("financial budget forecast", "financial_plan"),
        ("employee training checklist", "checklist")
    ]
    
    for query, expected_type in type_queries:
        print(f"\n📝 Query: '{query}'")
        analysis = intelligence_engine.analyze_query(query)
        predicted_types = analysis.expected_result_types
        
        status = "✅" if expected_type in predicted_types else "❌"
        print(f"   {status} Expected: {expected_type}")
        print(f"   🎯 Predicted Types: {', '.join(predicted_types)}")

async def main():
    """Run comprehensive demo of enhanced AI Search Platform."""
    print("🚀 Enhanced AI Search Platform - Comprehensive Demo")
    print("=" * 80)
    print("Demonstrating realistic enterprise search with:")
    print("• 10 diverse enterprise documents")
    print("• Advanced query intelligence") 
    print("• Department-specific filtering")
    print("• Document type prediction")
    print("• Intent detection and analysis")
    print("=" * 80)
    
    # Run all demos
    demo_query_intelligence()
    await demo_enhanced_search()
    demo_department_filtering()
    demo_document_type_detection()
    
    print("\n🎉 Demo completed!")
    print("\nKey Improvements Demonstrated:")
    print("✅ Realistic enterprise knowledge base with 10 diverse documents")
    print("✅ Advanced query intelligence with intent detection")
    print("✅ Department-aware search filtering")
    print("✅ Document type prediction and classification")
    print("✅ Enhanced metadata and source attribution")
    print("✅ Intelligent content ranking and scoring")

if __name__ == "__main__":
    asyncio.run(main())
