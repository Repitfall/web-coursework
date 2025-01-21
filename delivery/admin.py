from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics, ttfonts
from .models import (
    UserAddress,
    Courier,
    Restaurant,
    RestaurantGroup,
    RestaurantDish,
    Order,
    OrderDish,
    Ticket,
)


@admin.register(UserAddress)
class UserAddressAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id_user", "address"]
    raw_id_fields = ["id_user"]
    search_fields = ["id_user", "address"]


@admin.register(Courier)
class CourierAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["last_name", "first_name"]
    search_fields = ["last_name"]


class RestaurantResource(resources.ModelResource):
    class Meta:
        model = Restaurant
        fields = ["id", "title", "info"]

    def dehydrate_info(self, resources):
        return resources.info or "-"


class RestaurantGroupInline(admin.StackedInline):
    model = RestaurantGroup


@admin.register(Restaurant)
class RestaurantAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = RestaurantResource
    list_display = ["title"]
    search_fields = ["title"]
    inlines = [RestaurantGroupInline]


class RestaurantGroupResource(resources.ModelResource):
    class Meta:
        model = RestaurantGroup
        fields = ["id", "id_restaurant__title", "title", "info"]

    def dehydrate_info(self, resources):
        return resources.info or "-"


class RestaurantDishInline(admin.StackedInline):
    model = RestaurantDish


@admin.register(RestaurantGroup)
class RestaurantGroupAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = RestaurantGroupResource
    list_display = ["title", "id_restaurant"]
    list_filter = ["id_restaurant"]
    search_fields = ["title"]
    inlines = [RestaurantDishInline]


class RestaurantDishResource(resources.ModelResource):
    class Meta:
        model = RestaurantDish
        import_id_fields = ("id",)
        fields = [
            "id",
            "id_group__id_restaurant__title",
            "id_group__title",
            "title",
            "info",
        ]

    def dehydrate_info(self, resources):
        return resources.info or "-"


@admin.register(RestaurantDish)
class RestaurantDishAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    date_hierarchy = "date_created"
    resource_class = RestaurantDishResource
    list_display = [
        "title",
        "id_group",
        "id_group__id_restaurant",
        "date_created",
        "short_description",
    ]
    raw_id_fields = ["id_group"]
    readonly_fields = ["date_created"]
    list_filter = ["id_group"]
    search_fields = ["title", "info"]
    actions = ["generate_pdf"]

    def short_description(self, obj):
        return obj.info[:30] + "..." if len(obj.info) > 30 else obj.info

    def generate_pdf(self, request, queryset):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        y_pos = 10.5 * inch

        pdfmetrics.registerFont(ttfonts.TTFont("Times-Roman", "Times New Roman.ttf"))

        for dish in queryset:
            obj = p.beginText()
            obj.setTextOrigin(inch, y_pos)
            obj.setFont("Times-Roman", 14)
            obj.textLine(f"Название: {dish.title}")
            obj.textLine(f"Стоимость: {dish.price} рублей")
            obj.textLine(f"Группа: {dish.id_group}")
            obj.textLine(f"Ресторан: {dish.id_group.id_restaurant}")
            obj.textLine("-" * 50)

            p.drawText(obj)
            y_pos -= 1.5 * inch
            if y_pos <= inch:
                p.showPage()
                y_pos = 10.5 * inch

        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="dishes.pdf")

    generate_pdf.short_description = "Экспортировать в PDF"


class OrderDishInline(admin.StackedInline):
    model = OrderDish
    raw_id_fields = ["id_dish"]


@admin.register(Order)
class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "id_user"]
    search_fields = ["id_user"]
    inlines = [OrderDishInline]


@admin.register(OrderDish)
class OrderDishAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "id_order"]
    search_fields = ["id_order"]


@admin.register(Ticket)
class TicketAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id_order"]
    search_fields = ["id_order"]
    list_display_links = ["id_order"]
