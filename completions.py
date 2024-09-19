
from typing import List
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Tuple, List, Dict, Any

import logging


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


def generate_testset(generator: TestsetGenerator, documents: List[Dict[str, Any]], test_size: int) -> TestsetGenerator:
    logging.info("Initializing test set generator")
    generator, embeddings = initialize_generator()
    return generator.generate_with_llamaindex_docs(documents, test_size=test_size, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25}).to_dataset()
