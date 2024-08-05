"""Author by SonTV9"""

import pandas as pd

from .IngestorInterface import IngestorInterface
from .QuoteMode import QuoteModel


class CsvIngestor(IngestorInterface):
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str):
        csv = pd.read_csv(path)
        quotes = []
        for index, row in csv.iterrows():
            quotes.append(QuoteModel(**row))
        return quotes
