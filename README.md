# Decision Tree Analyzer

A Python package for creating, analyzing, and visualizing decision trees with expected value calculations.

## Features

- Create decision trees with decision, chance, and terminal nodes
- Calculate expected values using backward induction
- Generate Mermaid diagrams for visualization
- Find optimal paths through decision trees

## Installation

```bash
pip install dtree
```

## Quick Start
```python
from dtree import DecisionTree, NodeType

# Create a decision tree
tree = DecisionTree()

# Add nodes
tree.add_decision_node("start", "Investment Decision")
tree.add_chance_node("invest", "Market Outcome")
tree.add_terminal_node("success", "Success", 1000)
tree.add_terminal_node("failure", "Failure", -500)

# Add edges
tree.add_edge("start", "invest")
tree.add_edge("invest", "success", 0.6)
tree.add_edge("invest", "failure", 0.4)

# Calculate expected values
results = tree.calculate_expected_values()
print(results)

# Generate visualization
mermaid_code = tree.generate_mermaid_diagram()
print(mermaid_code)
```