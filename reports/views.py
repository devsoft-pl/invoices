from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
from invoices.models import Invoice


@login_required
def list_reports_view(request):
    net_invoices = list(Invoice.objects.filter(invoice_type=Invoice.INVOICE_SALES).annotate(month=ExtractMonth('sale_date')).values('month').annotate(sum_net=Sum('net_amount')))

    net_sum_per_month = dict([str(invoice['month']), invoice['sum_net']] for invoice in net_invoices)
    net_invoices = [{"month": month, "sum_net": net_sum_per_month.get(str(month), 0)} for month in range(1, 13)]

    gross_invoices = list(Invoice.objects.filter(invoice_type=Invoice.INVOICE_SALES).annotate(month=ExtractMonth('sale_date')).values('month').annotate(gross_sum=Sum('gross_amount')))

    gross_sum_per_month = dict([str(invoice['month']), invoice['gross_sum']] for invoice in gross_invoices)
    gross_invoices = [{"month": month, "gross_sum": gross_sum_per_month.get(str(month), 0)} for month in range(1, 13)]

    context = {"net_invoices": net_invoices, "gross_invoices": gross_invoices, "current_module": "reports"}

    return render(request, "reports/list_reports.html", context)


    #
    # # filter_form = ReportFilterForm(request.GET)
    # # if filter_form.is_valid():
    # #     invoices = filter_form.get_filtered_reports(invoices)
    #
    # # context = {"invoices": invoices, "filter_form": filter_form, "current_module": "reports"}
