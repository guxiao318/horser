from datetime import datetime
from .models import Interface_Info

def update_interface_info(now_person,interface_id,**edit_dict):
    updated_time = datetime.now()
    edit_dict["updated_time"] = updated_time
    edit_dict["updated_person"] = now_person  # 更新人为当前登录用户
    to_update = Interface_Info.objects.filter(id=interface_id)
    to_update.update(**edit_dict)
    resp = {'code': '000000', 'msg': '基本信息更新成功'}
    return resp


class parms_change:

    def __init__(self,input_dict):
        self.input_dict = input_dict
        self.interface_id = self.input_dict["interface_id"]

        parms_name_str = Interface_Info.objects.get(id=self.interface_id).input_field_list
        parms_demo_str = Interface_Info.objects.get(id=self.interface_id).input_demo_list
        parms_need_str = Interface_Info.objects.get(id=self.interface_id).input_need_list

        self.parms_name_list = parms_name_str.split(",")  # 字符串转换为列表
        self.parms_demo_list = parms_demo_str.split(",")
        self.parms_need_list = parms_need_str.split(",")


    def parms_edit(self):

        parms_new_name = self.input_dict["parms_new_name"]
        parms_old_name = self.input_dict["parms_old_name"]
        parms_demo = self.input_dict["parms_demo"]
        parms_need = self.input_dict["parms_need"]
        n = self.parms_name_list.index(parms_old_name)  # 找到老参数名的下标


        if parms_new_name != parms_old_name:  # 参数名有变化
            if parms_new_name in self.parms_name_list:  # 新参数名是否在参数名列表中已存在
                resp = {'code': '000002', 'msg': '更新失败，已有同名参数！'}

            else:  # 不存在同名参数
                self.parms_name_list[n] = parms_new_name  # 更新参数名
                self.parms_demo_list[n] = parms_demo  # 更新demo
                self.parms_need_list[n] = parms_need  # 更新是否必需

                input_field_list = ",".join(self.parms_name_list)  # 列表转换为字符串
                input_need_list = ",".join(self.parms_need_list)
                input_demo_list = ",".join(self.parms_demo_list)

                to_update = Interface_Info.objects.filter(id=self.interface_id)
                to_update.update(input_field_list=input_field_list, input_need_list=input_need_list,
                                 input_demo_list=input_demo_list)
                resp = {'code': '000000', 'msg': '参数信息更新成功！'}

        else:  # 参数名没有变化
            if parms_need == self.parms_need_list[n] and parms_demo == self.parms_demo_list[n]:
                resp = {'code': '000003', 'msg': '更新失败，参数信息无变化！'}
            else:
                n = self.parms_name_list.index(parms_old_name)  # 找到老参数名的下标
                self.parms_demo_list[n] = parms_demo  # 更新demo
                self.parms_need_list[n] = parms_need  # 更新是否必需

                input_need_list = ",".join(self.parms_need_list)
                input_demo_list = ",".join(self.parms_demo_list)

                to_update = Interface_Info.objects.filter(id=self.interface_id)
                to_update.update(input_need_list=input_need_list, input_demo_list=input_demo_list)
                resp = {'code': '000000', 'msg': '参数信息更新成功！'}

        return resp

    def parms_delete(self):

        parms_name = self.input_dict["parms_name"]
        n = self.parms_name_list.index(parms_name)  # 找到参数名的下标

        self.parms_name_list.pop(n)  # 删除参数名
        self.parms_demo_list.pop(n)  # 删除demo
        self.parms_need_list.pop(n)  # 删除是否必需

        input_field_list = ",".join(self.parms_name_list)  # 列表转换为字符串
        input_need_list = ",".join(self.parms_need_list)
        input_demo_list = ",".join(self.parms_demo_list)

        to_update = Interface_Info.objects.filter(id=self.interface_id)
        to_update.update(input_field_list=input_field_list, input_need_list=input_need_list,
                         input_demo_list=input_demo_list)

        resp = {'code': '000000', 'msg': '参数删除成功！'}
        return resp


    def parms_add(self):
        parms_name = self.input_dict["parms_name"]
        parms_demo = self.input_dict["parms_demo"]
        parms_need = self.input_dict["parms_need"]

        if parms_name in self.parms_name_list:
            resp = {'code': '000002', 'msg': '添加失败，已有同名参数！'}
        else:
            self.parms_name_list.append(parms_name)  # 添加参数名
            self.parms_demo_list.append(parms_demo)  # 添加demo
            self.parms_need_list.append(parms_need)  # 添加是否必需

            input_field_list = ",".join(self.parms_name_list)  # 列表转换为字符串
            input_need_list = ",".join(self.parms_need_list)
            input_demo_list = ",".join(self.parms_demo_list)

            to_add = Interface_Info.objects.filter(id=self.interface_id)
            to_add.update(input_field_list=input_field_list, input_need_list=input_need_list,
                             input_demo_list=input_demo_list)

            resp = {'code': '000000', 'msg': '参数添加成功！'}

        return resp
