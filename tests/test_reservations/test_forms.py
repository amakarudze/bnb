from reservations.forms import SearchReportsForm


def test_search_reports_form(search_report_form):
    form = SearchReportsForm(search_report_form)
    assert form.is_valid()
    assert form.errors == {}
