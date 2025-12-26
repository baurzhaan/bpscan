from bs4 import BeautifulSoup

class EdgePolicyReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> list[dict]:
        """Public method to parse Edge policy HTML and return structured data."""
        html = self._load_html()
        return self._parse_html(html)

    # ---------------------------- Internal Helpers ---------------------------- #
    def _load_html(self) -> str:
        """Load raw HTML from a user-saved edge://policy file."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_html(self, html: str) -> list[dict]:
        """Parse the Edge policy HTML table into structured dictionaries."""
        soup = BeautifulSoup(html, "html.parser")
        
        policy_table = soup.find(id="chrome-table")
        if not policy_table:
            raise ValueError("Could not! find policy table in HTML.")

        rows = policy_table.find_all("div", role="row", class_="c01111 c01134 entry")
        if len(rows) < 2:
            raise ValueError("Policy table appears to be empty.")
        
        headers = [ "Policy name", "Policy value", "Source", "Applies to", "Level", "Status" ]

        results = []
        
        for row in rows:
            el = row.select_one("span", role="rowheader")
            name = el.get_text().strip() if el else ""
            
            el = row.find_all("span", role="cell", class_="c01137")
            if len(el) < 2:
                raise ValueError("Something wrong with Policy Value or Status.")
            value = el[0].get_text().strip()
            status = el[1].get_text().strip()

            el = row.find_all("span", role="cell", class_="c01133")
            if len(el) < 3:
                raise ValueError("Something wrong with Source, Applies To or Level.")
            source = el[0].get_text().strip()
            applies_to = el[1].get_text().strip()
            level = el[2].get_text().strip()
            
            cols = [ name, value, source, applies_to, level, status ]
            
            entry = dict(zip(headers, cols))
            results.append(entry)

        return results
