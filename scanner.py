import ast
import os
import json

class ArcheologistScanner:
    def __init__(self):
        self.definitions = {} # {name: node}
        self.calls = set()
        self.file_map = {}    # {name: filepath}

    def scan_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    # Capture function definitions
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                       self.definitions[node.name] = node
                       self.file_map[node.name] = filepath

                    # Capture function calls (local and method chaining)
                    if isinstance(node, ast.Call):
                        # Standard calls: func()
                        if isinstance(node.func, ast.Name):
                            self.calls.add(node.func.id)
                        # Chained calls: obj.method()
                        elif isinstance(node.func, ast.Attribute):
                            self.calls.add(node.func.attr)
            except Exception as e:
                print(f"Skipping {filepath}: {e}")

    def calculate_confidence(self, name, node):
        """
        Assigns a confidence score (0-100) that the code is 'Dead'.
        Lower score = More likely its actually in use (protected)
        """
        score = 100

        # Rule 1: The Decorator Rule (Framework entry points)
        # Covers Flask, Django, FastAPI, Celery, etc.
        if node.decorator_list:
            return 0 # 0% chance its dead; decorators mean it's an entry point

        # Rule 2: Interface Inference (React-like or standard Dunders)
        # Component-style names (Capitalised) or Python internals
        if name.startswith("__") or name[0].isupper():
            score -= 60

        # Rule 3: Private Indicators
        # Leading underscores often mean its only for local use
        if name.startswith("_") and not name.startswith("__"):
            score += 10

        # Rule 4: Usage Check
        if name in self.calls:
            return 0 # Definitely in use

        return min(max(score, 0), 100)

    def run(self, directory):
        for root, _, filenames in os.walk(directory):
            if any(x in root for x in ["venv", ".git", "__pycache__", "tests"]):
                continue
            for filename in filenames:
                if filename.endswith(".py"):
                    self.scan_file(os.path.join(root, filename))

        report = []
        for name, node in self.definitions.items():
            dead_confidence = self.calculate_confidence(name, node)
            if dead_confidence > 0:
                report.append({
                    "function": name,
                    "file": self.file_map[name],
                    "dead_confidence": f"{dead_confidence}%"
                })

        # Sort by most likely to be 'dead'
        return sorted(report, key=lambda x: int(x["dead_confidence"].strip('%')), reverse=True)

    def save_report(self, report, filename="archeology_report.json"):
        with open(filename, "w", encoding="utf-8") as f:
            # Save to a JSON
            json.dump(report, f, indent=4)
        print(f"\n ✅Site Report saved to: {os.path.abspath(filename)}")

if __name__ == "__main__":
    scanner = ArcheologistScanner()
    results = scanner.run(".")

    print(f"🕵🏽SITE REPORT: {len(results)} potential artifacts found. \n")
    print(f"{'CONFIDENCE':<12} | {'FUNCTION':<25} | {'LOCATION'}")
    print("-" * 70)
    for r in results:
        print(f"{r['dead_confidence']:<12} | {r['function']:<25} | {r['file']}")
        
    # Save the report to a JSON file.
    scanner.save_report(results)

    