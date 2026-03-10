from django.contrib import admin
from django.utils.html import format_html
from urllib.parse import quote
import re

from .models import Guest, Expense, Category


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "guest_type",
        "invited_by",
        "confirmed",
        "email",
        "phone",
        "main_guest_display",
        "rsvp_link",
        "whatsapp_link",
        "created_at",
    )

    list_filter = (
        "confirmed",
        "invited_by",
        "guest_type",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    readonly_fields = (
        "rsvp_token",
        "created_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Informações principais", {
            "fields": (
                "name",
                "email",
                "phone",
                "guest_type",
                "invited_by",
                "confirmed",
            )
        }),
        ("Relacionamentos", {
            "fields": (
                "main_guest",
            )
        }),
        ("Sistema", {
            "fields": (
                "rsvp_token",
                "created_at",
                "notes",
            )
        }),
    )

    def main_guest_display(self, obj):
        if obj.main_guest:
            return obj.main_guest.name
        return "-"
    main_guest_display.short_description = "Convidado principal"

    def rsvp_link(self, obj):
        if obj.rsvp_token:
            return format_html(
                '<a href="/rsvp/{}/" target="_blank">Abrir RSVP</a>',
                obj.rsvp_token
            )
        return "-"
    rsvp_link.short_description = "Link RSVP"

    def whatsapp_link(self, obj):
        if not obj.rsvp_token:
            return "-"

        if not obj.phone:
            return "Sem telefone"

        # remove tudo que não for número
        phone_number = re.sub(r"\D", "", obj.phone)

        # adiciona 55 se a pessoa salvou só com DDD+número
        if phone_number and not phone_number.startswith("55"):
            phone_number = f"55{phone_number}"

        base_url = "http://127.0.0.1:8000"
        rsvp_url = f"{base_url}/rsvp/{obj.rsvp_token}/"

        message = (
            f"Olá, {obj.name}! 💍\n\n"
            f"Lucas & Marcelly ficariam muito felizes com sua presença nesse dia tão especial.\n\n"
            f"Confirme sua presença aqui:\n{rsvp_url}"
        )

        whatsapp_url = f"https://wa.me/{phone_number}?text={quote(message)}"

        return format_html(
            '<a href="{}" target="_blank">Enviar WhatsApp</a>',
            whatsapp_url
        )
    whatsapp_link.short_description = "WhatsApp"


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "value",
        "status",
        "date",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = ("-date",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)