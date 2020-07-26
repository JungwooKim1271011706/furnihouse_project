from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from django.views.generic.list import MultipleObjectMixin
from .models import Request
from .models import Notion
from .forms import RequestForm
from django.utils import timezone
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.

def login(request):
    return render(request, 'registration/login.html')

class vendorview(TemplateView):
    template_name = "cs/vendor_list.html"

class Requestview(MultipleObjectMixin, CreateView):
    model = Request
    fields = "__all__"
    template_name = "cs/request.html"
    success_rul = "cs/request/"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset() # DB에서 레코드들을 꺼내오는 메소드get_queryset()
        # get_queryset() 메소드는 어느쪽에 있는 것을 호출할까? (MultipleObjectMixin, CreateView)
        # 이럴 때 순서가 중요하다, 앞에 있는 클래스를 먼저 봐서 이 클래스에 get_queryset 메소드가
        # 있다면 그걸 호출하고, 거기에 없으면 CreateView에서 찾아서 get_queryset() 메소드를 호출
        # 둘 다 get_queryset() 메소드가 있기 때문에 MultipleObjectMixin 에 있는 것이 호출된다.
        return super().get(request, *args, **kwargs)
        # 상위 클래스(Requestview)의 get 메소드를 그대로 호출하게 되면, CreateView클래스의
        # get_context_data 메소드가 호출되고, 이 메소드에서 object_list라는 context변수가
        # 템플릿에 넘어가게 되는 것이다.
        # 그리고 상위 클래스의 메소드를 오버라이딩 할 때는 인자는 동일하게 써줘야 한다.

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().post(request, *args, **kwargs) # 인자는 동일하게


class RequestUpdateView(UpdateView):
        model = Request
        field = ['text']
        template_name_suffix = ""


# class RequestFormview(FormView):
#     form_class = RequestForm
#     template_name = "cs/request.html"
#     success_url = "/cs/request/"

#     def form_valid(self, form):
#         form.save()
#         return super(RequestFormview, self).form_valid(form)

class RequestDelete(DeleteView):
    model = Request
    success_url = "/cs/request/"
    context_object_name = "request_list"


@method_decorator(login_required, name="dispatch")
class CrudView(ListView):
    model=Request
    template_name='cs/crud.html'
    context_object_name = 'request_datas'

# index = CrudView.as_view()

class CreateCrudRequest(View):

    def get(self, request):
        author1 = request.user #simplelazyobject
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        phone_number1 = request.GET.get('phone_number', None)
        text1 = request.GET.get('text', None)
        
        obj = Request.objects.create(
            author = author1,
            name = name1,
            address = address1,
            phone_number = phone_number1,
            text = text1,
        )

        request_data = {'id': obj.id, 'author' : str(obj.author), 'name':obj.name,\
            'address':obj.address, 'phone_number':obj.phone_number, 'text':obj.text,\
             }

        data = {
            'request_data' : request_data
        }
        return JsonResponse(data)
        
class UpdateCrudRequest(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        phone_number1 = request.GET.get('phone_number', None)
        text1 = request.GET.get('text', None)

        obj = Request.objects.get(id=id1)
        # obj.author = author1
        obj.name = name1
        obj.address = address1
        obj.phone_number = phone_number1
        obj.text = text1
        obj.save()
        
        request_data = {'id': obj.id, 'name':obj.name, 'address':obj.address, 'phone_number':obj.phone_number, 'text':obj.text}
        
        data = {
            'request_data':request_data
        }
        return JsonResponse(data)

class DeletCrudRequest(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Request.objects.get(id=id1).delete()
        data = {
            'deleted' : True
        }
        return JsonResponse(data)

class Editstatus(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        obj = Request.objects.get(id=id1)
        if obj.status is False:
            obj.status = True
        else:
            obj.status = False
        
        obj.save()
        request_status = {'id' : obj.id, 'status' :obj.status}

        data = {
            'request_status' : request_status
        }
        return JsonResponse(data)


# @method_decorator(login_required, name="dispatch")
# class NotionView(ListView):
#     model = Notion
#     template_name = 'cs/crud.html'
#     context_object_name = 'notions'