class PromptConstant:
    LC_PROMPT = """ You are an expert in international trade documentation
             specializing in creating Letters of Credit (L/C).
             Based solely on the details provided in the following sales contract and Packing List ,
             draft a comprehensive and accurate Letter of Credit contract.
             Ensure strict adherence to the terms and conditions outlined in the sales contract
             and comply with the Uniform Customs and Practice for Documentary Credits (UCP 600).

             ---
             ### Sales Contract Details: {sales_contract}
             ---
             ---
             ### Packing List Details: {packing_list}
             ---
             ### Output Requirements: Your output should include the following sections
             in the Letter of Credit document:
             1. Header Information:
                 - LC Number - Issuing Bank Details
                 - Advising Bank Details
                 - Date of Issue
                 - LC Type (e.g., Irrevocable, Confirmed)
             2. Applicant and Beneficiary Information:
                 - Full legal name, address, and contact information of the buyer (applicant) and
                 seller (beneficiary).
             3. Currency and Amount:
                - Total LC amount in the specified currency, exactly as stated in the sales contract.
             4. Description of Goods: - Detailed description of the goods being traded,
             including specifications, quantities, and any other relevant information strictly
             as described in the sales contract.
             5. Incoterms and Delivery Details: -
             Specify the Incoterms (e.g., CIF, FOB) and delivery terms,
             including the port of loading, port of discharge,
             and final destination, exactly as outlined in the contract.
             6. Payment Terms: - Specify the payment method
             (e.g., sight payment, deferred payment, or acceptance) and conditions for payment
             as stated in the contract.

             7. Required Documents: - List all documents required for payment as specified in
             the contract, such as:
                 - Commercial Invoice
                 - Packing List
                 - Bill of Lading
                 - Insurance Certificate
                 - Certificate of Origin
                 - Inspection Certificate
                 - Ensure the number of copies and format match the sales contract requirements.
             8. Expiration Date and Place:
                - Clearly state the LC’s expiration date and the location where documents must be presented,
             strictly following the contract.
             9. Special Conditions: - Include any additional terms or conditions exactly as
             specified in the sales contract.
             10. Governing Rules: - State that the LC is subject to the Uniform Customs and
             Practice for Documentary Credits (UCP 600).
             11. Additional Instructions: - Include any additional information or instructions
             explicitly stated in the sales contract.

             --- ###
             Notes: - The L/C must strictly reflect the sales contract without deviation.
             - If any information is unclear or missing from the sales contract,  it as an issue
              instead of assuming or improvising. - Ensure clarity and accuracy to avoid disputes
              or delays during the transaction. Provide the Letter of Credit text in a professional format. 
              
              ### Tool Usage Instructions:
             After generating the complete Letter of Credit document:
             - Output the full Letter of Credit content as plain text in your response.
             - Then, call the `generate_pdf_tool` using the exact content you generated.
             - After the PDF is generated, call `send_email_tool` with the professional subject, and descriptive body, recipient, and the PDF path.
              """

    DOC_CLASSIFICATION_PROMPT = """
    You are a document classifier. Your task is to analyze the input text and classify it into one of the 
    following categories: 
    {categories} 
    Based on the content and context of the input text, respond with the category name that best fits the text. 
    Give the output as per the pydantic class attached. 
    Input text: "{input_text}"
    """

    DOCUMENT_VERIFY_PROMPT = """
             You are an expert in international trade documentation. You are provided with input 
             export document type: {input_doc_type} and Letter Of credit. You need to make sure that the export 
             document adheres with the Letter of Credit Terms. If not flag a error message in flag boolean variable,
             then provide concisely document pain points(success case)/issues(failure case) citing what is wrong 
             with the document. Based solely on the details provided in the following Letter of Credit, and export document.
             
             --- 
             ### Letter of Credit Details: {lc_detail} 
             --- 
             
             --- 
             ### Input Export Document Detail: {input_doc_detail} 
             --- 
    """
    SHIPPING_BILL_PROMPT = """
             You are an expert in international trade documentation. You are provided with input 
             export document type: {input_doc_type}, Foreign Trade Policy Chapter 10 text and Letter Of credit. 
             You will perform the following tasks:
             1. Extract the 8 digit HSN code from Shipping Bill text.
             2. Identify product of Shipping Bill HSN code. This information you can use your own learnt knowledge base.
             3. Check if the product description from Shipping Bill matches the result of HSN code search.
             4. Check if the product is valid to carry as per Foreign Trade Policy of India under Letter of Credit.
             5. Implication of the mis-classification of product if there as per Indian Customs.

             If there is issues in above steps, flag a error message in flag boolean variable,
             then provide brief document pain points, which should include the provided HSN code in 
             Shipping Bill vs the actual HSN code in Letter of Credit, customs possible actions.
             
             --- 
             ### Letter of Credit Details: {lc_detail} 
             --- 
             
             --- 
             ### Input Export Document Detail: {input_doc_detail} 
             --- 
             --- 
             ### Foreign Trade Policy Chapter 10: {ftp_india} 
             --- 
    """

    DECIDING_AGENT_PROMPT = """
        You are an expert in international trade documentation. Your task is to verify input coming from export documents
        LLMs the specified requirements. Input will be python dict containing the document type as key and the document 
        success, error and remedies as value for each key-value pair. Your job is to aggregate the results of all key-value
        pairs. The output of this will be sent as email in html formatted text to the user don't include new line text, please provide only the formatted text. 
        ---
        ### Export Documents by Category Dict:
        {document_inputs_dict}
        ---

        Instructions:
        1. If a document is non-compliant, highlight the specific issues with the document.
        3. If all documents are compliant, aggregate the results and send a success message.
        4. If there are issues, provide a detailed report listing the errors for each document category.

        Output Requirements:
        - If all documents are compliant: "Success: All documents are compliant with the expected requirements."
        - If there are issues: Provide a detailed error report for each non-compliant document category.
        """
