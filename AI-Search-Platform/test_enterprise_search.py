"""
Test Enterprise Search with Realistic Queries
============================================

Test the enhanced AI Search Platform with realistic enterprise queries
that should find relevant documents from our enterprise knowledge base.
"""

import sys
sys.path.append('src')

from src.rag_engine import AdvancedRAGEngine
from src.query_intelligence import QueryIntelligenceEngine
import asyncio
import time

async def test_enterprise_queries():
    """Test enterprise-specific queries."""
    print("🏢 Testing Enhanced Enterprise Search")
    print("=" * 60)
    
    rag_engine = AdvancedRAGEngine()
    
    # Realistic enterprise queries
    enterprise_queries = [
        "Q4 sales performance metrics",
        "customer support escalation procedures", 
        "security incident response protocol",
        "API authentication documentation",
        "employee onboarding process",
        "marketing campaign ROI analysis",
        "machine learning model performance",
        "financial budget forecast 2025"
    ]
    
    for query in enterprise_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 50)
        
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
                dept = result.metadata.get('department', 'General')
                doc_type = result.metadata.get('document_type', 'Document')
                author = result.metadata.get('author', 'Unknown')
                print(f"     📂 {dept} • {doc_type} • 👤 {author}")
                
                # Show content preview
                content_preview = result.content[:120] + "..." if len(result.content) > 120 else result.content
                print(f"     📄 {content_preview}")
                
        except Exception as e:
            print(f"❌ Search failed: {e}")

def test_query_intelligence():
    """Test query intelligence with enterprise queries."""
    print("\n🧠 Testing Query Intelligence")
    print("=" * 60)
    
    intelligence = QueryIntelligenceEngine()
    
    test_queries = [
        "What are our Q4 sales numbers?",
        "How do I escalate a support ticket?",
        "Show me recent security incidents",
        "Where is the API documentation?",
        "Employee onboarding checklist"
    ]
    
    for query in test_queries:
        print(f"\n📝 '{query}'")
        analysis = intelligence.analyze_query(query)
        
        print(f"   🎯 Intent: {analysis.intent.intent_type}")
        print(f"   🏢 Department: {analysis.intent.department_scope or 'Any'}")
        print(f"   🔧 Filters: {analysis.intent.filters}")

async def main():
    """Run enterprise search tests."""
    test_query_intelligence()
    await test_enterprise_queries()
    
    print("\n🎉 Enterprise search testing completed!")

if __name__ == "__main__":
    asyncio.run(main())
