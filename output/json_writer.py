import json

class JSONWriter:
    @staticmethod
    def write(data: dict, output_file: str = "nulltrace_report.json"):
        """Export results to a JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"[+] Successfully exported JSON report to {output_file}")
        except IOError as e:
            print(f"[-] Failed to write JSON report: {e}")
