import os
import yaml
import argparse
from collectors.chrome_reader import ChromePolicyReader
from collectors.edge_reader import EdgePolicyReader
from comparison.comparator import compare_cis_to_browser
from exporters.csv_exporter import export_to_csv

def load_cis_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Browser Policy Scan: Checks Chrome/Edge policy settings against CIS Benchmarks.")
    parser.add_argument(
        "--file",
        required=True,
        help="Path to HTML file exported from browser",
    )
    parser.add_argument(
        "--cis",
        required=True,
        help="Path to CIS yaml file",
    )
    parser.add_argument(
        "--browser",
        required=False,
        type=str.lower,
        choices=["edge", "chrome"],
        default="Edge",
        help="Which browser's policy reader to use. Default: Edge",
    )
    parser.add_argument(
        "--output",
        default="comparison_results.csv",
        help="Where to save the CSV comparison output. Default: comparison_results.csv"
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise ValueError(f"[ERROR] File not found: {args.file}")

    browser = args.browser.strip()

    if browser == "edge":
        reader = EdgePolicyReader(args.file)
    elif browser == "chrome":
        reader = ChromePolicyReader(args.file)
    else:
        raise ValueError(f"Unsupported browser: {args.browser}")

    try:
        browser_policies = reader.read()
        cis_policies = load_cis_yaml(args.cis)
        results = compare_cis_to_browser(cis_policies, browser_policies)
    except Exception as e:
        print(f"[ERROR] Failed to parse HTML: {e}")
        return

    print(f"Analyzed {len(browser_policies)} policy entries")

    export_to_csv(results, args.output)

if __name__ == "__main__":
    main()
