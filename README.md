# 🔍 bpscan

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)

A lightweight CLI tool to scan Chrome/Edge policy settings against CIS Benchmarks.

## ⚙️ Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/baurzhaan/bpscan
   cd bpscan
```

2. **Install requirements:**
```bash
   pip install -r requirements.txt
```

## 🚀 How to run

1. **Export browser's current policy settings** 
   * Open Chrome or Edge and go to ***chrome://policy/*** or ***edge://policy/***.
   * Tick the ***Show policies with no value set*** checkbox.
   * Save the page as a ***Webpage, Complete*** HTML file using Ctrl + S. By default, this will be saved as ***Policies.html***

2. **Run the tool**
   * Microsoft Edge version
```bash
python bpscan.py --file Policies.html --browser edge --cis data/cis-edge-v4.0.0-27.10.25.yaml --output edge.csv
```
   * Google Chrome version
```bash
python bpscan.py --file Policies.html --browser chrome --cis data/cis-chrome-v3.0.0-29.01.24.yaml --output chrome.csv
```

#### Arguments

```text
  -h, --help            show this help message and exit
  --file FILE           Path to HTML file exported from browser
  --cis CIS             Path to CIS yaml file
  --browser {edge,chrome}
                        Which browser's policy reader to use. Default: Edge
  --output OUTPUT       Where to save the CSV comparison output. Default: comparison_results.csv
```

### 📊 Example CSV Report (`output.csv`)

```markdown
| policy_id | policy_name | level | browser_value | effective_value | cis_recommended_value | compliant | value_source | rationale | impact
| EnableMediaRouter | Enable Google Cast | L1 | false | false | ['false'] | True | explicit | rationale | impact |
| CACertificateManagementAllowed | Allow users to manage installed CA certificates. | L1 |  | 1 | ['2'] | False | default | rationale | impact
| GuidedSwitchEnabled | Guided Switch Enabled | L1 |  | true | ['false'] | False | default | rationale | impact
```

## 🔍 How to interpret the result

The tool generates an ***output.csv*** file (or a filename of your choice). The ***Compliant*** column indicates whether each specific policy setting aligns with the CIS recommended values.

## 🔒 Privacy & Security

This tool is designed with a **privacy-first** approach:

* **Local Processing:** All data processing happens on your local machine.
* **No Data Collection:** Policy data never leaves your local machine.
* **Open Source:** You are encouraged to review the `bpscan.py` source code to verify that no network requests are being made.

## 📣 Feedback & Contributions

Feedback is highly appreciated! Whether it is a bug report, a new policy suggestion, or a general complaint, please reach out via one of the following:

* **GitHub Issues:** [Open an issue](https://github.com/baurzhaan/browser-policies-auditor/issues) to report bugs or request new features.
* **Inconsistencies:** If you notice the auditor flags a policy incorrectly compared to the official CIS Benchmark, please provide the Policy Name and the expected vs. actual result.
* **Email:** You can also reach me directly at `zhanabaur@gmail.com` for feedback or questions.

> **Note:** When reporting an error, please include your browser version and the operating system you are using.

---

## 📚 Credits & References

* **CIS Benchmarks** - [Center for Internet Security](https://www.cisecurity.org/).
* **Google Chrome Policies** - [Chrome Enterprise policy list](https://chromeenterprise.google/policies/).
* **Microsoft Edge Policies** - [Microsoft Edge - Policies](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies).
* **BeautifulSoup4** - Used for parsing policy exports.
* **PyYAML** - Used for processing benchmark configurations.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

> [!CAUTION]
> This tool is an independent project and is **not** an official CIS® product. It is intended to assist with auditing and should be used as part of a broader security strategy. The author is not responsible for any misconfigurations or system issues resulting from the use of this software. Always test policies in a lab environment before deploying to production.
