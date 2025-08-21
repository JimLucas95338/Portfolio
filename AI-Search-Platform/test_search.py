"""
Quick Test Script for AI Search Platform
========================================

This script tests the search functionality to ensure it returns results.
"""

import asyncio
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_engine import AdvancedRAGEngine

async def test_search():
    """Test the search functionality."""
    print("🔍 Testing AI Search Platform")
    print("=" * 40)
    
    # Initialize RAG engine
    print("⚡ Initializing RAG engine...")
    rag_engine = AdvancedRAGEngine()
    
    # Test queries
    test_queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Explain natural language processing",
        "What is RAG?",
        "Enterprise search solutions"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: '{query}'")
        print("-" * 30)
        
        try:
            # Perform search
            response = await rag_engine.search(query, user_id="test_user")
            
            # Display results
            print(f"✅ Found {len(response.source_results)} results")
            print(f"📊 Confidence: {response.confidence_score:.3f}")
            print(f"⚡ Time: {response.processing_time_ms:.1f}ms")
            print(f"🎯 Intent: {response.query_intent}")
            
            if response.source_results:
                print("\n📚 Top Results:")
                for j, result in enumerate(response.source_results[:3], 1):
                    print(f"  {j}. {result.source} (Score: {result.relevance_score:.3f})")
                    print(f"     {result.content[:100]}...")
            
            print(f"\n💬 Response Preview:")
            print(f"   {response.synthesized_answer[:150]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Search test completed!")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_search())
