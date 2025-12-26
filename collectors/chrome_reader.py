from bs4 import BeautifulSoup

class ChromePolicyReader:
    """
    MVP class for extracting Chrome policy information
    from an HTML file exported via chrome://policy.

    Usage:
        reader = ChromePolicyReader("path/to/chrome_policies.html")
        data = reader.read()
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> list[dict]:
        """Public method to parse Chrome policy HTML and return structured data."""
        html = self._load_html()
        return self._parse_html(html)

    # ---------------------------- Internal Helpers ---------------------------- #

    def _load_html(self) -> str:
        """Load raw HTML from a user-saved chrome://policy file."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_html(self, html: str) -> list[dict]:
        """Parse the Chrome policy HTML table into structured dictionaries."""
        soup = BeautifulSoup(html, "html.parser")

        policy_table = soup.find("policy-table")
        if not policy_table:
            raise ValueError("Could not! find policy table in HTML.")

        rows = policy_table.find_all("policy-row", role="rowgroup", class_="policy-data")
        if len(rows) < 2:
            raise ValueError("Policy table appears to be empty.")
        
        headers = [ "Policy name", "Policy value", "Source", "Applies to", "Level", "Status" ]

        results = []
        
        for row in rows:
            el = row.select_one(".name span")
            name = el.contents[0].strip() if el and el.contents else ""
            
            el = row.select_one(".value")
            value = el.contents[0].strip() if el and el.contents else ""
            
            el = row.select_one(".source")
            source = el.contents[0].strip() if el and el.contents else ""
            
            el = row.select_one(".scope")
            applies_to = el.contents[0].strip() if el and el.contents else ""
            
            el = row.select_one(".level")
            level = el.contents[0].strip() if el and el.contents else ""
            
            el = row.select_one(".messages")
            status = el.contents[0].strip() if el and el.contents else ""
            
            cols = [ name, value, source, applies_to, level, status ]
            
            entry = dict(zip(headers, cols))
            results.append(entry)
        
        return results
