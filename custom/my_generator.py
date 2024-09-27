from typing import Dict, Any, List
import os
from datasets.arrow_dataset import Dataset

from custom.default_llama_index import LlamaIndex

from logging import getLogger
logger = getLogger(__name__)


def build_query_engine(nodes: List[Dataset]):
    """ Customize this function to return a query engine of your choice. The engine """
    return LlamaIndex(nodes)
