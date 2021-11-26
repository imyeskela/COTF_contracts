import base64
import os
import zipfile
from io import BytesIO
from django.http import HttpResponse

from cotf_contracts import settings
from main.models import ContractTemplate, Contract, AuthenticationCode


def get_contract_and_payment(contract_number):
    contract = Contract.objects.get(number=contract_number)
    signed_contract = contract.signed_contract.path
    payment = contract.payment.path

    contract_and_payment = [signed_contract, payment]
    return contract_and_payment


def download(self, contract_number):
    files = get_contract_and_payment(contract_number)
    print(files)
    zip_subdir = str(contract_number)
    zip_filename = f'{zip_subdir}.zip'

    b = BytesIO()
    zip_file = zipfile.ZipFile(b, 'w')
    for file_path in files:
        file_dir, file_name = os.path.split(file_path)
        zip_path = os.path.join(zip_subdir, file_name)
        zip_file.write(file_path)

    zip_file.close()
    b.seek(0)

    response = HttpResponse(b.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment;filename=' + zip_filename

    return response




