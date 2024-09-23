from datasets import load_dataset
from logging import getLogger

from eval_data.models.qaset import QASetModel, QASetType


logger = getLogger(__name__)

def load_qa_dataset(qaset: QASetType):
    location = qaset.location.split(";")
    path = location[0]
    name = location[1] if len(location) > 1 else None

    logger.info(f"Loading HuggingFace dataset from {location}")

    dataset_dict = load_dataset(path, name)
    dataset = dataset_dict[list(dataset_dict.keys())[0]]

    test_questions = dataset[qaset.col_question]
    test_answers = dataset[qaset.col_answer]

    return test_questions, test_answers