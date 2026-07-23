import logging

from celery import shared_task
from django.db import transaction

from .models import Analysis
from .services import analyze_code

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(TimeoutError,), retry_backoff=True, max_retries=1)
def generate_analysis(analysis_id: str) -> None:
    analysis = Analysis.objects.get(pk=analysis_id)
    analysis.status = Analysis.Status.PROCESSING
    analysis.error_message = ""
    analysis.save(update_fields=["status", "error_message", "updated_at"])
    try:
        result = analyze_code(analysis.code)
        with transaction.atomic():
            analysis = Analysis.objects.select_for_update().get(pk=analysis_id)
            for field, value in result.model_dump().items():
                setattr(analysis, field, value)
            analysis.status = Analysis.Status.COMPLETED
            analysis.rating = ""
            analysis.save()
    except Exception:
        logger.exception("AI analysis failed", extra={"analysis_id": analysis_id})
        Analysis.objects.filter(pk=analysis_id).update(
            status=Analysis.Status.FAILED,
            error_message="Nie udało się wygenerować analizy. Spróbuj ponownie.",
        )
