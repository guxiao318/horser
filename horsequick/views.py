from django.shortcuts import render,HttpResponse,redirect
import json,requests
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Interface_Info,Domain_Info,User_Info,User_Domain_Group_Relation,Category_Info,Sub_Sys_Info
from django.forms import model_to_dict
from functools import wraps
from collections import ChainMap
from . import public_good


# Create your views here.

def check_login(func): #检查登录状态及和登录相关的初始化装饰器

        @wraps(func)
        def warpper(request,*args,**kwargs):

            login_status =request.session.get('login_status',False)
            interface_nums = 0
            if login_status:
                user_name = request.session.get('user_name',False)#从session中获取用户名
                user_id = User_Info.objects.get(user_name=user_name).id
                domain_id = request.session.get('domain_id',False)#从session中获取领域id
                domain_name = Domain_Info.objects.get(id=domain_id).domain_name

                domain_total = User_Domain_Group_Relation.objects.filter(user_id=user_id).values("belong_domain__domain_name")#用户属于的领域id
                domain_total_name_good =[]
                for i in domain_total:
                    domain_total_name_good.append(i["belong_domain__domain_name"])

                show = {"user_name": user_name,"domain_total":domain_total_name_good,"domain_name":domain_name,"domain_id":domain_id}


                category_list = Interface_Info.objects.filter(belong_domain_id=domain_id).values("belong_category__category_name").order_by("belong_category__category_name").distinct()  # 领域对于下的分类名列表
                category_list_good = []
                interface_total_dict = {} #领域下的接口字典

                for i in category_list:
                    category_list_good.append(i["belong_category__category_name"])  # 将分类转换为列表类型


                for i in category_list_good:
                    interface_info_objects = Interface_Info.objects.filter(belong_category__category_name=i,belong_domain_id= domain_id).values("interface_name", "id")
                    interface_num_category = len(interface_info_objects) #类别下的接口数量
                    interface_info_list = []

                    for n in interface_info_objects:
                        interface_info_list.append(n)
                        interface_total_dict[i] = interface_info_list  # 嵌套字典

                    interface_nums = interface_nums +interface_num_category

                sub_sys_list =[]
                sub_sys_with_domain = Sub_Sys_Info.objects.filter(belong_domain_id=domain_id).values("sub_sys_name")
                for i in sub_sys_with_domain:
                    sub_sys_list.append(i["sub_sys_name"])  # 将分类转换为列表类型


                show["interface_nums"] = interface_nums  # 该领域下接口数量
                show["interface_info"] = interface_total_dict #该领域下的接口信息
                show["category_list"] = category_list_good
                show["sub_sys_list"] = sub_sys_list
                return func(request, *args, **show)

            else:
                return redirect("/login/")
        return warpper





@csrf_exempt
def horser_login(request):
    if request.method == "GET":
        html = "login.html"
        return render(request,html)

    else:
        receive_data = json.loads(request.body.decode())  # 将body从byte类型转码后用json的loads函数将json格式转为字典
        user_name = receive_data['user_name']
        password = receive_data['password']

        try:
            if user_name.strip() == "" or password.strip()=="":
                raise Exception
        except Exception:
            resp = {'code':'000001','msg':'登录失败，用户名或密码不能为空！'}
        else:
            if User_Info.objects.filter(user_name=user_name).exists():
                if password == User_Info.objects.get(user_name=user_name).password:
                    resp = {'code': '000000', 'msg': '登录成功！'}
                    request.session['user_name'] =user_name
                    request.session['domain_id']= 1 #初始化默认通用领域
                    request.session['login_status'] = True
                else:
                    resp = {'code': '000002', 'msg': '登录失败，密码错误请重新输入！'}
            else:
                resp = {'code': '000003', 'msg': '登录失败，用户不存在请先注册！'}

    return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")




@check_login
def horser_index(request,**show):

    if request.method == "GET":


        html = "horser_index.html"
        interface_info_with_domain = show["interface_info"]

        return render(request,html,{"show":show,"interface_info_with_domain":interface_info_with_domain})


@check_login
def interface_webtest(request,**show):

    if request.method == "GET":
            html = 'interface_webtest.html'
            interface_info_with_domain = show["interface_info"]

            return render(request, html,{"show": show,"interface_info_with_domain":interface_info_with_domain})



@check_login
def interface_webtest_detail(request,jiekouId,**show):

    if request.method == "GET":

        try:
            r = Interface_Info.objects.get(id=jiekouId)

            if r != None:
                r_dict = model_to_dict(r)
                input_field_list = r_dict["input_field_list"].split(",")
                input_need_list = r_dict["input_need_list"].split(",")
                input_demo_list = r_dict["input_demo_list"].split(",")
                parm_id_list = range(len(input_field_list))
                r_dict_return = {}
                interface_name_dict ={}
                for p, n, d, i in zip(input_field_list, input_need_list, input_demo_list, parm_id_list):
                    r_dict_return[i] = {"parm": p, "need": n, "demo": d, "num": i}

                html = 'interface_webtest_detail.html'
                interface_info_with_domain = show["interface_info"]
                interface_name_dict["interface_name"] = r.interface_name

                return render(request, html,
                              {"r_dict_return": r_dict_return, "show": show, "interface_info_with_domain": interface_info_with_domain,"interface_name_dict":interface_name_dict})
        except:
            return redirect("/")


@check_login
def horser_help(request,**show):
    if request.method == "GET":
        html = "horser_help.html"
        interface_info_with_domain = show["interface_info"]


        return render(request,html,{'show':show,"interface_info_with_domain":interface_info_with_domain})

@check_login
def domain_manage(request,**show):
    if request.method == "GET":
        html = "domain_manage.html"

        interface_info_with_domain = show["interface_info"]
        domain_info = Domain_Info.objects.get(id=show["domain_id"])
        category_info = Category_Info.objects.filter(belong_domain=show["domain_id"])
        subsys_info = Sub_Sys_Info.objects.filter(belong_domain=show["domain_id"])

        return render(request,html,{"show":show,"interface_info_with_domain":interface_info_with_domain,"domain_info":domain_info,"category_info":category_info,"subsys_info":subsys_info})


@csrf_exempt
def domain_add(request):
    global resp
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
@check_login
def subsys_add(request,**show):
    global resp
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典
        sub_sys_name = receive_data['sub_sys_name']
        svn_address = receive_data['svn_address']
        git_address = receive_data['git_address']

        try:
            if sub_sys_name.strip() =="":
                raise Exception
        except Exception:
            resp = {'code':'000001','msg':'必填项不能为空'}
        else:
            if Sub_Sys_Info.objects.filter(sub_sys_name=sub_sys_name).exists():
                resp = {'code': '000002', 'msg': '添加失败，该领域下已存在此子系统！'}
            else:
                Sub_Sys_Info.objects.create(sub_sys_name=sub_sys_name,svn_address=svn_address,git_address=git_address,belong_domain_id=show["domain_id"])
                resp = {'code': '000000', 'msg': '添加成功'}

    return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



@csrf_exempt
@check_login
def category_add(request,**show):
    global resp
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典
        category_name = receive_data['category_name']

        try:
            if category_name.strip() =="":
                raise Exception
        except Exception:
            resp = {'code':'000001','msg':'必填项不能为空'}
        else:
            if Category_Info.objects.filter(category_name=category_name,belong_domain_id=show["domain_id"]).exists():
                resp = {'code': '000002', 'msg': '添加失败，该领域下已存在此类别！'}
            else:
                Category_Info.objects.create(category_name=category_name,belong_domain_id=show["domain_id"])
                resp = {'code': '000000', 'msg': '添加成功'}

    return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



@check_login
@csrf_exempt
def interface_add(request,**show):
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
        belong_category = receive_data['belong_category']


        input_list_need = [interface_name,interface_type,interface_url,belong_subsys] #必填项列表
        input_field_list = ",".join(input_field_list)#列表转换为字符串
        input_need_list = ",".join(input_need_list)
        input_demo_list = ",".join(input_demo_list)


        if belong_subsys ==None:#先检验有没有子系统
            resp = {'code': '000003', 'msg': '该领域下尚未添加子系统，请先在领域管理中添加子系统'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


        else:#子系统有数据
            belong_subsys_id = Sub_Sys_Info.objects.get(sub_sys_name=belong_subsys).id #获取子系统id
            input_dict = {"interface_name": interface_name, "interface_type": interface_type,
                          "input_field_list": input_field_list,
                          "input_need_list": input_need_list, "input_demo_list": input_demo_list,
                          "interface_url": interface_url, "belong_subsys_id": belong_subsys_id,
                          "interface_mock": interface_mock}


            try:#检验必填项是否都填了
                for i in input_list_need:
                    if i.strip() == '':
                        raise Exception

            except Exception:
                resp = {'code':'000001','msg':'必填项不能为空'}

            else:#必填项都填了

                if Interface_Info.objects.filter(interface_name=interface_name,belong_subsys_id=belong_subsys_id).exists():#检查接口是否已存在
                    resp = {'code': '000002', 'msg': '添加失败，该子系统下接口已存在'}

                else:#子系统下接口不存在则添加
                    created_time = datetime.now()
                    input_dict["created_time"] = created_time
                    input_dict["belong_domain_id"] = show["domain_id"] #添加的归属领域默认为当前领域
                    input_dict["created_person"] = show["user_name"] #添加的创建人为当前登录用户
                    if belong_category == "":
                        input_dict["belong_category_id"] = None
                    else:
                        input_dict["belong_category_id"] = Category_Info.objects.get(category_name=belong_category).id

                    Interface_Info.objects.create(**input_dict)
                    resp = {'code': '000000', 'msg': '添加成功'}

            return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



    else:
        html = "interface_add.html"

        interface_info_with_domain = show["interface_info"]
        sub_sys_list = show["sub_sys_list"]
        category_info = Category_Info.objects.filter(belong_domain=show["domain_id"])
        #该领域下的接口分类

        return render(request, html, {'show': show, "interface_info_with_domain": interface_info_with_domain,"sub_sys_list":sub_sys_list,"category_info":category_info})


@check_login

def interface_detail(request,jiekouId,**show):

    try:
        interface_objects = Interface_Info.objects.get(id=jiekouId)

        if interface_objects !=None:
            interface_info_now = model_to_dict(interface_objects) #当前的接口
            input_field_list = interface_info_now["input_field_list"].split(",")
            input_need_list= interface_info_now["input_need_list"].split(",")
            input_demo_list = interface_info_now["input_demo_list"].split(",")
            parm_id_list = range(len(input_field_list))
            interface_info_now_dict ={}
            for p,n,d,i in zip(input_field_list,input_need_list,input_demo_list,parm_id_list):
                interface_info_now_dict[i] = {"parm":p,"need":n,"demo":d,"num":i}

            html = 'interface_detail.html'

            interface_info_with_domain = show["interface_info"]
            category_and_subsys ={}
            category_id = interface_objects.belong_category_id
            subsys_id = interface_objects.belong_subsys_id

            if category_id ==None and subsys_id ==None:
                belong_category ="未分类"
                belong_subsys = "暂未绑定"
            elif category_id ==None and subsys_id !=None:
                belong_category = "未分类"
                belong_subsys = Sub_Sys_Info.objects.get(id=interface_objects.belong_subsys_id).sub_sys_name
            elif category_id != None and subsys_id == None:
                belong_subsys = "暂未绑定"
                belong_category = Category_Info.objects.get(id=interface_objects.belong_category_id).category_name
            else:
                belong_category = Category_Info.objects.get(id=interface_objects.belong_category_id).category_name

                belong_subsys = Sub_Sys_Info.objects.get(id=interface_objects.belong_subsys_id).sub_sys_name

            category_and_subsys["belong_category"] =belong_category
            category_and_subsys["belong_subsys"] = belong_subsys

            category_info = Category_Info.objects.filter(belong_domain=show["domain_id"])

            return render(request,html,{"interface_objects":interface_objects,"interface_info_now_dict":interface_info_now_dict,"show":show,"interface_info_with_domain":interface_info_with_domain,"category_and_subsys":category_and_subsys,"category_info":category_info})
    except:
        return redirect("/")



@check_login
def interface_depot(request):
    if request.method == "GET":
        html = "interface_depot.html"
    return render(request,html)



@csrf_exempt
def select_domain(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        domain_name = receive_data['domain_name']
        domain_id = Domain_Info.objects.get(domain_name=domain_name).id
        request.session['domain_id'] =domain_id #切换领域时，修改session的领域ID值
        resp={'code':'000000'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")


@check_login
@csrf_exempt
def edit_domain(request,**show):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        domain_name = receive_data['domain_name']
        domain_brief = receive_data['domain_brief']

        try:
            if Domain_Info.objects.filter(domain_name = domain_name,domain_brief=domain_brief).exists():
                raise Exception
        except Exception:

            resp={'code':'000001','msg':'修改失败，领域名已存在或信息无变动！'}
        else:
            to_update = Domain_Info.objects.filter(id = show["domain_id"])
            to_update.update(domain_name=domain_name,domain_brief=domain_brief)
            resp = {'code': '000000', 'msg': '领域信息修改成功！'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def edit_subsys(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        sub_sys_id = receive_data['sub_sys_id']
        sub_sys_name = receive_data['sub_sys_name_edit']
        svn_address = receive_data['svn_address_edit']
        git_address = receive_data['git_address_edit']

        try:
            if Sub_Sys_Info.objects.filter(sub_sys_name = sub_sys_name,svn_address=svn_address,git_address=git_address).exists():
                raise Exception
        except Exception:

            resp={'code':'000001','msg':'修改失败，子系统已存在或信息无变动！'}
        else:
            to_update = Sub_Sys_Info.objects.filter(id = sub_sys_id)
            to_update.update(sub_sys_name=sub_sys_name,svn_address=svn_address,git_address=git_address)
            resp = {'code': '000000', 'msg': '子系统信息修改成功！'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def edit_category(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        category_id = receive_data['category_id']
        category_name_edit = receive_data['category_name_edit']

        try:
            if Category_Info.objects.filter(id= category_id,category_name=category_name_edit).exists():
                raise Exception
        except Exception:

            resp={'code':'000001','msg':'修改失败，类别信息无变动！'}
        else:
            to_update = Category_Info.objects.filter(id = category_id)
            to_update.update(category_name =category_name_edit)
            resp = {'code': '000000', 'msg': '领域信息修改成功！'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")




@csrf_exempt
def delete_category(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        category_id = receive_data['category_id']
        Category_Info.objects.filter(id = category_id).delete()

        resp = {'code': '000000', 'msg': '该类别已删除，类别下的接口转移到未分类！'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def delete_subsys(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        sub_sys_id = receive_data['sub_sys_id']
        Sub_Sys_Info.objects.filter(id = sub_sys_id).delete()

        resp = {'code': '000000', 'msg': '该子系统已删除!'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def webtest_go(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        input_field_value_list = receive_data['input_field_value_list']
        interface_name_now = receive_data['interface_name_now'] #当前接口名
        protocol_type = receive_data['protocol_type']  # 协议类型

        interface_objects = Interface_Info.objects.get(interface_name=interface_name_now)
        interface_type = interface_objects.interface_type#请求类型
        interface_url = interface_objects.interface_url
        input_need_list =interface_objects.input_need_list.split(",")#当前接口的入参必需列表
        input_filed_list = interface_objects.input_field_list.split(",")
        req_url = protocol_type+"://"+interface_url

        try:
            for v,need in zip(input_field_value_list,input_need_list):
                if v=="" and need =="必需":
                    raise Exception
        except  Exception:
            resp = {'code': '000001', 'msg': '请求失败，必填项不能为空！'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

        else:#所有必填项都填了
            input_filed_num = len(input_filed_list)
            parms_value_dict_zip ={}
            parms_value_dict = {}
            for parm, value,i in zip(input_filed_list, input_field_value_list,range(input_filed_num)):
                parms_value_dict_zip[i] = {parm:value}


            for k,parms_input in parms_value_dict_zip.items():
                parms_value_dict =ChainMap(parms_value_dict,parms_input)

            if interface_type =="GET":

                r = requests.get(req_url,params=parms_value_dict)
                r_json = r.json()
                testresult = json.dumps(r_json,ensure_ascii=False,indent=4)
                resp = {'code': '000000','msg': '请求成功',"testresult":testresult}
                return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")

            elif interface_type =="POST":
                r = requests.post(req_url, data=parms_value_dict)
                r_json = r.json()
                testresult = json.dumps(r_json, ensure_ascii=False, indent=4)
                resp = {'code': '000000', 'msg': '请求成功', "testresult": testresult}
                return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


@csrf_exempt
@check_login
def interface_edit(request,**show):

    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典

        interface_id = receive_data['interface_id']
        interface_new_name = receive_data['interface_new_name']
        interface_old_name = receive_data['interface_old_name']
        interface_type = receive_data['interface_type']
        interface_url = receive_data['interface_url']
        interface_mock = receive_data['interface_mock']
        belong_subsys = receive_data['interface_subsys']
        belong_category = receive_data['interface_category']

        input_list_need = [interface_new_name,interface_type,interface_url,interface_old_name] #必填项列表

        try:#检验必填项是否都填了
            for i in input_list_need:
                if i.strip() == '':
                    raise Exception

        except Exception:
            resp = {'code':'000001','msg':'必填项不能为空'}

        else:#必填项都填了

            if belong_subsys =="暂未绑定" and belong_category =="未分类":
                belong_subsys_id =None
                belong_category_id =None
            elif belong_subsys =="暂未绑定" and belong_category !="未分类":
                belong_subsys_id = None
                belong_category_id = Category_Info.objects.get(category_name=belong_category,belong_domain_id=show["domain_id"]).id  # 获取分类id
            elif belong_subsys != "暂未绑定" and belong_category == "未分类":
                belong_subsys_id = Sub_Sys_Info.objects.get(sub_sys_name=belong_subsys).id  # 获取子系统id
                belong_category_id = None
            else:
                belong_subsys_id = Sub_Sys_Info.objects.get(sub_sys_name=belong_subsys).id #获取子系统id
                belong_category_id = Category_Info.objects.get(category_name=belong_category,belong_domain_id=show["domain_id"]).id #获取分类id

            edit_dict = {"interface_name": interface_new_name, "interface_type": interface_type,
                              "interface_url": interface_url, "belong_subsys_id": belong_subsys_id,
                              "interface_mock": interface_mock,"belong_category_id":belong_category_id}


            if Interface_Info.objects.filter(**edit_dict).exists():#检查接口是否无变化
                resp = {'code': '000002', 'msg': '修改失败，基本信息无变化！'}

            else:#有变化
                if interface_new_name != interface_old_name: #接口名有变化
                    compare_dict = {"interface_name": interface_new_name,"belong_subsys_id": belong_subsys_id}
                    if Interface_Info.objects.filter(**compare_dict).exists():#子系统和接口名联合主键检查是否该接口名已存在，不同子系统下允许有同名接口
                        resp = {'code': '000003', 'msg': '修改失败，本领域下此子系统已有同名接口！'}
                    else:
                        resp = public_good.update_interface_info(now_person=show["user_name"],interface_id=interface_id,**edit_dict)#调用公共方法

                else:#接口名没有变化则进行其他项内容的更新
                    resp =public_good.update_interface_info(now_person=show["user_name"], interface_id=interface_id,**edit_dict)

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def parms_edit(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典
        interface_id = receive_data['interface_id']
        parms_new_name = receive_data['parms_new_name']
        parms_old_name = receive_data['parms_old_name']
        parms_need = receive_data['parms_need']
        parms_demo = receive_data['parms_demo']


        input_list_need = [interface_id,parms_new_name,parms_old_name] #必填项列表

        try:#检验必填项是否都填了
            for i in input_list_need:
                if i.strip() == '':
                    raise Exception

        except Exception:
            resp = {'code':'000001','msg':'必填项不能为空'}

        else:#必填项都填了
            edit_parms_dict ={"interface_id":interface_id,"parms_new_name":parms_new_name,
                              "parms_old_name":parms_old_name,"parms_need":parms_need,"parms_demo":parms_demo}

            to_edit = public_good.parms_change(edit_parms_dict)
            resp = to_edit.parms_edit()


        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


@csrf_exempt
def parms_delete(request):
    if request.method == "POST":
        receive_data = json.loads(request.body.decode())#将body从byte类型转码后用json的loads函数将json格式转为字典
        interface_id = receive_data['interface_id']
        parms_name = receive_data['parms_name']

        delete_parms_dict = {"interface_id": interface_id, "parms_name": parms_name}
        to_delete = public_good.parms_change(delete_parms_dict)#调用公共类删除方法
        resp = to_delete.parms_delete()

        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")



@csrf_exempt
def parms_add(request):

    receive_data = json.loads(request.body.decode())  # 将body从byte类型转码后用json的loads函数将json格式转为字典
    interface_id = receive_data['interface_id']
    parms_name = receive_data['parms_name']
    parms_demo = receive_data['parms_demo']
    parms_need = receive_data['parms_need']

    if parms_name =="":
        resp = {'code': '000001', 'msg': '必填项不能为空'}
    else:
        add_parms_dict = {"interface_id":interface_id,"parms_name":parms_name,"parms_demo":parms_demo,"parms_need":parms_need}
        to_add = public_good.parms_change(add_parms_dict)#调用公共类添加方法
        resp = to_add.parms_add()

    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")