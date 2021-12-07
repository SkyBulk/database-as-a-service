# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django_services import admin as services_admin
from ..service.offering import OfferingService



class OfferingAdmin(services_admin.DjangoServicesAdmin):
    service_class = OfferingService
    search_fields = (
       'name',
    )
    list_display = (
       'name', 'cpus', 'memory_size_mb', 'selected_environments'
    )
    list_filter = ("cpus", "memory_size_mb", "environments")

    def selected_environments(self, obj):
        return ",".join(obj.environments.values_list('name', flat=True))

    save_on_top = True
    filter_horizontal = ("environments",)
