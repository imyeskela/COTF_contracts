from main.forms import ContractTemplateCreateForm, ContractCreateForm, FillingQuestionnaireForm, ContractTemplateChangeForm


def get_contract_form():
    """Получаем форму для создания Контракта"""

    return ContractCreateForm


def get_contract_template_create_form():
    return ContractTemplateCreateForm


def get_filling_questionnaire_form():
    """Получаем форму для заполнение анкеты"""

    return FillingQuestionnaireForm


def get_contract_template_form():
    return ContractTemplateChangeForm
