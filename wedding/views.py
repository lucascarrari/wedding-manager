from urllib.parse import quote
import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import GuestCreateForm, GuestEditForm, RSVPForm
from .models import Expense, Guest


WEDDING_DATE_STR = "2029-09-29 18:00:00"


def home(request):
    context = {
        "wedding_date": WEDDING_DATE_STR,
        "couple_names": "Lucas & Marcelly",
        "monogram": "LM",
    }
    return render(request, "home.html", context)


@login_required
def dashboard(request):
    expenses = Expense.objects.all()
    guests = Guest.objects.all()

    # só convidados principais na tabela
    main_guests = (
        Guest.objects
        .filter(main_guest__isnull=True)
        .prefetch_related("companions")
        .order_by("-created_at")
    )

    # financeiro
    total_expenses = round(
        expenses.aggregate(total=Sum("value"))["total"] or 0, 2
    )
    total_paid = round(
        expenses.filter(status="pago").aggregate(total=Sum("value"))["total"] or 0, 2
    )
    total_pending = round(
        expenses.filter(status="pendente").aggregate(total=Sum("value"))["total"] or 0, 2
    )

    # convidados
    total_guests = guests.count()
    confirmed_guests = guests.filter(confirmed=True).count()
    not_confirmed = guests.filter(confirmed=False).count()

    confirmed_main_guests = guests.filter(
        confirmed=True,
        main_guest__isnull=True,
    ).count()

    total_main_guests = guests.filter(main_guest__isnull=True).count()
    confirmed_people_total = guests.filter(confirmed=True).count()
    companions_total = guests.filter(main_guest__isnull=False).count()

    if total_main_guests > 0:
        confirmation_rate = round((confirmed_main_guests / total_main_guests) * 100, 1)
    else:
        confirmation_rate = 0

    # gráfico por categoria
    expenses_by_category = (
        expenses.values("category__name")
        .annotate(total=Sum("value"))
        .order_by("-total")
    )

    category_labels = [item["category__name"] for item in expenses_by_category]
    category_values = [float(item["total"]) for item in expenses_by_category]

    # links RSVP / WhatsApp
    base_url = request.build_absolute_uri("/").rstrip("/")

    guest_rows = []
    for guest in main_guests:
        rsvp_url = f"{base_url}{reverse('rsvp_confirm', args=[guest.rsvp_token])}"

        whatsapp_url = None
        if guest.phone:
            phone_number = re.sub(r"\D", "", guest.phone)
            if phone_number and not phone_number.startswith("55"):
                phone_number = f"55{phone_number}"

            message = (
                f"Olá, {guest.name}! 💍\n\n"
                f"Lucas & Marcelly ficariam muito felizes com sua presença nesse dia tão especial.\n\n"
                f"Confirme sua presença aqui:\n{rsvp_url}"
            )
            whatsapp_url = f"https://wa.me/{phone_number}?text={quote(message)}"

        guest_rows.append(
            {
                "guest": guest,
                "rsvp_url": rsvp_url,
                "whatsapp_url": whatsapp_url,
                "companions_count": guest.companions.count(),  # type: ignore[attr-defined]
                "edit_form": GuestEditForm(instance=guest),
            }
        )

    context = {
        "wedding_date": WEDDING_DATE_STR,
        "total_expenses": total_expenses,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "total_guests": total_guests,
        "confirmed_guests": confirmed_guests,
        "not_confirmed": not_confirmed,
        "confirmed_main_guests": confirmed_main_guests,
        "total_main_guests": total_main_guests,
        "confirmed_people_total": confirmed_people_total,
        "companions_total": companions_total,
        "confirmation_rate": confirmation_rate,
        "category_labels": category_labels,
        "category_values": category_values,
        "guest_rows": guest_rows,
        "guest_form": GuestCreateForm(),
    }

    return render(request, "dashboard.html", context)


@login_required
def add_guest(request):
    if request.method == "POST":
        form = GuestCreateForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.confirmed = False
            guest.save()
    return redirect("dashboard")


@login_required
def edit_guest(request, guest_id):
    guest = get_object_or_404(Guest, id=guest_id, main_guest__isnull=True)

    if request.method == "POST":
        form = GuestEditForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()

    return redirect("dashboard")


def public_rsvp(request):
    if request.method == "POST":
        form = RSVPForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            email = form.cleaned_data["email"].strip() if form.cleaned_data["email"] else ""

            main_guest = None

            if email:
                main_guest = Guest.objects.filter(
                    email__iexact=email,
                    main_guest__isnull=True,
                ).first()

            if not main_guest:
                main_guest = Guest.objects.filter(
                    name__iexact=name,
                    main_guest__isnull=True,
                ).first()

            if not main_guest:
                main_guest = Guest.objects.create(
                    name=name,
                    email=email if email else None,
                    confirmed=True,
                    guest_type="amigo",
                    invited_by="noivo",
                )
            else:
                main_guest.name = name
                main_guest.email = email if email else main_guest.email
                main_guest.confirmed = True
                main_guest.save()

            main_guest.companions.all().delete()  # type: ignore[attr-defined]

            companions_count = form.cleaned_data["companions_count"]

            for i in range(1, companions_count + 1):
                companion_name = form.cleaned_data.get(f"companion_{i}")

                if companion_name:
                    companion_name = companion_name.strip()
                    if companion_name:
                        Guest.objects.create(
                            name=companion_name,
                            email=None,
                            confirmed=True,
                            guest_type="agregado",
                            invited_by=main_guest.invited_by,
                            main_guest=main_guest,
                        )

            if main_guest.email:
                subject = "Confirmação recebida — Lucas & Marcelly 💍"
                message = (
                    f"Olá, {main_guest.name}!\n\n"
                    "Que alegria receber sua confirmação! 💚\n"
                    "Obrigado por confirmar presença nesse dia tão especial para nós.\n\n"
                    "Com carinho,\n"
                    "Lucas & Marcelly"
                )

                from_email = getattr(
                    settings,
                    "DEFAULT_FROM_EMAIL",
                    "no-reply@wedding.local",
                )

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[str(main_guest.email)],
                    fail_silently=False,
                )

            companions_count = main_guest.companions.count()  # type: ignore[attr-defined]
            total_people = 1 + companions_count

            return render(
                request,
                "rsvp_success.html",
                {
                    "guest": main_guest,
                    "companions_count": companions_count,
                    "total_people": total_people,
                },
            )
    else:
        form = RSVPForm()

    return render(request, "public_rsvp.html", {"form": form})


def rsvp_confirm(request, token):
    guest = get_object_or_404(Guest, rsvp_token=token)

    if request.method == "POST":
        form = RSVPForm(request.POST)

        if form.is_valid():
            guest.name = form.cleaned_data["name"].strip()
            guest.email = (
                form.cleaned_data["email"].strip()
                if form.cleaned_data["email"]
                else guest.email
            )
            guest.confirmed = True
            guest.save()

            guest.companions.all().delete()  # type: ignore[attr-defined]

            companions_count = form.cleaned_data["companions_count"]

            for i in range(1, companions_count + 1):
                companion_name = form.cleaned_data.get(f"companion_{i}")

                if companion_name:
                    companion_name = companion_name.strip()
                    if companion_name:
                        Guest.objects.create(
                            name=companion_name,
                            email=None,
                            confirmed=True,
                            guest_type="agregado",
                            invited_by=guest.invited_by,
                            main_guest=guest,
                        )

            if guest.email:
                subject = "Confirmação recebida — Lucas & Marcelly 💍"
                message = (
                    f"Olá, {guest.name}!\n\n"
                    "Que alegria receber sua confirmação! 💚\n"
                    "Obrigado por confirmar presença nesse dia tão especial para nós.\n\n"
                    "Com carinho,\n"
                    "Lucas & Marcelly"
                )

                from_email = getattr(
                    settings,
                    "DEFAULT_FROM_EMAIL",
                    "no-reply@wedding.local",
                )

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[str(guest.email)],
                    fail_silently=False,
                )

            companions_count = guest.companions.count()  # type: ignore[attr-defined]
            total_people = 1 + companions_count

            return render(
                request,
                "rsvp_success.html",
                {
                    "guest": guest,
                    "companions_count": companions_count,
                    "total_people": total_people,
                },
            )
    else:
        companions = list(guest.companions.all())  # type: ignore[attr-defined]
        form = RSVPForm(
            initial={
                "name": guest.name,
                "email": guest.email or "",
                "companions_count": len(companions),
                "companion_1": companions[0].name if len(companions) > 0 else "",
                "companion_2": companions[1].name if len(companions) > 1 else "",
                "companion_3": companions[2].name if len(companions) > 2 else "",
                "companion_4": companions[3].name if len(companions) > 3 else "",
                "companion_5": companions[4].name if len(companions) > 4 else "",
                "companion_6": companions[5].name if len(companions) > 5 else "",
                "companion_7": companions[6].name if len(companions) > 6 else "",
                "companion_8": companions[7].name if len(companions) > 7 else "",
                "companion_9": companions[8].name if len(companions) > 8 else "",
                "companion_10": companions[9].name if len(companions) > 9 else "",
            }
        )

    return render(
        request,
        "rsvp_confirm.html",
        {
            "guest": guest,
            "form": form,
        },
    )