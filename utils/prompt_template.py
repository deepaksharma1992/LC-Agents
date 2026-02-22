from langchain.prompts import PromptTemplate

from utils.prompt_constant import PromptConstant

# Define the prompt template for document classification
doc_classification_template = PromptTemplate(
    input_variables=["input_text", "categories"],
    template=PromptConstant.DOC_CLASSIFICATION_PROMPT
)

lc_prompt_template = PromptTemplate(input_variables=["sales_contract", "packing_list"],
                                    template=PromptConstant.LC_PROMPT)

document_verify_template = PromptTemplate(input_variables=["input_doc_type", "lc_detail", "input_doc_detail"],
                                          template=PromptConstant.DOCUMENT_VERIFY_PROMPT)

shipping_bill_template = PromptTemplate(input_variables=["input_doc_type", "lc_detail", "input_doc_detail", "ftp_india"],
                                          template=PromptConstant.SHIPPING_BILL_PROMPT)


deciding_agent_template = PromptTemplate(input_variables=["document_inputs_dict"],
                                          template=PromptConstant.DECIDING_AGENT_PROMPT)
