import unittest
from stores.llm.templates.template_parser import TemplateParser


class TemplateParserTests(unittest.TestCase):
    def test_english_template_resolution(self):
        parser = TemplateParser(language='en')
        prompt = parser.get(group='rag', key='system_prompt')
        self.assertIsNotNone(prompt)
        self.assertIn('assistant', prompt.lower())

    def test_arabic_template_resolution(self):
        parser = TemplateParser(language='ar')
        prompt = parser.get(group='rag', key='system_prompt')
        self.assertIsNotNone(prompt)

    def test_french_template_resolution(self):
        parser = TemplateParser(language='fr')
        prompt = parser.get(group='rag', key='system_prompt')
        self.assertIsNotNone(prompt)
        self.assertIn('assistant expert', prompt.lower())

    def test_fallback_to_default_language_when_unknown(self):
        parser = TemplateParser(language='de', default_language='en')
        prompt = parser.get(group='rag', key='system_prompt')
        self.assertIsNotNone(prompt)
        self.assertIn('assistant', prompt.lower())


if __name__ == '__main__':
    unittest.main()