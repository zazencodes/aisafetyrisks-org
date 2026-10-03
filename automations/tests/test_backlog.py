"""The research backlog loads only in chronological order."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from paper_video import backlog


def paper(title: str, published: str) -> str:
    return f"""- title: {title}
  authors: [A. Author]
  published: '{published}'
  link: https://example.org/{title}
  arxiv: null
  category: alignment
  relevance: Test entry.
  status: queued
"""


class BacklogOrderTests(unittest.TestCase):
    def load(self, *papers: str) -> list[backlog.Entry]:
        with TemporaryDirectory() as temp:
            path = Path(temp) / "papers.yaml"
            path.write_text("papers:\n" + "".join(papers))
            with patch.object(backlog, "BACKLOG", path):
                return backlog.load()

    def test_chronological_backlog_loads(self):
        entries = self.load(paper("older", "2016-06-21"), paper("newer", "2017-06-12"))
        self.assertEqual([e.title for e in entries], ["older", "newer"])

    def test_out_of_order_backlog_is_refused(self):
        with self.assertRaisesRegex(ValueError, "'older' .* follows 'newer'"):
            self.load(paper("newer", "2017-06-12"), paper("older", "2016-06-21"))

    def test_repository_backlog_is_chronological(self):
        backlog.load()


if __name__ == "__main__":
    unittest.main()
