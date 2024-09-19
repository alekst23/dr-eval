from llama_index.core.schema import Document
from packages.data.src.eval_data.models.document import DocumentModel, DocumentType
from packages.data.src.eval_data.models.qaset import QASetModel, QASetType
from packages.data.src.eval_data.models.testrun import TestRunModel, TestRunType

def sog_testrun(db_connection, test_run: TestRunType) -> TestRunType:
    testrun_model = TestRunModel(db_connection)
    if test_run := testrun_model.get_test_run_by_name(test_run.description):
        return test_run
    else:
        test_run.id = testrun_model.add_test_run(test_run)
        return test_run

def sog_document(db_connection, document: Document, datasource_id: int) -> DocumentType:
    document_model = DocumentModel(db_connection)
    document_name = document.extra_info['file_name']
    doc = document_model.get_document_by_name(document_name)
    if doc:
        return doc
    else:
        new_document = DocumentType(
            datasource_id=datasource_id,
            name=document_name,
            location=document.extra_info['file_path'],
            source="file"
        )
        new_document.id = document_model.add_document(new_document)

        return new_document
    

def sog_qaset(db_connection, document: Document, datasource_id: int, document_id: int):
    qaset_model = QASetModel(db_connection)
    if qaset := qaset_model.get_qaset_by_name(document.extra_info['file_name']):
        return qaset
    else:
        qaset = QASetType(
            datasource_id=datasource_id,
            document_id=document_id,
            name=document.extra_info['file_name'],
            location=document.extra_info['file_path']
        )
        qaset.id = QASetModel(db_connection).add_qaset(qaset)
        return qaset

