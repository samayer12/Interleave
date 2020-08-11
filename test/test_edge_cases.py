import unittest
from src import interleave


class PDFEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('text/edge_line_start_numbers.txt', 'r') as file:
            cls.edge_numbers = file.read()

        with open('text/edge_missing_paragraphs.txt', 'r') as file:
            cls.edge_missing_paragraphs = file.read()

        with open('text/edge_first_paragraph.txt', 'r') as file:
            cls.edge_first_paragraph = file.read()

        with open('text/edge_final_paragraph.txt', 'r') as file:
            cls.edge_final_paragraph = file.read()

        with open('text/edge_final_paragraph.txt', 'r') as file:
            cls.edge_final_paragraph = file.read()

        with open('text/edge_bad_parse.txt', 'r') as file:
            cls.edge_bad_parse = file.read()

        with open('text/edge_complex_7.txt', 'r') as file:
            cls.edge_complex_7 = file.read()

        cls.table_title = 'Table 1: PMNs for which EPA untimely published notice of receipt in the Federal Register'

        
    def test_edge_case_line_starts_with_numeric_sentence_end(self):
        result = interleave.build_paragraphs(interleave.sanitize_text('\n\n' + self.edge_numbers))
        self.assertEqual(7, len(result))  # Expect seven paragraphs

    def test_edge_case_missing_paragraphs(self):
        result = interleave.build_paragraphs(interleave.sanitize_text('\n\n' + self.edge_missing_paragraphs))
        self.assertEqual(7, len(result))  # Expect seven paragraphs

    def test_edge_case_isolate_first_paragraph(self):
        result = interleave.build_paragraphs(interleave.sanitize_text(self.edge_first_paragraph))
        self.assertEqual(1, len(result))

    def test_edge_case_ignore_trailing_tables(self):
        result = interleave.sanitize_text(self.edge_final_paragraph)[0]
        self.assertNotIn(self.table_title, result)

    def test_edge_marks_bad_paragraph_parse(self):
        result = interleave.build_paragraphs(interleave.sanitize_text('\n\n' + self.edge_bad_parse))
        self.assertEqual(3, len(result))
        self.assertIn('2. PARSE ERROR', result)

    def test_edge_complex_7(self):
        result = interleave.build_paragraphs(interleave.sanitize_text('\n\n' + self.edge_complex_7))
        self.assertEqual(4, len(result))

if __name__ == '__main__':
    unittest.main()
