# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import unittest
from unittest.mock import patch

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from trade_weaver.agents.root import TradingDeskCoordinator


class TestTradingDeskCoordinator(unittest.TestCase):
    def test_agent_invocation(self):
        """Test that the TradingDeskCoordinator agent can be invoked."""
        session_service = InMemorySessionService()
        runner = Runner(
            agent=TradingDeskCoordinator,
            session_service=session_service,
            app_name="trade_weaver_test",
        )

        async def run_test():
            session = await session_service.create_session(
                app_name="trade_weaver_test", user_id="test_user"
            )
            
            # Mock the LLM response to avoid actual API calls
            mock_response = unittest.mock.Mock()
            mock_response.candidates = [unittest.mock.Mock()]
            mock_response.candidates[0].content.parts = [unittest.mock.Mock()]
            mock_response.candidates[0].content.parts[0].text = "Acknowledged."

            with patch(
                "google.generativeai.GenerativeModel.generate_content_async",
                return_value=mock_response,
            ):
                response_generator = runner.run_async(
                    session_id=session.session_id,
                    user_id=session.user_id,
                    new_message=types.Content(
                        role="user", parts=[types.Part(text="Hello")]
                    ),
                )
                
                final_response = None
                async for event in response_generator:
                    if event.is_final_response():
                        final_response = event.content.parts[0].text
                
                self.assertEqual(final_response, "Acknowledged.")

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
