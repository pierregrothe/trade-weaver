# /market_analyst/tools.py
from typing import List, Dict, Any

from google.adk.events import Event
from google.genai import types
import json

def cluster_instruments(instruments: List[Dict[str, Any]]) -> Event:
    """
    Clusters a list of enriched instruments.
    This is a mockup function that adds a mock correlation_cluster_id.
    """
    print("Clustering instruments...")
    # Sort by ticker for deterministic output
    instruments.sort(key=lambda x: x["ticker"])
    for i, instrument in enumerate(instruments):
        instrument["correlation_cluster_id"] = i % 2
    return Event(
        author="cluster_instruments",
        content=types.Content(
            parts=[
                types.Part(
                    text=json.dumps({"clustered_instruments": instruments})
                )
            ]
        ),
    )
