from dotenv import load_dotenv
load_dotenv()
from datetime import UTC, datetime
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from Flight_agent.context import Context
from Flight_agent.state import InputState, State
from Flight_agent.tools import TOOLS
from Flight_agent.utils import load_chat_model



async def call_model(state: State) -> Dict[str, List[AIMessage]]:
    # hardcode context directly for now
    ctx = Context()
    model = load_chat_model(ctx.model).bind_tools(TOOLS)
    system_message = ctx.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages]
        ),
    )
    if state.is_last_step and response.tool_calls:
        return {"messages": [AIMessage(id=response.id, content="Sorry couldn't find an answer")]}
    return {"messages": [response]}
builder = StateGraph(State,input_schema=InputState)
builder.add_node(call_model)
builder.add_node("tools",ToolNode(TOOLS))

builder.add_edge("__start__","call_model")

def route_model_output(state:State)->Literal["__end__","tools"]:
    last_message = state.messages[-1]
    if not last_message.tool_calls:
        return "__end__"
    return "tools"

builder.add_conditional_edges("call_model",route_model_output)
builder.add_edge("tools","call_model")
graph = builder.compile(name="React Agent")
