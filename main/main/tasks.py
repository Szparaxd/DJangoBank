from celery import shared_task
from celery.utils.log import get_task_logger
from bank.models import Kredyt,CyklicznePrzelewy


logger = get_task_logger(__name__)


@shared_task
def sample_task():
    for _kredyt in Kredyt:
        bankkredytu = _kredyt.konto
        bankkredytu.withDrawnBalance(_kredyt.kosztMiesieczny)

    for _przelew in CyklicznePrzelewy:
        _przelew.execute()
    pass
