# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from django.utils.translation import ugettext_lazy as _
from django import forms
from .. import models
from ckeditor.widgets import CKEditorWidget

log = logging.getLogger(__name__)


class PlanForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    replication_topology = forms.ModelChoiceField(
        queryset=models.ReplicationTopology.objects.all()
    )

    class Meta:
        model = models.Plan

    def clean_has_persistence(self):
        engine = self.cleaned_data['engine']
        if not engine.engine_type.is_in_memory:
            return True
        return self.cleaned_data['has_persistence']

    def clean(self):
        cleaned_data = super(PlanForm, self).clean()

        engine = cleaned_data.get("engine")
        if not engine:
            msg = _("Please select a Engine Type")
            log.warning(u"%s" % msg)
            raise forms.ValidationError(msg)

        is_default = cleaned_data.get("is_default")
        if not is_default:
            if self.instance.id:
                plans = models.Plan.objects.filter(
                    is_default=True, engine=engine).exclude(id=self.instance.id)
            else:
                plans = models.Plan.objects.filter(
                    is_default=True, engine=engine)
            if not plans:
                msg = _("At least one plan must be default")
                log.warning(u"%s" % msg)
                raise forms.ValidationError(msg)

        return cleaned_data


class PlanAttributeInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        # if count < 1:
        #     log.warning(u"%s" % _("You must have at least one plan attribute"))
        #     raise forms.ValidationError(_("You must have at least one plan attribute"))
