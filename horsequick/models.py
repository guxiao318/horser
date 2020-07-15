from django.db import models

# Create your models here.
class User_Group_Info(models.Model):
    group_brief= models.CharField(max_length=50,verbose_name="组简介")

    class Meta:
        verbose_name = "用户组表"
        ordering = ['-id']



class User_Info(models.Model):
    user_name = models.CharField(max_length=30,verbose_name="用户名")
    user_role = models.CharField(max_length=20,verbose_name="用户角色")
    password = models.CharField(max_length=20,verbose_name="用户密码")

    class Meta:
        verbose_name = "用户表"
        ordering = ['-id']

class User_Group_Relation(models.Model):
    user = models.ForeignKey(User_Info,on_delete=models.CASCADE,verbose_name="用户id")
    group_belong = models.ForeignKey(User_Group_Info, on_delete=models.CASCADE,verbose_name="所属组id")

    class Meta:
        verbose_name = "用户与组关系表"
        ordering = ['-id']

class Interface_Info(models.Model):
    interface_name = models.CharField(max_length=20,verbose_name="接口名")
    interface_type = models.CharField(max_length=20,verbose_name="接口类型")
    interface_url = models.CharField(max_length=150,verbose_name="接口url")
    input_fileld_list = models.CharField(max_length=200,verbose_name="输入字段列表",null=True)
    input_need_list = models.CharField(max_length=200,verbose_name="输入字段必需列表",null=True)
    input_demo_list = models.CharField(max_length=200,verbose_name="输入字段实例列表",null=True)
    assert_filed_list = models.CharField(max_length=200,verbose_name="断言字段列表",null=True)
    match_list = models.CharField(max_length=200,verbose_name="匹配内容列表",null=True)
    assert_result_list = models.CharField(max_length=200,verbose_name="断言结果列表",null=True)
    belong_subsys = models.CharField(max_length=50,verbose_name="所属子系统")
    belong_group = models.CharField(max_length=50,verbose_name="所属分类",null=True)
    belong_git_base = models.CharField(max_length=100,verbose_name="所属git代码库",blank=True)
    belong_svn_base = models.CharField(max_length=100, verbose_name="所属svn代码库",blank=True)
    created_time = models.DateTimeField(verbose_name="创建时间")
    updated_time = models.DateTimeField(verbose_name="更新时间",null=True)


    class Meta:
        verbose_name = "接口信息表"
        ordering = ['-updated_time']