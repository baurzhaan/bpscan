import csv
from typing import List, Dict

def export_to_csv(results: List[Dict], output_path: str) -> None:
    if not results:
        print("[WARN] No results to export.")
        return

    headers = list(results[0].keys())

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)

    print(f"[OK] Exported comparison results to {output_path}")
