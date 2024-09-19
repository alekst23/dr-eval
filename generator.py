from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Tuple, List, Dict, Any
from datasets import Dataset

from logging import getLogger
logger = getLogger(__name__)

def initialize_generator() -> Tuple[TestsetGenerator, OpenAIEmbeddings]:
    generator_llm = ChatOpenAI(model="gpt-4o-mini")
    critic_llm = ChatOpenAI(model="gpt-4o")
    embeddings = OpenAIEmbeddings()
    generator = TestsetGenerator.from_langchain(
        generator_llm,
        critic_llm,
        embeddings
    )
    return generator, embeddings

def generate_testset(documents: List[Dict[str, Any]], test_size: int) -> Dataset:
    logger.info("Initializing test set generator")
    logger.info(f"Processing {len(documents)} documents")
    generator, embeddings = initialize_generator()
    return generator.generate_with_llamaindex_docs(documents, test_size=test_size, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25}).to_dataset()