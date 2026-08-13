"""
Talent Signal Workflow Compiler (Python ADK Edition)
Compiles visual node graphs into executable MongoDB Atlas aggregation pipelines and LLM Agent execution plans.
"""

from typing import List, Dict, Any, Tuple

def validate_workflow_graph(graph: Dict[str, Any]) -> List[str]:
    """Validates a workflow graph for required node configs and valid edges."""
    errors = []
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    if not graph.get("id"):
        errors.append("Workflow graph missing 'id'.")
    if not nodes:
        errors.append("Workflow graph must contain at least one node.")

    node_ids = {n["id"] for n in nodes if "id" in n}

    for edge in edges:
        if edge.get("source") not in node_ids:
            errors.append(f"Edge {edge.get('id')} references missing source node {edge.get('source')}.")
        if edge.get("target") not in node_ids:
            errors.append(f"Edge {edge.get('id')} references missing target node {edge.get('target')}.")

    for node in nodes:
        node_id = node.get("id", "unknown")
        node_type = node.get("type")
        config = node.get("config", {})

        if node_type == "dataSource" and not config.get("collection"):
            errors.append(f"Node {node_id} (dataSource) requires 'collection' in config.")
        elif node_type == "vectorSearch" and (not config.get("index") or not config.get("field")):
            errors.append(f"Node {node_id} (vectorSearch) requires 'index' and 'field' in config.")
        elif node_type == "filter" and (not config.get("field") or not config.get("op")):
            errors.append(f"Node {node_id} (filter) requires 'field' and 'op' in config.")
        elif node_type == "llmAgent" and (not config.get("provider") or not config.get("model")):
            errors.append(f"Node {node_id} (llmAgent) requires 'provider' and 'model' in config.")

    return errors

def get_topological_order(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Sorts workflow nodes topologically based on directed edge connections."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    in_degree = {n["id"]: 0 for n in nodes}
    adj = {n["id"]: [] for n in nodes}
    node_map = {n["id"]: n for n in nodes}

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src in adj:
            adj[src].append(tgt)
            in_degree[tgt] = in_degree.get(tgt, 0) + 1

    queue = [n_id for n_id, deg in in_degree.items() if deg == 0]
    sorted_nodes = []

    while queue:
        curr_id = queue.pop(0)
        sorted_nodes.append(node_map[curr_id])
        for neighbor_id in adj.get(curr_id, []):
            in_degree[neighbor_id] -= 1
            if in_degree[neighbor_id] == 0:
                queue.append(neighbor_id)

    return sorted_nodes if len(sorted_nodes) == len(nodes) else nodes

def compile_workflow_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    """Compiles a visual workflow graph into an executable MongoDB Atlas pipeline & LLM execution plan."""
    validation_errors = validate_workflow_graph(graph)
    if validation_errors:
        return {
            "status": "error",
            "errors": validation_errors
        }

    sorted_nodes = get_topological_order(graph)
    pipeline = []
    llm_stages = []
    execution_order = []

    for node in sorted_nodes:
        n_id = node["id"]
        n_type = node["type"]
        config = node.get("config", {})
        execution_order.append(f"{n_id} ({n_type})")

        if n_type == "vectorSearch":
            limit = config.get("limit", 10)
            pipeline.append({
                "$vectorSearch": {
                    "index": config.get("index"),
                    "path": config.get("field", "embedding"),
                    "queryVector": "[DYNAMIC_EMBEDDING_VECTOR]",
                    "numCandidates": limit * 5,
                    "limit": limit
                }
            })
        elif n_type == "filter":
            op = config.get("op", "eq")
            mongo_op = "$eq" if op == "eq" else f"${op}"
            pipeline.append({
                "$match": {
                    config.get("field"): {mongo_op: config.get("value")}
                }
            })
        elif n_type == "llmAgent":
            llm_stages.append({
                "stageType": "llmAgent",
                "stageName": n_id,
                "provider": config.get("provider"),
                "model": config.get("model"),
                "promptTemplate": config.get("promptTemplate", ""),
                "outputField": config.get("outputField", "output")
            })

    return {
        "status": "success",
        "workflowId": graph.get("id"),
        "workflowName": graph.get("name"),
        "pipeline": pipeline,
        "llmStages": llm_stages,
        "executionOrder": execution_order
    }
