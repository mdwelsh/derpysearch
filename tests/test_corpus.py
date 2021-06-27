
import pytest
from unittest.mock import MagicMock, NonCallableMock


from .. import corpus

def test_corpus():
    mock_client = MagicMock()
    mock_client.get.return_value = None
    mock_client.put.return_value = None

    thecorpus = corpus.Corpus(mock_client, "airplane")
    thecorpus.load()

    result = thecorpus.gentext("airplane", 10)
    assert result.startswith("airplane")
    result = thecorpus.gentext("The", 10)
    assert result.startswith("The")


