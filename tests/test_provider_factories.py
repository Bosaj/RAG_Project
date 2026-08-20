import unittest

from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory


class VectorDBProviderFactoryTests(unittest.TestCase):
    def test_unknown_provider_raises_actionable_error(self):
        factory = VectorDBProviderFactory.__new__(VectorDBProviderFactory)

        with self.assertRaisesRegex(
            ValueError,
            "Unsupported vector database provider: 'unknown'",
        ):
            factory.create("unknown")


if __name__ == "__main__":
    unittest.main()
