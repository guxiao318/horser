import jenkins

#远程Jenkins的地址
jenkins_server_url = 'http://81.68.104.92:8080/'

#用户名
user_id = 'guxiao'

#用户的token值(每个user有对应的token----如本文第3.1节所示)
api_token = '114260a857d050c966763b187610759812'

#登录密码
#passwd = 'admin'

#server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=passwd)

#使用  API_Token    进行Jenkins登录操作
server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)

#使用get.version()方法获取版本号
version = server.get_version()

print(version)
#server.build_job('oschina_selenium_docker')