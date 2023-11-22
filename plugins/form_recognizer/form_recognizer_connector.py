from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient, AnalyzeResult
from typing import Optional
from logging import Logger
from semantic_kernel.utils.null_logger import NullLogger
import json

class FormRecognizerConnector():

    _api_key: str

    def __init__(self, endpoint: str, api_key: str, logger: Optional[Logger] = None) -> None:
        self._api_key = api_key
        self._endpoint = endpoint
        self._logger = logger if logger else NullLogger()

        if not self._endpoint:
            raise ValueError("FormRecognizer endpoint cannot be null.")

        if not self._api_key:
            raise ValueError("FormRecognizer API key cannot be null.")

    def recognize_invoice_async(self, filename_path: str) -> str:

        # Create an instance of a Form Recognizer client
        document_analysis_client = DocumentAnalysisClient(
            endpoint=self._endpoint, credential=AzureKeyCredential(self._api_key)
        )

        poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", open(filename_path, "rb"))

        invoices = poller.result()

        invoice = invoices.documents[0]
        invoice_total = invoice.fields.get("InvoiceTotal")
        customer_name = invoice.fields.get("CustomerName")
        invoice_id = invoice.fields.get("InvoiceId")
        invoice_date = invoice.fields.get("InvoiceDate")
        invoice_total_value = str(invoice_total.value) if invoice_total and invoice_total.value else None
        customer_name_value = str(customer_name.value) if customer_name and customer_name.value else None
        invoice_id_value = str(invoice_id.value) if invoice_id and invoice_id.value else None
        invoice_date_value = str(invoice_date.value) if invoice_date and invoice_date.value else None

        self._logger.info("Invoice Total: {}".format(invoice_total_value))
        self._logger.info("Customer Name: {}".format(customer_name_value))
        self._logger.info("Invoice ID: {}".format(invoice_id_value))
        self._logger.info("Invoice Date: {}".format(invoice_date_value))

        # Create a string with the results, separated by ";"
        result = ";".join([invoice_total_value, customer_name_value, invoice_id_value, invoice_date_value])

        return result


    def read_invoice(self, filename_path: str) -> str:
        # Create an instance of a Form Recognizer client
        document_analysis_client = DocumentAnalysisClient(
            endpoint=self._endpoint, credential=AzureKeyCredential(self._api_key)
        )

        poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", open(filename_path, "rb"))

        invoices = poller.result()

        invoice = invoices.documents[0]

        # Create a dictionary to store all field values
        field_values = {}

        # Iterate over all fields in the invoice
        for field_name, field in invoice.fields.items():
            # Convert the field value to a string if it exists, else store None
            field_values[field_name] = str(field.value) if field and field.value else None

            # Log the field value
            self._logger.debug("{}: {}".format(field_name, field_values[field_name]))

        # Convert the dictionary to a JSON string
        result = json.dumps(field_values, ensure_ascii=False)

        return result