"""Author by SonTV9"""

from .IngestorInterface import IngestorInterface
from .QuoteMode import QuoteModel


class TxtIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str):
        quotes = []
        with open(path, 'r') as file:
            for line in file:
                parts = line.strip().split(' - ')
                quotes.append(QuoteModel(*parts))
        return quotes
