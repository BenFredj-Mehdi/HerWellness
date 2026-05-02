"""
Static frontend placeholder for HerWellness.

This file was intentionally emptied by the developer to remove backend AI
functionality. The website now runs as a static frontend only. If you need
to re-enable a backend later, restore or replace this module with a FastAPI
app that exposes the required endpoints.
"""

if __name__ == '__main__':
    print("agent.py disabled — static frontend only.")

        # Call Groq LLM with streaming for low latency
        full_response = ""
        with GROQ_CLIENT.messages.stream(
            """
            agent.py

            Intentionally minimal placeholder. The project is configured as a static
            frontend only; backend AI and API endpoints have been removed.

            If you later choose to re-enable a backend, replace this file with a proper
            FastAPI (or other) server implementation and restore any required
            dependencies in requirements.txt.
            """

            if __name__ == '__main__':
                print('agent.py disabled — static frontend only.')
        return await local_rule_reply(session_id, prompt)
