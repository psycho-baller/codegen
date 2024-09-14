import ast
import os
import networkx as nx
import json

def parse_imports(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")
    return imports

def build_import_graph(codebase_path):
    graph = nx.DiGraph()
    
    for root, _, files in os.walk(codebase_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = parse_imports(file_path)
                module_name = os.path.relpath(file_path, codebase_path).replace(os.sep, '.')[:-3]
                folder_name = os.path.relpath(root, codebase_path).split(os.sep)[0]
                graph.add_node(module_name, folder=folder_name)
                for imp in imports:
                    graph.add_edge(module_name, imp)
    
    return graph

def graph_to_json(graph):
    nodes = []
    edges = []
    for node, data in graph.nodes(data=True):
        nodes.append({
            'id': node,
            'folder': data.get('folder', 'default'),
            'size': 200 + 200 * graph.out_degree(node)
        })
    for source, target in graph.edges():
        edges.append({'source': source, 'target': target})
    return json.dumps({'nodes': nodes, 'edges': edges})

if __name__ == "__main__":
    codebase_path = "repo"
    import_graph = build_import_graph(codebase_path)
    graph_json = graph_to_json(import_graph)
    print(graph_json)