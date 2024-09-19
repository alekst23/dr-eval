from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)
from ragas import evaluate
from datasets import Dataset
import math

def eval_ragas(test_function, questions: list[str], contexts: list[list[str]], answers: list[str], ground_truths: list[list[str]]):
    dataset = Dataset.from_dict({
        'question': questions,
        'contexts': contexts,
        'answer': answers,
        'ground_truth': ground_truths
    })
    result = evaluate(
        dataset,
        metrics=[
            test_function
        ],
    )

    print(f">>> eval_rags > result = {result}")
    res = next(iter(result.values()))
    if math.isnan(res):
        return 0.0
    else:
        return res

def eval_ragas_precision(questions: list[str], contexts: list[list[str]], answers: list[str], ground_truths: list[list[str]])->float:
    return eval_ragas(context_precision, questions, contexts, answers, ground_truths)

def eval_ragas_recall(questions: list[str], contexts: list[list[str]], answers: list[str], ground_truths: list[list[str]])->float:
    return eval_ragas(context_recall, questions, contexts, answers, ground_truths)

def eval_ragas_faithfulness(questions: list[str], contexts: list[list[str]], answers: list[str], ground_truths: list[list[str]])->float:
    return eval_ragas(faithfulness, questions, contexts, answers, ground_truths)

def eval_ragas_answer_relevancy(questions: list[str], contexts: list[list[str]], answers: list[str], ground_truths: list[list[str]])->float:
    return eval_ragas(answer_relevancy, questions, contexts, answers, ground_truths)

#Dataset[question: list[str], contexts: list[list[str]], answer: list[str], ground_truth: list[list[str]]]
