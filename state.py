from __future__ import annotations
from typing import Dict , List , Literal , cast , Sequence
from dataclasses import dataclass , field

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from typing_extensions import Annotated




@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage],add_messages] = field(default_factory= list)

@dataclass
class State(InputState):
    is_last_step : IsLastStep = field(default = False)