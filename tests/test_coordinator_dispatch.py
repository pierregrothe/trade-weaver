import json
import pytest
from google.genai.types import Content, Part
from trade_weaver.schemas import DailyWatchlistDocument

pytestmark = pytest.mark.asyncio


async def test_coordinator_happy_path_workflow(root_agent, adk_test_harness):
    """
    Integration Test: Verifies the Coordinator's dynamic fan-out/fan-in workflow
    on a successful, "happy path" run.
    """
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="happy_path_test",
    )

    payload = {
        "target_agent": "market_analyst_agent",
        "parameters": {"exchanges": ["NASDAQ"]},
    }
    content = Content(parts=[Part(text=json.dumps(payload))])

    events = [
        event
        async for event in runner.run_async(
            session_id=session.id, user_id="test_user", new_message=content
        )
    ]

    assert events, "Test failed: No events were returned."
    final_event = events[-1]
    assert final_event.author == "trading_desk_coordinator"
    assert final_event.content and final_event.content.parts

    final_payload = json.loads(final_event.content.parts[0].text)
    assert final_payload.get("status") == "success"

    result_data = final_payload.get("result")
    assert isinstance(result_data, dict)
    watchlist = DailyWatchlistDocument(**result_data)

    assert sorted(watchlist.exchanges_scanned) == ["NASDAQ"]
    assert len(watchlist.analysis_results) == 1
    result = watchlist.analysis_results[0]
    assert result.market_regime.exchange == "NASDAQ"
    assert len(result.candidate_list) > 0


async def test_coordinator_handles_all_pipelines_failing(root_agent, adk_test_harness):
    """
    Integration Test: Verifies the Coordinator's error handling when all
    dynamically created pipelines fail to produce a result.
    """
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
