import pytest
from dtree import DecisionTree, NodeType

class TestDecisionTree:
    def test_create_tree(self):
        tree = DecisionTree()
        assert len(tree.nodes) == 0
        assert len(tree.edges) == 0
    
    def test_add_nodes(self):
        tree = DecisionTree()
        tree.add_decision_node("d1", "Decision 1")
        tree.add_chance_node("c1", "Chance 1")
        tree.add_terminal_node("t1", "Terminal 1", 100)
        
        assert len(tree.nodes) == 3
        assert tree.nodes["d1"].node_type == NodeType.DECISION
        assert tree.nodes["c1"].node_type == NodeType.CHANCE
        assert tree.nodes["t1"].node_type == NodeType.TERMINAL
        assert tree.nodes["t1"].value == 100
    
    def test_add_edges(self):
        tree = DecisionTree()
        tree.add_decision_node("d1", "Decision 1")
        tree.add_terminal_node("t1", "Terminal 1", 100)
        tree.add_edge("d1", "t1")
        
        assert len(tree.edges) == 1
        assert tree.edges[0].from_node == "d1"
        assert tree.edges[0].to_node == "t1"
    
    def test_expected_value_calculation(self):
        tree = DecisionTree()
        tree.add_decision_node("start", "Start")
        tree.add_terminal_node("end", "End", 100)
        tree.add_edge("start", "end")
        
        results = tree.calculate_expected_values()
        assert results["start"] == 100
        assert results["end"] == 100