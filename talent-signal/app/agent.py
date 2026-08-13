"""
Root Agent for Talent Signal Workflow Compiler
Exposes graph compilation, validation, node rewiring, and LLM provider swapping to Agents CLI.
"""

from google.adk.agents import Agent
from app.tools import (
    compile_graph,
    validate_graph,
    rewire_filter_before_vector_search,
    swap_llm_provider
)

root_agent = Agent(
    name="talent_signal_compiler_agent",
    model="gemini-2.5-flash",
    instruction="""You are the Talent Signal Visual Workflow Compiler Agent.

Your capabilities:
1. Validate visual workflow graphs (nodes, edges, config schemas).
2. Compile visual graphs into executable MongoDB Atlas aggregation pipelines ($vectorSearch, $match) and LLM agent execution stages.
3. Demonstrate node rewiring (e.g. dragging filter before vector search -> generating pre-filter vs post-filter Atlas queries).
4. Demonstrate zero-code LLM provider swapping (e.g. Anthropic claude-sonnet-5 -> OpenAI gpt-4o -> Gemini gemini-2.5-flash).""",
    tools=[
        compile_graph,
        validate_graph,
        rewire_filter_before_vector_search,
        swap_llm_provider
    ]
)
