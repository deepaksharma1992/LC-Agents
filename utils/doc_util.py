from typing import TypedDict

from pydantic import BaseModel


class DocumentTypeOutput(BaseModel):
    doc_type: str

class DocumentOutputResult(TypedDict):
    is_error_in_doc: bool
    doc_result: str

class DocumentCategories:
    SALES_CONTRACT = "Sales Contract"
    LETTER_OF_CREDIT = "Letter of Credit"
    BILL_OF_LADING = "Bill of Lading"
    COMMERCIAL_INVOICE = "Commercial Invoice"
    PACKING_LIST = "Packing List"
    CERTIFICATE_OF_ORIGIN = "Certificate of Origin"
    INSURANCE_CERTIFICATE = "Insurance Certificate"
    FUMIGATION_CERTIFICATE = "Fumigation Certificate"
    INSPECTION_CERTIFICATE = "Inspection Certificate"
    PHYTOSANITARY_CERTIFICATE = "Phytosanitary Certificate"
    SHIPPING_BILL = "Shipping Bill"
    UNCLASSIFIED = "Unclassified"

    @classmethod
    def get_categories(cls):
        return [
            cls.SALES_CONTRACT,
            cls.LETTER_OF_CREDIT,
            cls.BILL_OF_LADING,
            cls.COMMERCIAL_INVOICE,
            cls.PACKING_LIST,
            cls.CERTIFICATE_OF_ORIGIN,
            cls.INSURANCE_CERTIFICATE,
            cls.INSPECTION_CERTIFICATE,
            cls.FUMIGATION_CERTIFICATE,
            cls.PHYTOSANITARY_CERTIFICATE,
            cls.SHIPPING_BILL,
            cls.UNCLASSIFIED
        ]

