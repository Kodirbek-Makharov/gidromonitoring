from django.contrib import admin
from monitoring.models import Dalolatnoma, Viloyat, Tuman, Noqonuniy_holat_turi, Stansiya, DalolatnomaRasm
# Register your models here.

class DalolatnomaRasmAdmin(admin.StackedInline):
    model = DalolatnomaRasm

class DalolatnomaAdmin(admin.ModelAdmin):
    # model = Datasets
    list_display = ["korsatma_raqam", "inspektor", "noqonuniy_holat_turi"]
    inlines = [DalolatnomaRasmAdmin,]
    # list_filter = ["korsatma_raqam", "inspektor", "noqonuniy_holat_turi"]

    pass


admin.site.register(Dalolatnoma, DalolatnomaAdmin)
admin.site.register(Viloyat)
admin.site.register(Tuman)
admin.site.register(Noqonuniy_holat_turi)
admin.site.register(Stansiya)
# admin.site.register(DalolatnomaRasm, DalolatnomaRasmAdmin)
