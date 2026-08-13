"""
Unit tests for Talent Signal Workflow Compiler
"""

import unittest
from app.compiler import compile_workflow_graph, validate_workflow_graph
from app.tools import (
    DEMO_WORKFLOW_GRAPH,
    compile_graph,
    validate_graph,
    rewire_filter_before_vector_search,
    swap_llm_provider
)

class TestWorkflowCompiler(unittest.TestCase):
    def test_validation_base_workflow(self):
        res = validate_graph()
        self.assertTrue(res["valid"])
        self.assertEqual(len(res["errors"]), 0)

    def test_base_workflow_compilation(self):
        compiled = compile_graph()
        self.assertEqual(compiled["status"], "success")
        self.assertEqual(len(compiled["pipeline"]), 2)
        # Check that stage 0 is $vectorSearch and stage 1 is $match
        self.assertIn("$vectorSearch", compiled["pipeline"][0])
        self.assertIn("$match", compiled["pipeline"][1])
        self.assertEqual(len(compiled["llmStages"]), 1)
        self.assertEqual(compiled["llmStages"][0]["provider"], "anthropic")

    def test_rewire_filter_before_vector_search(self):
        res = rewire_filter_before_vector_search()
        plan = res["compiled_plan"]
        self.assertEqual(plan["status"], "success")
        # In pre-filter pipeline, $match precedes $vectorSearch
        self.assertIn("$match", plan["pipeline"][0])
        self.assertIn("$vectorSearch", plan["pipeline"][1])

    def test_swap_llm_provider(self):
        res = swap_llm_provider(node_id="n4", provider="openai", model="gpt-4o")
        plan = res["compiled_plan"]
        self.assertEqual(plan["status"], "success")
        self.assertEqual(plan["llmStages"][0]["provider"], "openai")
        self.assertEqual(plan["llmStages"][0]["model"], "gpt-4o")

if __name__ == "__main__":
    unittest.main()
