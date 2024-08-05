"""Author by SonTV9"""

import docx

from .IngestorInterface import IngestorInterface
from .QuoteMode import QuoteModel


class DocxIngestor(IngestorInterface):

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str):
        quotes = []
        doc = docx.Document(path)
        for paragraph in doc.paragraphs:
            quotes.append(QuoteModel(*paragraph.text.split(' - ')))
        return quotes

