# Architecture

Every agent has 7 components:

- **context.py** — agent behaviour, personality and settings (system prompt, model name)
- **graph.py** — the brain, defines the ReAct loop and decision making
- **tools.py** — the hands, functions the agent can call to interact with the world
- **state.py** — conversation memory, tracks messages across turns

Helper files:
- **prompts.py** — stores system prompt templates
- **utils.py** — helper functions (model loader etc.)
- **__init__.py** — exposes only graph as the public interface

Think of it like a car — graph is the steering wheel (what you interact with), 
everything else is the engine running internally.
