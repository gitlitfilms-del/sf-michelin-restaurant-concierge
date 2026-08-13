// Demonstrates: (1) compiling a simple workflow, (2) what happens to the compiled
// output when a node is rewired — the exact "move node → different Atlas query" case
// from the dev plan — and (3) swapping an LLM Agent node's provider with no code change.

import { compile, validate } from "./compiler";
import type { WorkflowGraph } from "./types";

const baseWorkflow: WorkflowGraph = {
  id: "wf_demo",
  name: "Talent Signal — Demo Pipeline",
  nodes: [
    { id: "n1", type: "dataSource", position: { x: 0, y: 0 }, config: { collection: "employees" } },
    {
      id: "n2",
      type: "vectorSearch",
      position: { x: 250, y: 0 },
      config: { index: "review_vector_index", field: "review_embedding", limit: 20 },
    },
    {
      id: "n3",
      type: "filter",
      position: { x: 500, y: 0 },
      config: { field: "department", op: "eq", value: "Platform Engineering" },
    },
    {
      id: "n4",
      type: "llmAgent",
      position: { x: 750, y: 0 },
      config: {
        provider: "anthropic",
        model: "claude-sonnet-5",
        promptTemplate: "Summarize why these employees stand out:\n{{documents}}",
        outputField: "summary",
      },
    },
    { id: "n5", type: "output", position: { x: 1000, y: 0 }, config: {} },
  ],
  edges: [
    { id: "e1", source: "n1", target: "n2" },
    { id: "e2", source: "n2", target: "n3" },
    { id: "e3", source: "n3", target: "n4" },
    { id: "e4", source: "n4", target: "n5" },
  ],
};

console.log("=== Base workflow: validate ===");
console.log(validate(baseWorkflow)); // expect []

console.log("\n=== Base workflow: compiled plan ===");
console.log(JSON.stringify(compile(baseWorkflow), (k, v) => (k === "run" ? "[fn]" : v), 2));

// --- Scenario: user drags the Filter node BEFORE the Vector Search node on the canvas ---
// This is the exact interaction described in the dev plan. Only the edges change;
// the compiler produces a structurally different Atlas pipeline as a result.

const rewired: WorkflowGraph = {
  ...baseWorkflow,
  edges: [
    { id: "e1", source: "n1", target: "n3" }, // dataSource -> filter (now first)
    { id: "e2", source: "n3", target: "n2" }, // filter -> vectorSearch (now second)
    { id: "e3", source: "n2", target: "n4" },
    { id: "e4", source: "n4", target: "n5" },
  ],
};

console.log("\n=== Rewired workflow (filter moved before vector search): compiled plan ===");
console.log(JSON.stringify(compile(rewired), (k, v) => (k === "run" ? "[fn]" : v), 2));
// Note the $match stage now precedes $vectorSearch in the pipeline array — a materially
// different query (pre-filter vs post-filter), generated purely from moving one edge.

// --- Scenario: swap the LLM Agent's provider from Anthropic to OpenAI ---
// No compiler or handler code changes — only the node's config.provider value.

const swappedProvider: WorkflowGraph = {
  ...baseWorkflow,
  nodes: baseWorkflow.nodes.map((n) =>
    n.id === "n4" ? { ...n, config: { ...n.config, provider: "openai", model: "gpt-4o" } } : n
  ),
};

console.log("\n=== Provider swapped (anthropic -> openai): validate ===");
console.log(validate(swappedProvider)); // still []
