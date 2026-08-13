# ⚡ Talent Signal — Visual Workflow Compiler & Agent CLI System

> **Compiler Engine for MongoDB Atlas Vector Search Pipelines & Multi-Provider LLM Agents**

Demonstrates compiling visual node graphs into executable MongoDB Atlas aggregation pipelines, node rewiring (`$match` pre-filter vs post-filter optimization), and zero-code provider swapping.

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
npx ts-node src/example.ts
```
