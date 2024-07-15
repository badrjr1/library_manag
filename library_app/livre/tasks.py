from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Loans , Penalty

@shared_task
def send_reminders():
    overdue_loans = Loans.objects.filter(due_date__lt=timezone.now(), return_date__isnull=True, reminder_sent=False)
    for loan in overdue_loans:
        send_mail(
            'Reminder: Overdue Item',
            f'Dear {loan.member.first_name},\n\nThe item {loan.book.title} was due on {loan.due_date}. Please return it as soon as possible.',
            'bibliothequehb@biblio.com',
            [loan.member.email],
            fail_silently=False,
        )
        loan.reminder_sent = True
        loan.save()
        Penalty.objects.create(
            loan =loan,
            reason='depasse le temps d''emprunte'
        )