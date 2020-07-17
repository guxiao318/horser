from django.shortcuts import render,HttpResponse,redirect
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Interface_Info,Domain_Info
from django.forms import model_to_dict

# Create your views here.

def horser_login(request):
    if request.method == "GET":
        html = "login.html"
        return render(request,html)





def horser_index(request):
    if request.method == "GET":


        html = "horser_index.html"

        return render(request,html)


def horser_help(request):
    if request.method == "GET":
        html = "horser_help.html"

        return render(request,html)


def domain_manage(request):
    if request.method == "GET":
        html = "domain_manage.html"

        return render(request,html)

@csrf_exempt
def domain_add(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典
        domain_name = receive_data['domain_name']
        domain_brief = receive_data['domain_brief']

        try:
            if domain_name.strip() =="":
                raise Exception
        except Exception:
            resp = {'code':'000001','msg':'必填项不能为空'}
        else:
            if Domain_Info.objects.filter(domain_name=domain_name).exists():
                resp = {'code': '000002', 'msg': '添加失败，该领域已存在！'}
            else:
                Domain_Info.objects.create(domain_name=domain_name,domain_brief=domain_brief)
                resp = {'code': '000000', 'msg': '添加成功'}

    return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")





@csrf_exempt
def interface_add(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        interface_name = receive_data['interface_name']
        interface_type = receive_data['interface_type']
        interface_url = receive_data['interface_url']
        interface_mock = receive_data['interface_mock']
        input_field_list = receive_data['input_field_list']
        input_need_list = receive_data['input_need_list']
        input_demo_list = receive_data['input_demo_list']
        belong_subsys = receive_data['belong_subsys']
        belong_group = receive_data['belong_group']
        belong_git_base = receive_data['belong_git_base']
        belong_svn_base = receive_data['belong_svn_base']

        input_list_need = [interface_name,interface_type,interface_url,belong_subsys] #必填项列表
        input_field_list = ",".join(input_field_list)#列表转换为字符串
        input_need_list = ",".join(input_need_list)
        input_demo_list = ",".join(input_demo_list)

        input_dict = {"interface_name":interface_name,"interface_type":interface_type,"input_field_list":input_field_list,
                      "input_need_list":input_need_list,"input_demo_list":input_demo_list,"interface_url":interface_url,"belong_group":belong_group,"belong_subsys":belong_subsys,"belong_git_base":belong_git_base,
                      "belong_svn_base":belong_svn_base,"interface_mock":interface_mock}

        try:
            for i in input_list_need:
                if i.strip() == '':
                    raise Exception

        except Exception:
            resp = {'code':'000001','msg':'必填项不能为空'}

        else:
            if Interface_Info.objects.filter(interface_name=interface_name,belong_subsys=belong_subsys).exists():#检查接口是否已存在
                resp = {'code': '000002', 'msg': '添加失败，该子系统下接口已存在'}
            else:#子系统下接口不存在则添加
                created_time = datetime.now()
                input_dict["created_time"] = created_time
                Interface_Info.objects.create(**input_dict)

                resp = {'code': '000000', 'msg': '添加成功'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



    else:
        html = "interface_add.html"
        return render(request,html)


def interface_detail(request,jiekouId):

    try:
        r = Interface_Info.objects.get(id=jiekouId)

        if r !=None:
            r_dict = model_to_dict(r)
            input_field_list = r_dict["input_field_list"].split(",")
            input_need_list= r_dict["input_need_list"].split(",")
            input_demo_list = r_dict["input_demo_list"].split(",")
            parm_id_list = range(len(input_field_list))
            r_dict_return ={}
            for p,n,d,i in zip(input_field_list,input_need_list,input_demo_list,parm_id_list):
                r_dict_return[i] = {"parm":p,"need":n,"demo":d,"num":i}



            html = 'interface_detail.html'
            return render(request,html,{"r":r,"r_dict_return":r_dict_return})
    except:
        return redirect("/")


def interface_depot(request):
    if request.method == "GET":
        html = "interface_depot.html"
    return render(request,html)
