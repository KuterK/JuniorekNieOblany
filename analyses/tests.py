from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import AnalysisCreateForm
from .models import Analysis
from .schemas import CodeAnalysisV1
from .tasks import generate_analysis

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return get_user_model().objects.create_user(username="junior", password="strong-pass-123")


def test_code_is_limited_to_100_lines():
    form = AnalysisCreateForm(data={"code": "\n".join("x" for _ in range(101))})
    assert not form.is_valid()
    assert "maksymalnie 100 linii" in form.errors["code"][0]


def test_library_requires_authentication(client):
    response = client.get(reverse("analysis-list"))
    assert response.status_code == 302
    assert reverse("login") in response.url


def test_users_cannot_open_someone_elses_analysis(client, user):
    other = get_user_model().objects.create_user(username="other")
    analysis = Analysis.objects.create(owner=other, code="print('secret')")
    client.force_login(user)
    assert client.get(analysis.get_absolute_url()).status_code == 404


def test_create_stores_owner_and_dispatches_task(client, user):
    client.force_login(user)
    with patch("analyses.views.generate_analysis.delay") as delay:
        response = client.post(reverse("analysis-create"), {"code": "print('hello')"})
    analysis = Analysis.objects.get()
    assert response.status_code == 302
    assert analysis.owner == user
    delay.assert_called_once_with(str(analysis.pk))


def test_ai_task_saves_versioned_result(user):
    analysis = Analysis.objects.create(owner=user, code="print('hello')")
    result = CodeAnalysisV1(
        schema_version=1,
        language="Python",
        title="Wypisanie tekstu",
        short_description="Prosty przykład.",
        tags=["python", "print"],
        summary="Kod wypisuje tekst.",
        explanation="Wywołuje funkcję print.",
        concepts="Wywołanie funkcji.",
        pitfalls="Brak.",
        junior_explanation="print pokazuje wartość w konsoli.",
    )
    with patch("analyses.tasks.analyze_code", return_value=result):
        generate_analysis(str(analysis.pk))
    analysis.refresh_from_db()
    assert analysis.status == Analysis.Status.COMPLETED
    assert analysis.schema_version == 1
    assert analysis.language == "Python"


def test_ai_failure_has_retry_message(user):
    analysis = Analysis.objects.create(owner=user, code="broken")
    with patch("analyses.tasks.analyze_code", side_effect=RuntimeError("secret provider error")):
        generate_analysis(str(analysis.pk))
    analysis.refresh_from_db()
    assert analysis.status == Analysis.Status.FAILED
    assert "Spróbuj ponownie" in analysis.error_message
    assert "secret" not in analysis.error_message
