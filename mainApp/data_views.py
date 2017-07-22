# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import *
from .forms import *

from Districts import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .views import IsAdmin
import json
from django.contrib.postgres.search import SearchVector, SearchQuery
from watson import search as watson
from dateutil import parser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class IsAdmin(UserPassesTestMixin):
    def test_func(self):
        try:
            return 'admin' == str(self.request.user.groups.all()[0])
        except:
            return False


class LoginRequired(LoginRequiredMixin):
    login_url = '/login/'



class HomeView(LoginRequired,View):
    template_name = 'mainApp/landing_page.html'
    def get(self, request):
        # datapoints = DataPoint.objects.all()[:10][::-1]
        search_form = SearchForm()
        district_list = list(dist_choices)
        labs = Lab.objects.all().values('name')
        users = User.objects.all()
        return render(request,self.template_name)
    def post(self, request):
        datapoints = DataPoint.objects.all()[:10][::-1]
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            any_term = search_form.cleaned_data.get('any_term')
            if any_term:
                datapoints = []
                ws = watson.filter(DataPoint,any_term,ranking=False)
                for q in ws:
                    datapoints.append(DataPoint.objects.get(id=str(q)[3:]))
            else:
                datapoints = DataPoint.objects.all()
                district = search_form.cleaned_data.get('district')
                if district:
                    datapoints = DataPoint.objects.filter(district=district)
                lab = search_form.cleaned_data.get('lab')
                if lab:
                    l = Lab.objects.get(name=lab)
                    datapoints = datapoints.filter(lab=l)
                user = search_form.cleaned_data.get('user')
                if user:
                    u = User.objects.get(username=user)
                    datapoints = datapoints.filter(added_by=u)
                patient_name = search_form.cleaned_data.get('patient_name')
                if patient_name:
                    datapoints = datapoints.filter(patient_name__search=str(patient_name))
                patient_age = search_form.cleaned_data.get('patient_age')
                if patient_age:
                    datapoints = datapoints.filter(age=patient_age)

                if search_form.cleaned_data.get('date_start'):
                    date_start = parser.parse(search_form.cleaned_data.get('date_start'))
                    date_end = parser.parse(search_form.cleaned_data.get('date_end'))
                    datapoints = datapoints.filter(date__range=(date_start, date_end))

        # district_list = list(dist_choices)
        # labs = Lab.objects.all().values('name')
        # users = User.objects.all()
        # return render(request, self.template_name, {'datapoints':datapoints,'search_form':search_form,'district_list':district_list,
        #                                           'labs':labs,'users':users})

class TestDataAdd(LoginRequired, generic.CreateView):
    model = TestData
    fields = ['test_parameter', 'lot_number', 'control_level', 'control_data','remarks']

    def form_valid(self, form):
        data = form.save()
        data.added_by = self.request.user
        data.lab = self.request.user.userprofile.lab
        data.district = self.request.user.userprofile.lab.district
        data.save()
        return HttpResponseRedirect(reverse('mainapp:testdata-detail', kwargs={'pk': data.pk}))

class TestDataDetail(IsAdmin, LoginRequired, generic.DetailView):
    model = TestData
    template_name = 'mainApp/testdata_detail.html'


class TestDataUpdate(IsAdmin, LoginRequired, generic.UpdateView):
    model = TestData
    fields = ['control_data','remarks']

class TestParameterAdd(IsAdmin, LoginRequired, generic.CreateView):
    model = TestParameter
    fields = ['parameter_name', 'description']

    def form_valid(self, form):
        data = form.save()
        data.added_by = self.request.user
        data.lab = self.request.user.userprofile.lab
        data.save()
        return HttpResponseRedirect(reverse('mainapp:parameter-detail', kwargs={'pk': data.pk}))


class TestParameterDetail(IsAdmin, LoginRequired,generic.DetailView):
    model = TestParameter
    template_name = 'mainApp/testparameter_detail.html'

class TestParameterList(IsAdmin, LoginRequired, generic.ListView):
    model = TestParameter
    context_object_name = 'all_parameters'
    template_name = 'mainApp/testparameters.html'
    def get_queryset(self):
        return TestParameter.objects.all()


class TestParameterUpdate(IsAdmin, LoginRequired, generic.UpdateView):
    model = TestParameter
    fields = ['parameter_name', 'description']

def get_labs_ajax(request):
    #http://localhost:8000/get_labs_ajax/?district=DHAKA
    district = request.GET['district']
    dist_id=0
    for d in dist_choices:
        if d[1]==district:
            dist_id=d[0]

    labs = Lab.objects.filter(district=dist_id).values('name')
    resp=""
    for l in labs:
        resp+='<option value={}>'.format(l['name'])

    return HttpResponse(resp)

def get_users_ajax(request):
    # http://localhost:8000/get_users_ajax/?district=DHAKA&lab=ICDDRB
    district = request.GET['district']
    lab = request.GET['lab']
    dist_id = 0

    for d in dist_choices:
        if d[1] == district:
            dist_id = d[0]
    labs=Lab.objects.all()
    if dist_id:
        labs = labs.filter(district=dist_id)
    if lab:
        labs = labs.filter(name=lab)
    resp=""

    for l in labs:
        for u in l.userprofile_set.all():
            resp+='<option value={}>'.format(u)
    return HttpResponse(resp)
