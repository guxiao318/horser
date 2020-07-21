from django.shortcuts import render,HttpResponse,redirect
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Interface_Info,Domain_Info,User_Info,User_Domain_Group_Relation
from django.forms import model_to_dict
from functools import wraps

# Create your views here.

def check_login(func):
    @wraps(func)
    def warpper(request,*args,**kwargs):

        login_status =request.session.get('login_status',False)

        if login_status:
            user_name = request.session.get('user_name',False)#从session中获取用户名
            user_id = User_Info.objects.get(user_name=user_name).id
            domain_name = request.session.get('domain_name',False)#从session中获取领域名
            domain_id = Domain_Info.objects.get(domain_name=domain_name).id


            domain_total = User_Domain_Group_Relation.objects.filter(user=user_id).values("belong_domain__domain_name")#用户属于的领域id

            domain_total_name_good =[]
            for i in domain_total:
                domain_total_name_good.append(i["belong_domain__domain_name"])

            show = {"user_name": user_name,"domain_total":domain_total_name_good,"domain_name":domain_name,"domain_id":domain_id}


            group_list = Interface_Info.objects.filter(belong_domain=domain_id).values("belong_group").distinct()  # 分类列表
            group_list_good = []
            back_dict = {}

            for i in group_list:
                group_list_good.append(i["belong_group"])  # 将分类转换为列表类型

            for i in group_list_good:
                interface_name_objects = Interface_Info.objects.filter(belong_group=i).values("interface_name", "id")
                interface_name_list = []
                for n in interface_name_objects:
                    interface_name_list.append(n)
                    back_dict[i] = interface_name_list  # 嵌套字典

            show["interface_info"] = back_dict

            return func(request, *args,**show)
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
                    request.session['domain_name']= "通用领域" #初始化默认通用领域
                    request.session['login_status'] = True
                else:
                    resp = {'code': '000002', 'msg': '登录失败，密码错误请重新输入！'}
            else:
                resp = {'code': '000003', 'msg': '登录失败，用户不存在请先注册！'}

    return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")




@check_login
def horser_index(request,**show):
    global interface_name_objects
    if request.method == "GET":


        html = "horser_index.html"
        back_dict = show["interface_info"]

        return render(request,html,{"show":show,"back_dict":back_dict})


@check_login
def horser_help(request,**show):
    if request.method == "GET":
        html = "horser_help.html"
        back_dict = show["interface_info"]


        return render(request,html,{'show':show,"back_dict":back_dict})

@check_login
def domain_manage(request,**show):
    if request.method == "GET":
        html = "domain_manage.html"

        back_dict = show["interface_info"]
        return render(request,html,{"show":show,"back_dict":back_dict})


@csrf_exempt
@check_login
def domain_add(request,**show):
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
                input_dict["belong_domain_id"] = show["domain_id"] #添加的归属领域默认为当前领域
                input_dict["created_person"] = show["user_name"] #添加的创建人为当前登录用户
                Interface_Info.objects.create(**input_dict)

                resp = {'code': '000000', 'msg': '添加成功'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")



    else:
        html = "interface_add.html"
        back_dict = show["interface_info"]

        return render(request, html, {'show': show, "back_dict": back_dict})

@check_login
def interface_detail(request,jiekouId,**show):

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
            back_dict = show["interface_info"]

            return render(request,html,{"r":r,"r_dict_return":r_dict_return,"show":show,"back_dict":back_dict})
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
        request.session['domain_name'] =domain_name #切换领域时，修改session的值
        resp={'code':'000000'}

        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json")

