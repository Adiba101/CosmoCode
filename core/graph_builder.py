import os
import hashlib


class GalaxyGraphBuilder:
    """Builds graph structure from parsed code files with metrics and dependency analysis."""
    
    @staticmethod
    def detect_circular_dependencies(edges):
        """Detect circular dependencies using DFS with colors.
        Returns count of circular dependencies found."""
        # Build adjacency list for dependency edges only
        graph = {}
        for edge in edges:
            if edge["type"] == "dependency":
                source = edge["source"]
                target = edge["target"]
                if source not in graph:
                    graph[source] = []
                graph[source].append(target)
        
        # Track visited states: 0 = unvisited, 1 = visiting, 2 = visited
        states = {}
        cycles_found = 0
        
        def has_cycle(node, path):
            nonlocal cycles_found
            if node in states:
                if states[node] == 1:  # Back edge found - cycle detected
                    cycles_found += 1
                    return True
                return False
            
            states[node] = 1  # Mark as visiting
            
            for neighbor in graph.get(node, []):
                if has_cycle(neighbor, path + [node]):
                    pass
            
            states[node] = 2  # Mark as visited
            return False
        
        # Check all nodes for cycles
        for node in graph:
            if node not in states:
                has_cycle(node, [])
        
        return min(cycles_found, 10)  # Cap at 10 to avoid huge numbers
    
    @staticmethod
    def calculate_dependency_depth(edges, nodes):
        """Calculate maximum dependency depth (longest dependency chain).
        Returns the depth as a float. Handles circular dependencies gracefully."""
        # Build adjacency list for dependencies
        graph = {}
        in_degree = {}
        
        for node in nodes:
            node_id = node["id"]
            in_degree[node_id] = 0
            graph[node_id] = []
        
        for edge in edges:
            if edge["type"] == "dependency":
                source = edge["source"]
                target = edge["target"]
                if source not in graph:
                    graph[source] = []
                if target not in in_degree:
                    in_degree[target] = 0
                graph[source].append(target)
                in_degree[target] += 1
        
        # Find root nodes (no incoming dependencies)
        roots = [node_id for node_id in graph if in_degree.get(node_id, 0) == 0]
        
        # If no roots (circular dependency), compute depth from all unvisited nodes
        if not roots:
            roots = list(graph.keys())
        
        if not roots:
            return 0.0
        
        # DFS to find maximum depth from each root, with cycle detection
        max_depth = 0
        global_visited = set()
        
        def dfs_depth(node, current_depth, path_visited):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            for neighbor in graph.get(node, []):
                # Skip if we've hit a cycle in this path
                if neighbor in path_visited:
                    continue
                # Mark as visited for this path
                path_visited.add(neighbor)
                dfs_depth(neighbor, current_depth + 1, path_visited)
                path_visited.discard(neighbor)
        
        for root in roots:
            if root not in global_visited:
                global_visited.add(root)
                path_visited = {root}
                dfs_depth(root, 1, path_visited)
        
        return float(max_depth)

    @staticmethod
    def build_graph(files_data):
        """Build a galaxy graph from parsed file data."""
        nodes = []
        edges = []
        
        # Summaries for Counts
        summary = {
            "stars": 0,       # Classes
            "planets": 0,     # Functions
            "orbits": 0,      # Dependencies
            "blackholes": 0,  # Bugs
            "loc": 0,
            "avgCoverage": 0,
            "avgComplexity": 0
        }
        
        node_map = {}
        total_coverage = 0
        total_complexity = 0
        valid_files_count = 0
        
        # First Pass: Register all file nodes (Stars)
        for filepath, data in files_data.items():
            valid_files_count += 1
            summary["loc"] += data["loc"]
            total_coverage += data["coverage"]
            total_complexity += data["complexity"]
            
            # Group classes as stars
            if data["classes"]:
                for cls in data["classes"]:
                    summary["stars"] += 1
                    node_id = f"class:{filepath}:{cls['name']}"
                    node = {
                        "id": node_id,
                        "name": cls["name"],
                        "type": "star",
                        "filepath": filepath,
                        "language": data["language"],
                        "loc": data["loc"],
                        "coverage": data["coverage"],
                        "complexity": data["complexity"],
                        "line": cls["line"],
                        "bugsCount": len(data["bugs"]),
                        "workSignalsCount": int(hashlib.md5(cls["name"].encode()).hexdigest()[:1], 16) % 4
                    }
                    nodes.append(node)
                    node_map[cls["name"]] = node_id
            else:
                # File itself counts as a star if no classes defined
                summary["stars"] += 1
                base_name = os.path.basename(filepath)
                node_id = f"file:{filepath}:{base_name}"
                node = {
                    "id": node_id,
                    "name": base_name,
                    "type": "star",
                    "filepath": filepath,
                    "language": data["language"],
                    "loc": data["loc"],
                    "coverage": data["coverage"],
                    "complexity": data["complexity"],
                    "line": 1,
                    "bugsCount": len(data["bugs"]),
                    "workSignalsCount": int(hashlib.md5(base_name.encode()).hexdigest()[:1], 16) % 4
                }
                nodes.append(node)
                node_map[base_name] = node_id

            # Functions as planets orbiting their file's classes
            for func in data["functions"]:
                summary["planets"] += 1
                func_id = f"func:{filepath}:{func['name']}"
                # Parent star is the first class in the file, or the file star itself
                parent_id = f"class:{filepath}:{data['classes'][0]['name']}" if data["classes"] else f"file:{filepath}:{os.path.basename(filepath)}"
                
                node = {
                    "id": func_id,
                    "name": func["name"],
                    "type": "planet",
                    "filepath": filepath,
                    "language": data["language"],
                    "parentStar": parent_id,
                    "paramCount": func["paramCount"],
                    "isPublic": func["isPublic"],
                    "complexity": max(1, data["complexity"] // (len(data["functions"]) or 1)),
                    "line": func["line"]
                }
                nodes.append(node)
                # Link planet to parent star
                edges.append({
                    "source": parent_id,
                    "target": func_id,
                    "type": "orbit"
                })

            # Bugs as Black Holes
            for bug in data["bugs"]:
                summary["blackholes"] += 1
                bug_id = f"bug:{filepath}:{bug['category']}:{bug['line']}"
                parent_id = f"class:{filepath}:{data['classes'][0]['name']}" if data["classes"] else f"file:{filepath}:{os.path.basename(filepath)}"
                
                node = {
                    "id": bug_id,
                    "name": f"{bug['category']}: L{bug['line']}",
                    "type": "blackhole",
                    "filepath": filepath,
                    "category": bug["category"],
                    "severity": bug["severity"],
                    "message": bug["message"],
                    "line": bug["line"],
                    "owaspRef": bug["owaspRef"],
                    "snippet": bug["snippet"],
                    "parentStar": parent_id
                }
                nodes.append(node)
                # Link blackhole to parent star
                edges.append({
                    "source": parent_id,
                    "target": bug_id,
                    "type": "gravitational_pull"
                })

        # Second Pass: Resolve dependencies (Orbit Paths)
        for filepath, data in files_data.items():
            parent_id = f"class:{filepath}:{data['classes'][0]['name']}" if data["classes"] else f"file:{filepath}:{os.path.basename(filepath)}"
            for dep in data["dependencies"]:
                # Look for matching target star in code
                if dep in node_map:
                    summary["orbits"] += 1
                    edges.append({
                        "source": parent_id,
                        "target": node_map[dep],
                        "type": "dependency",
                        "strength": 2 + (data["complexity"] % 4)
                    })

        if valid_files_count > 0:
            summary["avgCoverage"] = round(total_coverage / valid_files_count, 1)
            summary["avgComplexity"] = round(total_complexity / valid_files_count, 1)
        
        # Calculate dependency metrics
        summary["dependencyDepth"] = GalaxyGraphBuilder.calculate_dependency_depth(edges, nodes)
        summary["circularImports"] = GalaxyGraphBuilder.detect_circular_dependencies(edges)
        
        # Calculate codebase health score (same formula as frontend)
        # Base 100, minus penalties for complexity and bugs, plus coverage bonus
        bug_penalty = summary["blackholes"] * 12
        complexity_penalty = summary["avgComplexity"] * 1.5
        coverage_bonus = (summary["avgCoverage"] - 50) * 0.1
        summary["codebaseHealth"] = max(0, min(100, round(100 - bug_penalty - complexity_penalty + coverage_bonus)))
            
        return {
            "summary": summary,
            "nodes": nodes,
            "edges": edges
        }
