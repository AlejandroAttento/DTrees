#!/usr/bin/env python3
"""
Comprehensive examples demonstrating different utility functions in DecisionTree
"""

import math
from dtree import DecisionTree

def risk_averse_utility(x):
    """Risk-averse utility function: U(x) = 1 - e^(-x/100)"""
    return 1 - math.exp(-x/100)

def risk_seeking_utility(x):
    """Risk-seeking utility function: U(x) = x^2 / 10000"""
    return x**2 / 10000

def linear_utility(x):
    """Linear utility function: U(x) = x/100"""
    return x/100

def logarithmic_utility(x):
    """Logarithmic utility function: U(x) = sign(x) * log(1 + |x|/10)"""
    if x >= 0:
        return math.log(1 + x/10)
    else:
        return -math.log(1 + abs(x)/10)

def main():
    # Create a simple decision tree structure
    def create_tree(utility_func=None):
        tree = DecisionTree(utility_function=utility_func)
        
        # Add nodes
        tree.add_decision_node("D1", "Choose Investment")
        tree.add_chance_node("C1", "High Risk")
        tree.add_chance_node("C2", "Low Risk")
        tree.add_terminal_node("T1", "Big Win", 300)
        tree.add_terminal_node("T2", "Small Win", 100)
        tree.add_terminal_node("T3", "Small Loss", -50)
        tree.add_terminal_node("T4", "Big Loss", -200)
        
        # Add edges
        tree.add_edge("D1", "C1", 0.5)
        tree.add_edge("D1", "C2", 0.5)
        tree.add_edge("C1", "T1", 0.3)
        tree.add_edge("C1", "T3", 0.7)
        tree.add_edge("C2", "T2", 0.8)
        tree.add_edge("C2", "T4", 0.2)
        
        return tree
    
    # Test different utility functions
    utility_functions = [
        ("No Utility Function", None),
        ("Linear Utility", linear_utility),
        ("Risk-Averse Utility", risk_averse_utility),
        ("Risk-Seeking Utility", risk_seeking_utility),
        ("Logarithmic Utility", logarithmic_utility),
    ]
    
    for name, utility_func in utility_functions:
        print(f"\n{'='*60}")
        print(f"DECISION TREE WITH {name.upper()}")
        print(f"{'='*60}")
        
        tree = create_tree(utility_func)
        tree.print_tree_summary()
        
        # Get optimal path
        optimal_path = tree.get_optimal_path("D1")
        print("Optimal Path:")
        for node_id in optimal_path:
            node = tree.nodes[node_id]
            print(f"  -> {node.name} ({node_id})")
    
    # Demonstrate the impact on decision making
    print(f"\n{'='*60}")
    print("IMPACT ON DECISION MAKING")
    print(f"{'='*60}")
    
    # Create a tree with high risk vs low risk choice
    def create_risk_choice_tree(utility_func=None):
        tree = DecisionTree(utility_function=utility_func)
        
        # Add nodes
        tree.add_decision_node("D1", "Investment Choice")
        tree.add_decision_node("D2", "High Risk Strategy")
        tree.add_decision_node("D3", "Low Risk Strategy")
        tree.add_chance_node("C1", "Market Boom")
        tree.add_chance_node("C2", "Market Bust")
        tree.add_chance_node("C3", "Stable Market")
        tree.add_terminal_node("T1", "High Success", 500)
        tree.add_terminal_node("T2", "High Failure", -300)
        tree.add_terminal_node("T3", "Moderate Success", 150)
        tree.add_terminal_node("T4", "Moderate Failure", -50)
        
        # Add edges
        tree.add_edge("D1", "D2", 1.0)
        tree.add_edge("D1", "D3", 1.0)
        tree.add_edge("D2", "C1", 1.0)
        tree.add_edge("D2", "C2", 1.0)
        tree.add_edge("D3", "C3", 1.0)
        tree.add_edge("C1", "T1", 0.4)
        tree.add_edge("C1", "T2", 0.6)
        tree.add_edge("C2", "T2", 1.0)
        tree.add_edge("C3", "T3", 0.7)
        tree.add_edge("C3", "T4", 0.3)
        
        return tree
    
    print("\nRisk Choice Analysis:")
    print("-" * 40)
    
    for name, utility_func in utility_functions:
        tree = create_risk_choice_tree(utility_func)
        expected_values = tree.calculate_expected_values()
        
        # Get the expected values for the two strategies
        high_risk_ev = expected_values.get("D2", 0)
        low_risk_ev = expected_values.get("D3", 0)
        
        print(f"{name}:")
        print(f"  High Risk Strategy: {high_risk_ev:.3f}")
        print(f"  Low Risk Strategy:  {low_risk_ev:.3f}")
        print(f"  Recommended: {'High Risk' if high_risk_ev > low_risk_ev else 'Low Risk'}")
        print()

if __name__ == "__main__":
    main() 