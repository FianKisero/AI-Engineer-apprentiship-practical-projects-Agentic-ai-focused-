# AI Agent Project

This project contains a simple agent script that can either:
- use OpenAI when an API key is available and quota is present, or
- fall back to a local summary when no API key or quota is available.

## Run it

From the repository root:

```bash
python agent.py
```

Or from the project folder:

```bash
cd first-ai-agent
python agent.py
```

## Notes

- The project expects a local environment file at `first-ai-agent/.env` if you want to use OpenAI.
- If your OpenAI account has no available credits or quota, the script will fall back to a local summary automatically.
- Do not commit your `.env` file.
