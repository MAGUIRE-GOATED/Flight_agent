from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated

from Flight_agent import prompts

@dataclass(kw_only=True)
class Context:
    system_prompt : str = field ( 
        default= prompts.SYSTEM_PROMPT,
        metadata = {
            "description" : "Tells the agent how to behave and interact with the user"
        }
    )
    model : Annotated[str,{"__template_metadata__": {"kind": "llm"}}] = field(
        default = "groq/llama-3.3-70b-versatile",
        metadata = {
            "description": "Tells the agent which model to use"
        }
    )
    max_search_results : int = field(
        default = 10 ,
        metadata = {
            "description" : "max number of search results before answering a search query"
        }

    )

    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args."""
        for f in fields(self):
            if not f.init:
                continue

            if getattr(self, f.name) == f.default:
                setattr(self, f.name, os.environ.get(f.name.upper(), f.default))

    


    