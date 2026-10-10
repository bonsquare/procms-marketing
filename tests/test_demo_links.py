from html.parser import HTMLParser
from pathlib import Path
import unittest


PAGE = Path(__file__).resolve().parents[1] / "index.html"
LOGIN = "https://procurems-demo.up.railway.app/login"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.current = {"href": dict(attrs).get("href"), "text": ""}

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.links.append(self.current)
            self.current = None


class DemoLinksTest(unittest.TestCase):
    def test_demo_calls_to_action_open_login(self):
        parser = LinkParser()
        parser.feed(PAGE.read_text(encoding="utf-8"))
        labels = (
            "Explore the demo",
            "Explore the free demo",
            "Open the demo",
            "Open the free demo",
        )
        for label in labels:
            with self.subTest(label=label):
                matches = [link for link in parser.links if link["text"].strip().startswith(label)]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0]["href"], LOGIN)


if __name__ == "__main__":
    unittest.main()
