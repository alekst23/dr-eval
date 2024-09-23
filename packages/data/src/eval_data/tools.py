from sqlite3 import Connection
from typing import List
from logging import getLogger

from eval_data.models.question import QuestionModel, QuestionType
from eval_data.models.qaset import QASetModel, QASetType


logger = getLogger(__name__)

def save_question_answers(db: Connection, question_list: List[str], answer_list: List[str], qaset: QASetType):
    logger.info(f"Saving {len(question_list)} questions and {len(answer_list)} answers for QASet {qaset.name}")

    question_model = QuestionModel(db)
    existing_questions = [ q.question for q in question_model.get_questions_by_qaset_id(qaset.id) ]
    count_existing = 0
    count_new = 0
    for question, answer in zip(question_list, answer_list):
        if not question or question in existing_questions:
            count_existing += 1
            continue

        question = QuestionType(
            qaset_id=qaset.id,
            document_id=qaset.document_id,
            question=question,
            answer=answer,
        )
        question_id = question_model.add_question(question)
        count_new += 1

    return count_new, count_existing