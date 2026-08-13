# ⚡ Talent Signal — Visual Workflow Topology Compiler vs n8n

> **Structural Query Compilation Engine for MongoDB Atlas Vector Search Pipelines & Multi-Provider LLM Agents**

---

## 💡 Architectural Comparison: n8n vs Talent Signal Compiler

| Feature | n8n MongoDB Nodes | Talent Signal Topology Compiler |
| :--- | :--- | :--- |
| **Execution Model** | Static, step-by-step sequential node execution. | Abstract Syntax Tree (AST) graph compiler. |
| **Canvas Topology Impact** | Moving nodes changes the sequence of separate API calls. | Moving nodes **rewrites the generated MongoDB aggregation query structure itself**. |
| **Pre-Filter vs Post-Filter** | Requires manual configuration inside individual node parameters. | Moving a `Filter` node before `VectorSearch` on canvas automatically compiles a pre-filter `$match` stage before `$vectorSearch`. |
| **LLM Provider Swapping** | Hardcoded node instances or manual credential switching. | Zero-code config swapping (`Anthropic` ➔ `OpenAI` ➔ `Gemini`) with instant AST validation. |
| **Query Output** | Isolated individual operations (`Find`, `Aggregate`). | Single unified MongoDB Atlas Aggregation Pipeline + LLM Execution Plan. |

---

## 🌟 Key Scenarios & Capabilities

1. **Visual Graph Compilation:** Converts nodes (`dataSource`, `vectorSearch`, `filter`, `llmAgent`, `output`) and directed edges into executable MongoDB Atlas pipeline stages + LLM execution plans.
2. **Node Rewiring (Pre-Filter vs Post-Filter):**
   - **Base Workflow (`n1 -> n2 -> n3`):** `$vectorSearch` runs first, followed by post-filter `$match`.
   - **Rewired Workflow (`n1 -> n3 -> n2`):** Dragging the filter before vector search moves `$match` before `$vectorSearch`, producing a materially different pre-filter Atlas query.
3. **LLM Provider Swapping:** Swapping `config.provider` from `anthropic` (`claude-sonnet-5`) to `openai` (`gpt-4o`) or `gemini` (`gemini-2.5-flash`) with zero compiler or code changes.

---

## 🚀 Execution & Testing

### Python ADK Unit Tests
```bash
python3 -m unittest discover -s tests
```

### TypeScript Demo Execution
```bash
npx tsx src/example.ts
```
