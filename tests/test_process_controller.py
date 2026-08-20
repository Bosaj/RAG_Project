import tempfile
import unittest
from pathlib import Path

from controllers.ProcessController import ProcessController


class ProcessFilePathTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.controller = ProcessController.__new__(ProcessController)
        self.controller.project_path = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_resolves_file_inside_project_directory(self):
        file_path = Path(self.temp_dir.name) / "document.txt"
        file_path.write_text("hello", encoding="utf-8")

        self.assertEqual(
            Path(self.controller.get_file_path("document.txt")),
            file_path.resolve(),
        )

    def test_rejects_traversal_file_id(self):
        self.assertIsNone(self.controller.get_file_path("../../outside.txt"))
        self.assertIsNone(self.controller.get_file_loader("../../outside.txt"))

    def test_missing_file_returns_no_loader(self):
        self.assertIsNone(self.controller.get_file_loader("missing.txt"))

    def test_extension_normalization_is_case_insensitive(self):
        self.assertEqual(self.controller.get_file_extension("document.TXT"), ".txt")
        self.assertEqual(self.controller.get_file_extension("document.PdF"), ".pdf")


if __name__ == "__main__":
    unittest.main()
