"""
context_processor.py

This module is used to register context processor`
"""

from employee.models import Employee
from payroll.models import tax_models as models
from payroll.models.models import Deduction


def default_currency(request):
    payroll_settings = models.PayrollSettings.objects.first()

    if payroll_settings is None:
        selected_company = request.session.get("selected_company")

        if selected_company and selected_company != "all":
            company_id = selected_company
        else:
            company_id = None

        payroll_settings = models.PayrollSettings.objects.create(
            currency_symbol="$",
            company_id=company_id,
        )

    return {
        "currency": request.session.get(
            "currency",
            payroll_settings.currency_symbol,
        ),
        "position": request.session.get(
            "position",
            payroll_settings.position,
        ),
    }

def host(request):
    """
    This method will return the host
    """
    protocol = "https" if request.is_secure() else "http"
    return {"host": request.get_host(), "protocol": protocol}


def get_deductions(request):
    """
    This method used to return the deduction
    """
    deductions = Deduction.objects.filter(
        only_show_under_employee=False, employer_rate__gt=0
    )
    return {"get_deductions": deductions}


def get_active_employees(request):
    """
    This method used to return the deduction
    """
    employees = Employee.objects.filter(
        is_active=True, contract_set__isnull=False, payslip__isnull=False
    ).distinct()
    return {"get_active_employees": employees}
