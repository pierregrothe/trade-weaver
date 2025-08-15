#!/usr/bin/env python3
"""
Debug script to test discovery functions directly
"""
import asyncio
from market_analyst.sub_agents.exchange_gapper_discovery.tools import discover_exchange_gappers
from market_analyst.sub_agents.ticker_enrichment_pipeline.tools import enrich_ticker_data

async def test_discovery():
    """Test the discovery and enrichment functions directly"""
    
    print("[DEBUG] Testing discovery functions...")
    
    # Test NASDAQ discovery
    nasdaq_result = await discover_exchange_gappers("NASDAQ")
    print(f"[OK] NASDAQ discovery: {nasdaq_result}")
    
    # Test TSX discovery  
    tsx_result = await discover_exchange_gappers("TSX")
    print(f"[OK] TSX discovery: {tsx_result}")
    
    # Test enrichment
    print("\n[DEBUG] Testing enrichment functions...")
    for ticker_data in nasdaq_result:
        enriched = await enrich_ticker_data(
            ticker=ticker_data["ticker"],
            exchange_id="NASDAQ", 
            gapper_data=ticker_data
        )
        print(f"[OK] Enriched {ticker_data['ticker']}: exchange_id={enriched['exchange_id']}")
        
    for ticker_data in tsx_result:
        enriched = await enrich_ticker_data(
            ticker=ticker_data["ticker"],
            exchange_id="TSX",
            gapper_data=ticker_data
        )
        print(f"[OK] Enriched {ticker_data['ticker']}: exchange_id={enriched['exchange_id']}")

if __name__ == "__main__":
    asyncio.run(test_discovery())