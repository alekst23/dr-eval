# Testing Process
The following steps describe the process of performing a RAG evaluation test

1. Initialization of Datasources: Setting up datasources that describe collections of documents.
2. Document Handling: Adding documents to the datasources which will be used for generating questions.
3. QASet Creation: Establishing QA sets that contain questions and their correct answers linked to specific documents.
4. Question Generation: Questions are either loaded from a QASet source or generated from the Document. This is done once before the test runs.
5. Execution of Test Runs: Running the tests to generate responses.
6. Evaluation Setup: Configuring evaluation functions and test evaluations to assess the responses based on predefined metrics.
7. Response Generation: Utilizing the RAG system to generate responses to the questions during test runs.
8. Context Management: Associating responses with relevant document contexts.
9. Execute Evaluation: Running the configured evaluation functions to generate scores and feedback for the responses.