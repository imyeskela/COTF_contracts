import os
from pathlib import Path

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.generic import View
import io
from io import BytesIO

from docxtpl import DocxTemplate
from django.views.generic import CreateView

from cotf_contracts.settings import BASE_DIR, MEDIA_URL
from services.main_logic import get_contracts
from services.file_logic import get_path
from main.utils import ContractListMixin
from main.forms import TemplateUploadForm
from main.models import Contract


class ContractListView(ContractListMixin, View):
    """Отображение всех контрактов"""

    queryset = get_contracts()
    template_name = 'contracts_list.html'


class ContractCreateView(CreateView):

    model = Contract
    template_name = 'contract_creation.html'
    form_class = TemplateUploadForm


# def doc_test(request):
#     doc = DocxTemplate(os.path.join(BASE_DIR, 'upload\\upload\Продление_МСК_КМСпеременные_Z5PiVvo.docx'))
#     context = {'id': "1488"}
#     doc.render(context)
#     doc.save("generated1488.docx")
#
#     doc_io = io.BytesIO() # create a file-like object
#     doc.save(doc_io) # save data to file-like object
#     doc_io.seek(0) # go to the beginning of the file-like object
#
#     response = HttpResponse(doc_io.read())
#
#     # Content-Disposition header makes a file downloadable
#     response["Content-Disposition"] = "attachment; filename=generated_doc.docx"
#
#     # Set the appropriate Content-Type for docx file
#     response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#
#     return response