#!/usr/bin/env python3
"""
Example demonstrating the utility function feature in DecisionTree
"""

import math
from dtree import DecisionTree

def main():
    # Create a decision tree with a risk-averse utility function
    # U(x) = 1 - e^(-x/100) - This is a common risk-averse utility function
    def risk_averse_utility(x):
        return 1 - math.exp(-x/100)
    
    # Create decision tree with utility function
    tree = DecisionTree(utility_function=risk_averse_utility)
    
    # Add nodes
    tree.add_decision_node("D1", "Invest in Project")
    tree.add_chance_node("C1", "Market Success")
    tree.add_chance_node("C2", "Market Failure")
    tree.add_terminal_node("T1", "High Success", 200)
    tree.add_terminal_node("T2", "Moderate Success", 100)
    tree.add_terminal_node("T3", "Low Success", 50)
    tree.add_terminal_node("T4", "Failure", -50)
    
    # Add edges
    tree.add_edge("D1", "C1", 0.6)
    tree.add_edge("D1", "C2", 0.4)
    tree.add_edge("C1", "T1", 0.3)
    tree.add_edge("C1", "T2", 0.5)
    tree.add_edge("C1", "T3", 0.2)
    tree.add_edge("C2", "T4", 1.0)
    
    # Print summary
    print("Decision Tree with Risk-Averse Utility Function")
    print("Utility Function: U(x) = 1 - e^(-x/100)")
    print("=" * 60)
    tree.print_tree_summary()
    
    # Get optimal path
    optimal_path = tree.get_optimal_path("D1")
    print("Optimal Path (using utility values):")
    for node_id in optimal_path:
        node = tree.nodes[node_id]
        print(f"  -> {node.name} ({node_id})")
    
    # Create same tree without utility function for comparison
    print("\n" + "=" * 60)
    print("Same Decision Tree WITHOUT Utility Function")
    print("=" * 60)
    
    tree_no_utility = DecisionTree()
    
    # Add nodes
    tree_no_utility.add_decision_node("D1", "Invest in Project")
    tree_no_utility.add_chance_node("C1", "Market Success")
    tree_no_utility.add_chance_node("C2", "Market Failure")
    tree_no_utility.add_terminal_node("T1", "High Success", 200)
    tree_no_utility.add_terminal_node("T2", "Moderate Success", 100)
    tree_no_utility.add_terminal_node("T3", "Low Success", 50)
    tree_no_utility.add_terminal_node("T4", "Failure", -50)
    
    # Add edges
    tree_no_utility.add_edge("D1", "C1", 0.6)
    tree_no_utility.add_edge("D1", "C2", 0.4)
    tree_no_utility.add_edge("C1", "T1", 0.3)
    tree_no_utility.add_edge("C1", "T2", 0.5)
    tree_no_utility.add_edge("C1", "T3", 0.2)
    tree_no_utility.add_edge("C2", "T4", 1.0)
    
    tree_no_utility.print_tree_summary()
    
    # Generate diagrams
    tree.generate_mermaid_diagram()
    tree.save_mermaid_diagram("decision_tree_with_utility.md")
    
    tree_no_utility.generate_mermaid_diagram()
    tree_no_utility.save_mermaid_diagram("decision_tree_no_utility.md")
    
    print("\nDiagrams saved:")
    print("- decision_tree_with_utility.md (with utility function)")
    print("- decision_tree_no_utility.md (without utility function)")

if __name__ == "__main__":
    main() 