from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import os
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from babel.dates import format_date
from PIL import Image
from docx import Document
from docx.shared import Mm, Inches, Pt
import qrcode
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from docx2pdf import convert
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.mail import EmailMessage
import base64
import convertapi

from cotf_contracts.settings import BASE_DIR, EMAIL_HOST_USER
from services.num_to_text import num2text
from main.forms import FillingQuestionnaireForm


from main.models import ContractTemplate, Contract
from main.forms import ContractTemplateCreateForm, ContractCreateForm, FillingQuestionnaireForm


def get_template_contracts():
    """Получаем все Шаблоны Контракты"""

    return ContractTemplate.objects.all()


def get_form_contract_template():
    """Получаем форму для создания Контракта"""

    return ContractCreateForm


def get_contracts():
    """Получаем все Контракты"""

    return Contract.objects.all()


def get_filling_questionnaire_form():
    """Получаем форму для заполнение анкеты"""

    return FillingQuestionnaireForm


def get_contract(self):
    return get_object_or_404(Contract.objects.all(), number=self.kwargs['contract_number'])


def generator_num_contract():
    """Генератор номера договора"""

    try:
        contract = Contract.objects.last()
        contract_num = getattr(contract, 'number')
        return contract_num + 1
    except AttributeError:
        return 24546799


