import sys
from dotenv import load_dotenv
load_dotenv()

PATH_IN = f"tests/data/output/completions/{sys.argv[1] if len(sys.argv)>1 else 'file'}"

# data
from datasets import Dataset, load_dataset

dataset = Dataset.load_from_disk(PATH_IN)


# metrics

from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)

# evaluation
from ragas import evaluate

result = evaluate(
    dataset,
    metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall,
    ],
)

df = result.to_pandas()
print(df.head())
#df.to_csv("tests/data/output/results.csv")
df.to_pickle("src/eval-serv/results.pkl")