from django.shortcuts import render,HttpResponse
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Interface_Info
# Create your views here.

def horser_index(request):
    if request.method == "GET":
        html = "horser_index.html"

        return render(request,html)


def horser_help(request):
    if request.method == "GET":
        html = "horser_help.html"

        return render(request,html)



@csrf_exempt
def interface_add(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        interface_name = receive_data['interface_name']
        interface_type = receive_data['interface_type']
        interface_url = receive_data['interface_url']
        input_fileld_list = receive_data['input_fileld_list']
        input_need_list = receive_data['input_need_list']
        input_demo_list = receive_data['input_demo_list']
        belong_subsys = receive_data['belong_subsys']
        belong_group = receive_data['belong_group']
        belong_git_base = receive_data['belong_git_base']
        belong_svn_base = receive_data['belong_svn_base']

        input_list = [interface_name,interface_type,interface_url,belong_subsys]

        input_dict = {"interface_name":interface_name,"interface_type":interface_type,"input_fileld_list":input_fileld_list,
                      "input_need_list":input_need_list,"input_demo_list":input_demo_list,"interface_url":interface_url,"belong_group":belong_group,"belong_subsys":belong_subsys,"belong_git_base":belong_git_base,
                      "belong_svn_base":belong_svn_base}

        try:
            for i in input_list:
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