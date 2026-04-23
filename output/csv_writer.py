import csv

class CSVWriter:
    @staticmethod
    def write(data: dict, output_file: str = "nulltrace_report.csv"):
        """Export results to a CSV file."""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # We flatten the results slightly depending on the query
                query = data.get("query", "unknown")
                results = data.get("results", {})
                
                # Basic key-value flatten for the root of results
                writer.writerow(["Query", "Source", "Key", "Value"])
                
                for source, source_data in results.items():
                    if isinstance(source_data, dict):
                        for k, v in source_data.items():
                            writer.writerow([query, source, k, v])
                    else:
                         writer.writerow([query, source, "data", source_data])
                         
            print(f"[+] Successfully exported CSV report to {output_file}")
        except IOError as e:
            print(f"[-] Failed to write CSV report: {e}")
