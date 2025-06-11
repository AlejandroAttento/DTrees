from typing import Dict, List, Tuple
from .models import Node, Edge, NodeType
from mermaid import Mermaid

class DecisionTree:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        
    def add_decision_node(self, node_id: str, name: str):
        """Add a decision node to the tree"""
        self.nodes[node_id] = Node(node_id, name, NodeType.DECISION)
        
    def add_chance_node(self, node_id: str, name: str):
        """Add a chance node to the tree"""
        self.nodes[node_id] = Node(node_id, name, NodeType.CHANCE)
        
    def add_terminal_node(self, node_id: str, name: str, value: float):
        """Add a terminal node to the tree"""
        self.nodes[node_id] = Node(node_id, name, NodeType.TERMINAL, value)
        
    def add_edge(self, from_node: str, to_node: str, probability: float = 1.0):
        """Add an edge between two nodes"""
        if from_node not in self.nodes:
            raise ValueError(f"From node '{from_node}' does not exist")
        if to_node not in self.nodes:
            raise ValueError(f"To node '{to_node}' does not exist")
            
        self.edges.append(Edge(from_node, to_node, probability))
        
    def get_children(self, node_id: str) -> List[Tuple[str, float]]:
        """Get all children of a node with their probabilities"""
        children = []
        for edge in self.edges:
            if edge.from_node == node_id:
                children.append((edge.to_node, edge.probability))
        return children
        
    def calculate_expected_values(self, precision: int = 2) -> Dict[str, float]:
        """
        Calculate expected values for all nodes in the tree using backward induction
        
        Args:
            precision: Number of decimal places to round the results to
            
        Returns:
            Dictionary mapping node_id to expected value
        """
        # Reset all expected values
        for node in self.nodes.values():
            node.expected_value = None
            
        def calculate_node_value(node_id: str) -> float:
            node = self.nodes[node_id]
            
            # Return cached value if already calculated
            if node.expected_value is not None:
                return node.expected_value
                
            if node.node_type == NodeType.TERMINAL:
                node.expected_value = node.value
                
            elif node.node_type == NodeType.CHANCE:
                children = self.get_children(node_id)
                expected_value = 0.0
                
                for child_id, probability in children:
                    child_value = calculate_node_value(child_id)
                    expected_value += probability * child_value
                    
                node.expected_value = expected_value
                
            elif node.node_type == NodeType.DECISION:
                children = self.get_children(node_id)
                if not children:
                    node.expected_value = 0.0
                else:
                    # For decision nodes, take the maximum expected value
                    max_value = float('-inf')
                    for child_id, _ in children:
                        child_value = calculate_node_value(child_id)
                        max_value = max(max_value, child_value)
                    node.expected_value = max_value
                    
            return node.expected_value
            
        # Calculate expected values for all nodes
        for node_id in self.nodes.keys():
            calculate_node_value(node_id)
            
        # Return results rounded to specified precision
        results = {}
        for node_id, node in self.nodes.items():
            results[node_id] = round(node.expected_value, precision)
            
        return results
        
    def print_tree_summary(self, precision: int = 2):
        """Print a summary of the tree with expected values"""
        expected_values = self.calculate_expected_values(precision)
        
        print("Decision Tree Summary:")
        print("=" * 50)
        
        for node_id, node in self.nodes.items():
            print(f"{node.node_type.value.upper()}: {node.name} ({node_id})")
            if node.node_type == NodeType.TERMINAL:
                print(f"  Terminal Value: ${node.value:.{precision}f}")
            print(f"  Expected Value: ${expected_values[node_id]:.{precision}f}")
            
            # Show children
            children = self.get_children(node_id)
            if children:
                print("  Children:")
                for child_id, prob in children:
                    child_name = self.nodes[child_id].name
                    print(f"    -> {child_name} ({child_id}) [p={prob:.{precision}f}]")
            print()
            
    def get_optimal_path(self, start_node: str, precision: int = 2) -> List[str]:
        """
        Get the optimal path from a starting node (for decision nodes)
        
        Args:
            start_node: Starting node ID
            precision: Number of decimal places for calculations
            
        Returns:
            List of node IDs representing the optimal path
        """
        expected_values = self.calculate_expected_values(precision)
        path = [start_node]
        current = start_node
        
        while True:
            node = self.nodes[current]
            children = self.get_children(current)
            
            if not children:  # Terminal node
                break
                
            if node.node_type == NodeType.DECISION:
                # Choose child with maximum expected value
                best_child = None
                best_value = float('-inf')
                
                for child_id, _ in children:
                    child_value = expected_values[child_id]
                    if child_value > best_value:
                        best_value = child_value
                        best_child = child_id
                        
                current = best_child
                path.append(current)
                
            elif node.node_type == NodeType.CHANCE:
                # For chance nodes, show the path but note it's probabilistic
                # Just take the first child for path demonstration
                current = children[0][0]
                path.append(current)
                
            else:  # Terminal
                break
                
        return path

    def generate_mermaid_diagram(self, precision: int = 2, show_expected_values: bool = True) -> str:
        """
        Generate a modern Mermaid diagram representation of the decision tree
        
        Args:
            precision: Number of decimal places for values
            show_expected_values: Whether to show expected values in nodes
            
        Returns:
            String containing the Mermaid diagram code
        """
        # Calculate expected values first
        expected_values = self.calculate_expected_values(precision)
        
        # Start with horizontal layout
        mermaid_code = ["graph LR"]
        
        # Define modern Tableau-like node styles
        mermaid_code.extend([
            # Decision nodes - Blue theme
            "    classDef decision fill:#4e79a7,stroke:#2c5f85,stroke-width:3px,color:#ffffff,font-weight:bold,font-size:12px",
            # Chance nodes - Orange theme  
            "    classDef chance fill:#f28e2c,stroke:#d4751a,stroke-width:3px,color:#ffffff,font-weight:bold,font-size:12px",
            # Terminal nodes - Green theme
            "    classDef terminal fill:#59a14f,stroke:#3f7a37,stroke-width:3px,color:#ffffff,font-weight:bold,font-size:12px",
            # Alternative modern color scheme (uncomment to use):
            # "    classDef decision fill:#1f77b4,stroke:#0d5a8a,stroke-width:3px,color:#ffffff,font-weight:bold",
            # "    classDef chance fill:#ff7f0e,stroke:#cc5500,stroke-width:3px,color:#ffffff,font-weight:bold", 
            # "    classDef terminal fill:#2ca02c,stroke:#1f7a1f,stroke-width:3px,color:#ffffff,font-weight:bold"
        ])
        
        # Add nodes with enhanced styling
        for node_id, node in self.nodes.items():
            label_parts = [f"<b>{node.name}</b>"]
            
            # Add values to label with better formatting
            if node.node_type == NodeType.TERMINAL:
                label_parts.append(f"Value: {node.value:,.{precision}f}")
            
            if show_expected_values and node_id in expected_values and node.node_type != NodeType.TERMINAL:
                label_parts.append(f"EV: {expected_values[node_id]:,.{precision}f}")
            
            # Create label with line breaks
            label = "<br/>".join(label_parts)
            
            # Determine node shape based on type with modern styling
            if node.node_type == NodeType.DECISION:
                # Rounded rectangle for decision nodes (more modern than diamond)
                mermaid_code.append(f'    {node_id}["{label}"]')
                mermaid_code.append(f"    class {node_id} decision")
            elif node.node_type == NodeType.CHANCE:
                # Stadium shape for chance nodes (modern rounded pill shape)
                mermaid_code.append(f'    {node_id}(["{label}"])')
                mermaid_code.append(f"    class {node_id} chance")
            else:  # Terminal
                # Rounded rectangle for terminal nodes
                mermaid_code.append(f'    {node_id}["{label}"]')
                mermaid_code.append(f"    class {node_id} terminal")
        
        # Add edges with enhanced styling
        for edge in self.edges:
            # Format probability label with better styling
            if edge.probability == 1.0:
                prob_label = ""
            else:
                prob_label = f"|<b>{edge.probability:.{precision}f}</b>|"
            
            # Use thicker arrows for better visibility
            mermaid_code.append(f"    {edge.from_node} ==>{prob_label} {edge.to_node}")
        
        # Add overall styling
        mermaid_code.extend([
            "    linkStyle default stroke:#666,stroke-width:2px",
            "    %%{init: {'theme':'base', 'themeVariables': {'primaryColor':'#ffffff', 'primaryTextColor':'#333333', 'primaryBorderColor':'#dddddd', 'lineColor':'#666666'}}}%%"
        ])
        
        return "\n".join(mermaid_code)
    
    def save_mermaid_diagram(self, filename: str = "decision_tree.md", precision: int = 2, 
                           show_expected_values: bool = True):
        """
        Save the Mermaid diagram to a markdown file
        
        Args:
            filename: Output filename (should end with .md)
            precision: Number of decimal places for values
            show_expected_values: Whether to show expected values in nodes
        """
        mermaid_code = self.generate_mermaid_diagram(precision, show_expected_values)
        
        markdown_content = f"""
```mermaid
{mermaid_code}
```
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Mermaid diagram saved to {filename}")

    def save_mermaid_graph(self, filename: str = "decision_tree.png", precision: int = 2, 
                           show_expected_values: bool = True):
        mermaid_code = self.generate_mermaid_diagram(precision, show_expected_values)

        mermaid = Mermaid(mermaid_code)

        mermaid.to_png("diagram.png")