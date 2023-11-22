from semantic_kernel.skill_definition import sk_function
from plugins.form_recognizer.form_recognizer_connector import FormRecognizerConnector
import logging

class FormRecognizer:
    """
    A plugin to read an Invoice.
    """

    def __init__(self, endpoint: str, api_key: str):
        if not endpoint:
            raise Exception("FormRecognizer endpoint is not set")
        if not api_key:
            raise Exception("FormRecognizer API key is not set")

        # Create a logger
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.INFO)

        # Create a file handler
        handler = logging.FileHandler('my_log.log')
        handler.setLevel(logging.INFO)

        # Add the handler to the logger
        logger.addHandler(handler)

        # Create an instance of the FormRecognizerConnector
        self.form_recognizer = FormRecognizerConnector(endpoint=endpoint, api_key=api_key, logger=logger)

    @sk_function(
        description="Use Form Recognizer to process an invoice. The result is a dictionary of the detected fields.",
        name="process_invoice",
        input_description="The path to the invoice file.",
    )
    def process_invoice(self, filename_path: str) -> str:
        """
        A native function that uses Form Recognizer to process an invoice.
        """

        # Input validation, the error message can help self-correct the input
        if not filename_path:
            raise ValueError("The filename_path argument cannot be null.")

        #result = self.form_recognizer.recognize_invoice_async(filename_path=filename_path)
        result = self.form_recognizer.read_invoice(filename_path=filename_path)

        return result