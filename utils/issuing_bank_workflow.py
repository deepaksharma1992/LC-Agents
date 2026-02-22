from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langgraph.graph.message import add_messages

from custom_llm import get_llm_agent
from utils.doc_util import DocumentCategories, DocumentTypeOutput
from utils.pdf_utils import get_files_in_directory, extract_pdf_content
from utils.prompt_template import doc_classification_template, lc_prompt_template

load_dotenv()

document_agent_llm = get_llm_agent()
lc_llm = get_llm_agent()


doc_extract_dict = {}
files = get_files_in_directory("../import_docs")
for file in files:
    prompt = doc_classification_template
    file_text = extract_pdf_content(file)
    user_input = prompt.format(categories=DocumentCategories.get_categories(), input_text=file_text)
    structured_llm = document_agent_llm.with_structured_output(DocumentTypeOutput)
    response = structured_llm.invoke(user_input)
    print(response)
    doc_type = response.doc_type
    doc_extract_dict[doc_type] = file_text

print(doc_extract_dict)
prompt = lc_prompt_template
document_input = prompt.format(sales_contract=doc_extract_dict.get(DocumentCategories.SALES_CONTRACT),
                               packing_list=doc_extract_dict.get(DocumentCategories.PACKING_LIST))
response = lc_llm.invoke(document_input)
print(response)

print("\nWorkflow finished.")
