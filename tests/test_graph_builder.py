import unittest
from core.graph_builder import GalaxyGraphBuilder


class TestGalaxyGraphBuilder(unittest.TestCase):
    def test_build_graph_metrics(self):
        files_data = {
            "app/foo.py": {
                "classes": [{"name": "Foo", "line": 1, "inherits": []}],
                "functions": [{"name": "bar", "line": 4, "paramCount": 1, "isPublic": True}],
                "dependencies": ["Bar"],
                "bugs": [],
                "loc": 15,
                "coverage": 80,
                "complexity": 3,
                "language": "Python"
            },
            "app/bar.py": {
                "classes": [{"name": "Bar", "line": 1, "inherits": []}],
                "functions": [{"name": "baz", "line": 3, "paramCount": 0, "isPublic": True}],
                "dependencies": ["Foo"],
                "bugs": [],
                "loc": 20,
                "coverage": 70,
                "complexity": 4,
                "language": "Python"
            }
        }

        graph = GalaxyGraphBuilder.build_graph(files_data)

        self.assertEqual(graph["summary"]["stars"], 2)
        self.assertEqual(graph["summary"]["planets"], 2)
        self.assertGreaterEqual(graph["summary"]["orbits"], 2)
        self.assertGreaterEqual(graph["summary"]["dependencyDepth"], 1)
        self.assertGreaterEqual(graph["summary"]["circularImports"], 1)
        self.assertIn("codebaseHealth", graph["summary"])
