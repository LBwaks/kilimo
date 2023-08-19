from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from formtools.wizard.views import SessionWizardView
from .forms import LandForm,LandLocationForm,LandCoordinatesForm,LandResourcesForm,LandInfrastructureForm,LandImagesForm
from .models import Land
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


class LandListView(ListView):
    model = Land
    template_name = "lands/lands.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            "period_lease", "owner"
        )  # .prefetch_related()
        return queryset


class LandDetailView(DetailView):
    model = Land
    template_name = "lands/land-detail.html"
    # create a folium map center 
    # add a marker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["land"] = self.get_object()
        return context
def show_coordinates_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('3') or {}
    return cleaned_data.get("show_coordinates")

class LandWizard(SessionWizardView):
    form_list =[LandForm,LandResourcesForm,LandInfrastructureForm,LandLocationForm,LandCoordinatesForm,LandImagesForm]
    template_name = "lands/add-land.html"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media/lands'))
    condition_dict={'4':show_coordinates_form}
    def done(self, form_list, **kwargs):
        # file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media/lands'))
        
        print(form_list)
        # return render(self.request, 'done.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })
        land = 
        land_images = form_list[-1].save(commit=False)
        land_images.land = land
        land_images.save()
        return HttpResponse("Form submitted")