import json
import pytest
from google.genai.types import Content, Part
from trade_weaver.schemas import DailyWatchlistDocument

pytestmark = pytest.mark.asyncio

async def test_coordinator_fan_out_fan_in_workflow(root_agent, adk_test_harness):
    """
    Integration Test: Verifies the Coordinator's dynamic fan-out/fan-in workflow.

    It validates:
    1.  The Coordinator accepts a payload with a list of exchanges.
    2.  It dynamically creates and runs parallel MarketAnalystPipelines.
    3.  It correctly aggregates results from the unique state keys.
    4.  It produces a final, consolidated DailyWatchlistDocument.
    """
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="fan_out_fan_in_test",
    )

    # --- Input: Request analysis for a single exchange to avoid rate limiting ---
    payload = {
        "target_agent": "market_analyst_agent", # This is now just a routing key
        "parameters": {"exchanges": ["NASDAQ"]},
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
    assert events, "Test failed: No events were returned from the agent run."

    final_event = events[-1]
    assert final_event.author == "trading_desk_coordinator"
    assert final_event.content and final_event.content.parts

    try:
        final_payload = json.loads(final_event.content.parts[0].text)
    except (json.JSONDecodeError, IndexError):
        pytest.fail("The final event content was not valid JSON.")

    # 1. Assert the overall status is 'success'
    assert final_payload.get("status") == "success"

    # 2. Assert the result field is a valid DailyWatchlistDocument
    result_data = final_payload.get("result")
    assert isinstance(result_data, dict)
    try:
        watchlist = DailyWatchlistDocument(**result_data)
    except Exception as e:
        pytest.fail(
            "The 'result' field is not a valid DailyWatchlistDocument. "
            f"Validation error: {e}. Payload: {result_data}"
        )

    # 3. Assert the fan-out/fan-in and data structure are correct
    assert sorted(watchlist.exchanges_scanned) == ["NASDAQ"]
    assert len(watchlist.analysis_results) == 1, "Should have one result object for the single exchange."

    # Check the contents of the analysis result
    result = watchlist.analysis_results[0]
    assert result.market_regime is not None
    assert result.market_regime.exchange == "NASDAQ"
    assert isinstance(result.candidate_list, list)
    assert len(result.candidate_list) > 0, "Candidate list should not be empty."
