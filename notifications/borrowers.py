from datetime import timedelta, date

from borrowings.models import Borrowing


def borrowers_overdue() -> str:
    queryset = Borrowing.objects.all()

    borrowings = []
    tomorrow = date.today() + timedelta(1)

    overdue = queryset.filter(expected_return_date__lte=tomorrow, actual_return_date=None)
    if len(overdue) == 0:
        return "No borrowings overdue today!"
    for count, borrowing in enumerate(overdue, start=1):
        borrowings.append(f"{count}. {borrowing} expected date {borrowing.expected_return_date}")

    borrowings = "\n".join(borrowings)
    return borrowings
