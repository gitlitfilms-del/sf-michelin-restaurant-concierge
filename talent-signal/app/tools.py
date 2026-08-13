"""
ADK Function Tools for Talent Signal Visual Workflow Compiler
Exposes graph compilation, validation, node rewiring, and provider swapping tools to Agents CLI.
"""

from typing import Dict, Any, List
from app.compiler import compile_workflow_graph, validate_workflow_graph

# Default sample workflow graph matching example.ts
DEMO_WORKFLOW_GRAPH = {
    "id": "wf_demo",
    "name": "Talent Signal — Demo Pipeline",
    "nodes": [
        {"id": "n1", "type": "dataSource", "position": {"x": 0, "y": 0}, "config": {"collection": "employees"}},
        {"id": "n2", "type": "vectorSearch", "position": {"x": 250, "y": 0}, "config": {"index": "review_vector_index", "field": "review_embedding", "limit": 20}},
        {"id": "n3", "type": "filter", "position": {"x": 500, "y": 0}, "config": {"field": "department", "op": "eq", "value": "Platform Engineering"}},
        {"id": "n4", "type": "llmAgent", "position": {"x": 750, "y": 0}, "config": {"provider": "anthropic", "model": "claude-sonnet-5", "promptTemplate": "Summarize why these employees stand out:\n{{documents}}", "outputField": "summary"}},
        {"id": "n5", "type": "output", "position": {"x": 1000, "y": 0}, "config": {}}
    ],
    "edges": [
        {"id": "e1", "source": "n1", "target": "n2"},
        {"id": "e2", "source": "n2", "target": "n3"},
        {"id": "e3", "source": "n3", "target": "n4"},
        {"id": "e4", "source": "n4", "target": "n5"}
    ]
}

def compile_graph(graph: Dict[str, Any] = None) -> Dict[str, Any]:
    """Compiles a visual workflow graph into a MongoDB Atlas pipeline & LLM execution plan."""
    target_graph = graph or DEMO_WORKFLOW_GRAPH
    return compile_workflow_graph(target_graph)

def validate_graph(graph: Dict[str, Any] = None) -> Dict[str, Any]:
    """Validates a visual workflow graph structure for correctness."""
    target_graph = graph or DEMO_WORKFLOW_GRAPH
    errors = validate_workflow_graph(target_graph)
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def rewire_filter_before_vector_search(graph: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Simulates user dragging the Filter node BEFORE the Vector Search node on the visual canvas.
    Changes edge topology (n1 -> n3 -> n2 -> n4 -> n5) and compiles the pre-filter Atlas pipeline.
    """
    base = graph or DEMO_WORKFLOW_GRAPH
    rewired_graph = dict(base)
    rewired_graph["edges"] = [
        {"id": "e1", "source": "n1", "target": "n3"},  # dataSource -> filter
        {"id": "e2", "source": "n3", "target": "n2"},  # filter -> vectorSearch
        {"id": "e3", "source": "n2", "target": "n4"},
        {"id": "e4", "source": "n4", "target": "n5"}
    ]
    compiled = compile_workflow_graph(rewired_graph)
    return {
        "rewired_scenario": "Filter node moved before Vector Search node (Pre-filter query)",
        "compiled_plan": compiled
    }

def swap_llm_provider(node_id: str = "n4", provider: str = "openai", model: str = "gpt-4o", graph: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Swaps an LLM Agent node's provider and model (e.g. anthropic -> openai / gemini) with zero code changes.
    """
    base = graph or DEMO_WORKFLOW_GRAPH
    swapped_graph = dict(base)
    updated_nodes = []
    for node in base["nodes"]:
        if node["id"] == node_id:
            new_node = dict(node)
            new_node["config"] = dict(node["config"])
            new_node["config"]["provider"] = provider
            new_node["config"]["model"] = model
            updated_nodes.append(new_node)
        else:
            updated_nodes.append(node)
    swapped_graph["nodes"] = updated_nodes
    compiled = compile_workflow_graph(swapped_graph)
    return {
        "swapped_scenario": f"Swapped node {node_id} provider to {provider} ({model})",
        "compiled_plan": compiled
    }
