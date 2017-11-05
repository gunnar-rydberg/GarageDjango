from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from datetime import datetime, timezone

from . models import Vehicle
from .models import Vehicle, GarageMember, VehicleType

from django import forms

class VehicleTypeForm(forms.Form):
    """Search form"""
    vehicle_type = forms.ChoiceField(
        choices=[(0,'Any')] + list(VehicleType.objects.all().order_by('name').values_list('id','name')), 
        required=False,
        widget=forms.Select)

class VehicleListView(View):
    """List vehicles"""
    def get(self, request):
        search_regno = request.GET.get('regno','')
        search_type = int(request.GET.get('vehicle_type',"0"))
        search_brand = request.GET.get('brand','')
        search_model = request.GET.get('model','')

        filters = Q()
        if search_regno != '':
            filters = filters & Q(reg_no__contains=search_regno)
        if search_type > 0:
            filters = filters & Q(vehicle_type=search_type)
        if search_brand != '':
            filters = filters & Q(brand__contains=search_brand)
        if search_model != '':
            filters = filters & Q(model__contains=search_model)
        vehicles = Vehicle.objects.filter(filters).order_by('reg_no')

        return render(request, 'garage_app/vehicle_list.html', {'object_list': vehicles, 'form':VehicleTypeForm()})

class VehicleDetailView(DetailView):
    """Vehicle details"""
    model = Vehicle
    template = 'vehicle_detail.html'
    template_name = 'garage_app/vehicle_detail.html'

class VehicleParkForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ('owner','reg_no','vehicle_type','brand','model','no_of_wheels')


class VehicleParkView(View):
    """Park new vehicle"""
    def get(self, request):
        form = VehicleParkForm()
        return render(request, 'garage_app/vehicle_park.html', {'form': form})

    def post(self, request, *args, **kwars):
        """Validate park form and save vehicle with timestamp"""
        form = VehicleParkForm(request.POST)
        if form.is_valid():
            reg_no = form.cleaned_data['reg_no']
            if Vehicle.objects.filter(reg_no=reg_no).exists():
                form.add_error('reg_no', "Reg.No: '{}' is already registered".format(reg_no))
            else:
                vehicle = form.save(commit=False)
                #vehicle.park_date = timezone.now()
                vehicle.save()
                return redirect('vehicle_list')
        return render(request, 'garage_app/vehicle_park.html', {'form': form})
        
class VehicleEditView(UpdateView):
    """Update entry"""
    model = Vehicle
    fields = ['reg_no', 'brand', 'model']
    template_name = 'garage_app/vehicle_edit.html'

class VehicleCheckoutView(View):
    def get(self, request, pk):
        print("TEST {}".format("BAR"))
        vehicle = Vehicle.objects.get(pk=pk)

        return render(request, 'garage_app/vehicle_checkout.html', {'vehicle': vehicle})

    def post(self, request, *args, **kwars):
        print("CHECKOUT POST")

        vehicle = Vehicle.objects.get(pk=kwars['pk'])
        d = datetime.now(timezone.utc) - vehicle.park_time
        parking_time = "{} day(s) {} hour(s)".format(d.days, d.seconds // 3600)
        #TODO create timespan formatter!
        vehicle.delete()

        return render(request, 'garage_app/vehicle_receipt.html', {'vehicle': vehicle, 'parking_time': parking_time})

class GarageMemberCreate(CreateView):
    model = GarageMember
    fields = '__all__'
    template = 'member_create'
    template_name = 'garage_app/member_create.html'
    success_url = reverse_lazy('vehicle_list')

