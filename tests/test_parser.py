import unittest
from core.parser import CodeParser


class TestCodeParser(unittest.TestCase):
    def test_parse_python_file(self):
        content = """import os

class Foo:
    def bar(self, x):
        return x
"""
        metrics = CodeParser.parse_file("app/foo.py", content)

        self.assertEqual(metrics["language"], "Python")
        self.assertEqual(len(metrics["classes"]), 1)
        self.assertEqual(metrics["classes"][0]["name"], "Foo")
        self.assertEqual(len(metrics["functions"]), 1)
        self.assertIn("os", metrics["dependencies"])
        self.assertGreaterEqual(metrics["loc"], 4)
        self.assertGreaterEqual(metrics["coverage"], 20)

    def test_parse_csharp_file(self):
        content = """using System;

namespace App {
    public class Bar {
        public void Run() {
        }
    }
}
"""
        metrics = CodeParser.parse_file("App/Bar.cs", content)

        self.assertEqual(metrics["language"], "C#")
        self.assertEqual(len(metrics["classes"]), 1)
        self.assertEqual(metrics["classes"][0]["name"], "Bar")
        self.assertTrue(any(f["name"] == "Run" for f in metrics["functions"]))
        self.assertIn("System", metrics["dependencies"])
