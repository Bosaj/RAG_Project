import tempfile
import unittest
from pathlib import Path

from controllers.ProjectController import ProjectController


class ProjectPathTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.controller = ProjectController.__new__(ProjectController)
        self.controller.files_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_project_id_creates_directory_under_storage_root(self):
        project_path = Path(self.controller.get_project_path("project-1"))

        self.assertEqual(project_path.parent, Path(self.temp_dir.name).resolve())
        self.assertTrue(project_path.is_dir())

    def test_traversal_project_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.controller.get_project_path("../../outside")

    def test_empty_project_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.controller.get_project_path("   ")


if __name__ == "__main__":
    unittest.main()
