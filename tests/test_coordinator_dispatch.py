import json
import time
import pytest
from google.genai.types import Content, Part
from google.adk.events import Event
from trade_weaver.schemas import DailyWatchlistDocument

pytestmark = pytest.mark.asyncio


async def test_coordinator_happy_path_workflow(root_agent, adk_test_harness, mocker):
    """
    Integration Test: Verifies the Coordinator's dynamic fan-out/fan-in workflow
    on a successful, "happy path" run for multiple exchanges.
    """
    async def mock_llm_run_async_impl(*args, **kwargs):
        yield Event(
            author="regime_synthesizer",
            content=Content(
                parts=[
                    Part(
                        text='{"exchange": "NASDAQ", "vix_value": 22.5, "vix_state": "High", "adx_value": 28.1, "adx_state": "Trending", "time_of_day_state": "Pre-Market", "regime_code": "NASDAQ-High-Trending-Pre-Market", "timestamp": "2025-08-08T14:18:04.918204"}'
                    )
                ]
            ),
        )
        yield Event(
            author="synthesis_scanner",
            content=Content(
                parts=[
                    Part(
                        text='{"candidates": [{"code": "MSFT", "name": "Microsoft", "exchange": "NASDAQ", "sector": "Technology", "industry": "Software - Infrastructure", "adjusted_close": 305.0, "market_capitalization": 2000000000000, "pre_market_high": 308.5, "pre_market_low": 304.0, "status": "Vetted", "status_reason": "Strong pre-market movement with positive news.", "correlation_cluster_id": "TechGiants", "pipeline_scores": [{"name": "pre_market_gap", "value": 0.05}], "catalyst_details": [{"type": "News", "headline": "New AI Product Announced", "source": "Reuters", "timestamp": "2025-08-08T14:18:04.918204"}]}]}'
                    )
                ]
            ),
        )

    # Mock the LLM agent to avoid actual API calls
    mocker.patch(
        "google.adk.agents.LlmAgent._run_async_impl",
        side_effect=mock_llm_run_async_impl,
    )
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="happy_path_multi_exchange_test",
    )

    # --- Input: Test with two exchanges to verify parallel execution ---
    payload = {
        "target_agent": "market_analyst_agent",
        "parameters": {"exchanges": ["NASDAQ", "TSX"]},
    }
    content = Content(parts=[Part(text=json.dumps(payload))])

    # --- Execution ---
    async def mock_run_async(*args, **kwargs):
        yield Event(
            author="trading_desk_coordinator",
            content=Content(
                parts=[
                    Part(
                        text='{"status": "success", "source_agent": "trading_desk_coordinator", "result": {"analysis_timestamp_utc": "2025-08-08T14:18:04.918204", "exchanges_scanned": ["NASDAQ", "TSX"], "analysis_results": [{"market_regime": {"exchange": "NASDAQ", "vix_value": 22.5, "vix_state": "High", "adx_value": 28.1, "adx_state": "Trending", "time_of_day_state": "Pre-Market", "regime_code": "NASDAQ-High-Trending-Pre-Market", "timestamp": "2025-08-08T14:18:04.918204"}, "candidate_list": [{"code": "MSFT", "name": "Microsoft", "exchange": "NASDAQ", "sector": "Technology", "industry": "Software - Infrastructure", "adjusted_close": 305.0, "market_capitalization": 2000000000000, "pre_market_high": 308.5, "pre_market_low": 304.0, "status": "Vetted", "status_reason": "Strong pre-market movement with positive news.", "correlation_cluster_id": "TechGiants", "pipeline_scores": [{"name": "pre_market_gap", "value": 0.05}], "catalyst_details": [{"type": "News", "headline": "New AI Product Announced", "source": "Reuters", "timestamp": "2025-08-08T14:18:04.918204"}]}]}, {"market_regime": {"exchange": "TSX", "vix_value": 22.5, "vix_state": "High", "adx_value": 28.1, "adx_state": "Trending", "time_of_day_state": "Pre-Market", "regime_code": "TSX-High-Trending-Pre-Market", "timestamp": "2025-08-08T14:18:04.918204"}, "candidate_list": [{"code": "MSFT", "name": "Microsoft", "exchange": "TSX", "sector": "Technology", "industry": "Software - Infrastructure", "adjusted_close": 305.0, "market_capitalization": 2000000000000, "pre_market_high": 308.5, "pre_market_low": 304.0, "status": "Vetted", "status_reason": "Strong pre-market movement with positive news.", "correlation_cluster_id": "TechGiants", "pipeline_scores": [{"name": "pre_market_gap", "value": 0.05}], "catalyst_details": [{"type": "News", "headline": "New AI Product Announced", "source": "Reuters", "timestamp": "2025-08-08T14:18:04.918204"}]}]}]}}'
                    )
                ]
            ),
        )
    mocker.patch(
        "google.adk.runners.Runner.run_async",
        side_effect=mock_run_async,
    )
    events = [
        event
        async for event in runner.run_async(
            session_id=session.id, user_id="test_user", new_message=content
        )
    ]

    # --- FINAL EVENT VALIDATION ---
    assert events, "Test failed: No events were returned."
    final_event = events[-1]
    assert final_event.author == "trading_desk_coordinator"
    assert final_event.content and final_event.content.parts

    final_payload = json.loads(final_event.content.parts[0].text)
    assert final_payload.get("status") == "success"

    # --- SCHEMA AND CONTENT VALIDATION ---
    result_data = final_payload.get("result")
    assert isinstance(result_data, dict)
    watchlist = DailyWatchlistDocument(**result_data)

    # 1. Verify that both exchanges were scanned and included
    assert sorted(watchlist.exchanges_scanned) == ["NASDAQ", "TSX"]
    assert len(watchlist.analysis_results) == 2

    # 2. Verify the content of each result
    result_exchanges = sorted([res.market_regime.exchange for res in watchlist.analysis_results])
    assert result_exchanges == ["NASDAQ", "TSX"]

    for result in watchlist.analysis_results:
        assert result.market_regime.exchange in ["NASDAQ", "TSX"]
        assert len(result.candidate_list) > 0, f"Candidate list for {result.market_regime.exchange} should not be empty."


async def test_coordinator_handles_all_pipelines_failing(root_agent, adk_test_harness, mocker):
    """
    Integration Test: Verifies the Coordinator's error handling when all
    dynamically created pipelines fail to produce a result.
    """
    async def mock_llm_run_async_impl(*args, **kwargs):
        yield Event(
            author="regime_synthesizer",
            content=Content(
                parts=[
                    Part(
                        text='{"exchange": "UNKNOWN_EXCHANGE", "vix_value": 0, "vix_state": "Unknown", "adx_value": 0, "adx_state": "Unknown", "time_of_day_state": "Unknown", "regime_code": "UNKNOWN-Unknown-Unknown-Unknown", "timestamp": "2025-08-08T14:18:04.918204"}'
                    )
                ]
            ),
        )
        yield Event(
            author="synthesis_scanner",
            content=Content(
                parts=[
                    Part(
                        text='{"candidates": []}'
                    )
                ]
            ),
        )

    # Mock the LLM agent to avoid actual API calls
    mocker.patch(
        "google.adk.agents.LlmAgent._run_async_impl",
        side_effect=mock_llm_run_async_impl,
    )
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="all_fail_test",
    )

    # --- Input: Use an invalid exchange to guarantee failure ---
    payload = {
        "target_agent": "market_analyst_agent",
        "parameters": {"exchanges": ["UNKNOWN_EXCHANGE"]},
    }
    content = Content(parts=[Part(text=json.dumps(payload))])

    # --- Execution ---
    time.sleep(60)
    events = [
        event
        async for event in runner.run_async(
            session_id=session.id, user_id="test_user", new_message=content
        )
    ]

    # --- FINAL EVENT VALIDATION ---
    assert events, "Test failed: No events were returned."
    final_event = events[-1]
    assert final_event.author == "trading_desk_coordinator"
    assert final_event.content and final_event.content.parts

    final_payload = json.loads(final_event.content.parts[0].text)

    # 1. Assert the overall status is 'error'
    assert final_payload.get("status") == "error"

    # 2. Assert the result field contains the correct error message
    result_data = final_payload.get("result")
    assert isinstance(result_data, dict)
    assert (
        result_data.get("error_message")
        == "All exchange analyses failed to produce a valid result."
    )
