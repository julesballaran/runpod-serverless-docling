import os
import base64
import runpod

from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline


def doc_converter(path):
    converter = (
        DocumentConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.IMAGE,
                InputFormat.DOCX,
                InputFormat.HTML,
                InputFormat.PPTX,
                InputFormat.ASCIIDOC,
                InputFormat.CSV,
                InputFormat.MD,
            ],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend
                ),
                InputFormat.DOCX: WordFormatOption(
                    pipeline_cls=SimplePipeline
                ),
            },
        )
    )
    result = converter.convert(path)
    return result.document.export_to_markdown()

def handler(job):
    job_input = job["input"]

    file_url = job_input.get('file_url')
    file_base64 = job_input.get('file_base64')

    if not file_url and not file_base64:
        return {"error": "missing file_url"}
    
    if file_base64:
        file_data = base64.b64decode(file_base64)
        with open("output", "wb") as file:
            file.write(file_data)
        output = doc_converter("output")
        if os.path.exists("output"):
            os.remove("output")
            print("File deleted successfully!")
        else:
            print("File not found.")
        
        return output

    if file_url:
        return doc_converter(file_url)

    return ""


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})