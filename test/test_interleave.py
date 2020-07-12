import unittest
from src import interleave
from unittest.mock import patch


class PDFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('text/short_text.txt', 'r') as file:
            cls.short_text = file.read()

        with open('text/multiline_text.txt', 'r') as file:
            cls.multiline_text = file.read()

        with open('text/multipage_text.txt', 'r') as file:
            cls.multipage_text = file.read()

        with open('text/1000_paragraphs.txt', 'r') as file:
            cls.thousand_paragraphs = file.read()

        with open('text/pagenumbers.txt', 'r') as file:
            cls.pagenumbers = file.read()

        with open('text/headers.txt', 'r') as file:
            cls.headers = file.read()

        with open('text/edge_line_start_numbers.txt', 'r') as file:
            cls.edge_numbers = file.read()

        with open('text/edge_missing_paragraphs.txt', 'r') as file:
            cls.edge_paragraphs = file.read()

        with open('text/edge_first_paragraph.txt', 'r') as file:
            cls.edge_first_paragraph = file.read()

        cls.split_simple_text = ['1. First Entry.', '2. Second Entry.', '3. Third Entry.']

        cls.split_multiline_text = ['1. First Entry. This is a really long entry. It spans multiple lines. Very long. '
                                    'So tall. Can you believe how many words are here?',
                                    '2. Second Entry. This is an even longer entry! This one spans three lines. '
                                    'Ha, and you thought the last guy was verbose. '
                                    'Wait until I tell you a story my great-great grandfather once told me. '
                                    'Four score and seven years ago...',
                                    '3. Third Entry.']

        cls.split_multipage_text = ['1. First Entry.',
                                    '2. Second Entry. This paragraphs spans multiple pages. Words enable the document '
                                    'to automatically handle a page-break. This paragraph splits to the next page and '
                                    'continues with a normal word.',
                                    '3. Third Entry. This paragraphs spans multiple pages. Words enable the document '
                                    'to automatically handle a page-break. This paragraph splits to the next page and '
                                    'continues with a number so it is 1234 words.']

        cls.processed_text = [('1. First Entry.', '1. First Entry.'),
                              ('2. Second Entry.', '2. Second Entry.'),
                              ('3. Third Entry.', '3. Third Entry.')]

    def test_opens_PDF(self):
        self.assertEqual(self.short_text, interleave.convert_pdf_to_txt('PDFs/Simple.pdf'))

    def test_opens_multiline_PDF(self):
        self.assertEqual(self.multiline_text, interleave.convert_pdf_to_txt('PDFs/Multiline.pdf'))

    def test_opens_multipage_PDF(self):
        self.assertEqual(self.multipage_text, interleave.convert_pdf_to_txt('PDFs/Multipage.pdf'))

    def test_counts_up_to_1000_paragraphs(self):
        self.assertEqual(1000, len(interleave.get_sentences(self.thousand_paragraphs)))

    def test_builds_paragraphs_correctly(self):
        self.assertEqual(self.split_simple_text, interleave.build_paragraph('\n\n' + self.short_text))

    def test_splits_short_sentences(self):
        self.assertEqual(self.split_simple_text,
                         interleave.get_sentences(self.short_text))

    def test_splits_multiline_sentences(self):
        self.assertEqual(self.split_multiline_text,
                         interleave.get_sentences(self.multiline_text))

    def test_splits_multipage_paragraphs(self):
        self.assertEqual(self.split_multipage_text,
                         interleave.get_sentences(self.multipage_text))

    def test_removes_page_numbers(self):
        self.assertNotRegex('\n'.join(interleave.get_sentences(self.pagenumbers)),
                            r'\n\d+ \n')

    def test_removes_page_headers(self):
        self.assertNotRegex('\n'.join(interleave.get_sentences(self.headers)),
                            r'(\fC.*\d\n)')

    def test_edge_case_line_starts_with_numeric_sentence_end(self):
        result = interleave.get_sentences(self.edge_numbers)
        self.assertEqual(7, len(result))  # Expect six paragraphs

    def test_edge_case_missing_paragraphs(self):
        result = interleave.get_sentences(self.edge_paragraphs)
        self.assertEqual(7, len(result)) # Expect seven paragraphs

    def test_edge_case_isolate_first_paragraph(self):
        result = interleave.get_sentences(self.edge_first_paragraph)
        self.assertEqual(1, len(result))

    def test_zip_sentences_to_tuple(self):
        list1 = self.short_text
        list2 = self.short_text

        self.assertEqual(self.processed_text,
                         interleave.zip_sentences(interleave.get_sentences(list1),
                                                  interleave.get_sentences(list2)))

    @patch('builtins.open')
    @patch('src.interleave.writer', autospec=True)
    def test_writes_csv(self, mock_writer, mock_open):
        interleave.create_csv(self.processed_text)
        self.assertEqual(1, mock_open.call_count)
        self.assertEqual(2, mock_writer.call_count)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
