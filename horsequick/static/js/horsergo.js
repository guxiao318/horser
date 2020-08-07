$.ajaxSetup({
    data:{csrfmiddlewaretoken:'{{csrf_token}}'}

});


    function interface_add() {
    	var input_field_list = new Array() //入参数组
		var input_need_list = new Array() //入参是否必需数组
		var input_demo_list = new Array() //入场实例数组

    	$(".params_input").each(function () {
        	input_field_list.push($(this).val())
		})

		$(".params_need").each(function () {
        	input_need_list.push($(this).val())
		})

		$(".params_demo").each(function () {
        	input_demo_list.push($(this).val())
		})

        var interface_name = $("#interface_name").val()
        var interface_type = $("#interface_type").val()
        var interface_url = $("#interface_url").val()
		var interface_mock = $("#interface_mock").val()
		var belong_subsys = $("#belong_subsys").val()
		var belong_category = $("#belong_category").val()
        var belong_git_base = $("#belong_git_base").val()
        var belong_svn_base = $("#belong_svn_base").val()


        console.log('---------------add interface----------------')
		
		$.ajax({
			
			type:"post",
			url:"/interface_add/",
			data:JSON.stringify({"interface_name":interface_name,"interface_type":interface_type,"input_field_list":input_field_list,
			"input_need_list":input_need_list,"input_demo_list":input_demo_list,"interface_url":interface_url,"belong_category":belong_category,
			"belong_subsys":belong_subsys,"belong_git_base":belong_git_base,"belong_svn_base":belong_svn_base,"interface_mock":interface_mock}),
			cache:false,
			async:false,
			dataType:"json",
			
			success:function(resp){
				if(resp.code ==="000000"){
					alert(resp.msg);
					window.location.reload()
				}
				
				else if(resp.code==="000001"){
					alert(resp.msg);
				}

				else if(resp.code==="000002"){
					alert(resp.msg);

				}
				else{
					alert(resp.msg);
				}

			},
			
			error: function(){
				
				alert("出错了");
				window.location.reload()
			}
		});	

    }


    function webtest_go() {
		var input_field_value_list = new Array() //入参数组

		var interface_name_now = $("#interface_name_now").text() //当前接口名
		var protocol_type = $("#protocol_type").val() //协议类型

		$(".params_input").each(function () {
			input_field_value_list.push($(this).val())
		})

		$.ajax({

			type: "post",
			url: "/webtest_go/",
			data: JSON.stringify({"input_field_value_list": input_field_value_list,"interface_name_now":interface_name_now,
			"protocol_type":protocol_type}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					$("#testresult").val(resp.testresult)
				} else if (resp.code === "000001") {
					alert(resp.msg);
				} else {
					alert(resp.msg);
				}

			},

			error: function () {

				alert("出错了");
			}


		});
	}




    function domain_add() {
		var domain_name = $("#domain_name").val()
		var domain_brief = $("#domain_brief").val()

		$.ajax({

			type: "post",
			url: "/domain_add/",
			data: JSON.stringify({"domain_name": domain_name, "domain_brief": domain_brief}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
				} else if (resp.code === "000001") {
					alert(resp.msg);
				} else {
					alert(resp.msg);
				}

			},

			error: function () {

				alert("出错了");
			}


		});
	}

	function category_add() {
		var category_name = $("#category_name").val()


		$.ajax({

			type: "post",
			url: "/category_add/",
			data: JSON.stringify({"category_name": category_name}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
				} else if (resp.code === "000001") {
					alert(resp.msg);
				} else {
					alert(resp.msg);
				}

			},

			error: function () {

				alert("出错了");
			}


		});
	}


	function subsys_add() {
		var sub_sys_name = $("#sub_sys_name").val()
		var svn_address = $("#svn_address").val()
		var git_address = $("#git_address").val()


		$.ajax({

			type: "post",
			url: "/subsys_add/",
			data: JSON.stringify({"sub_sys_name": sub_sys_name,"svn_address": svn_address,"git_address": git_address}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
				} else if (resp.code === "000001") {
					alert(resp.msg);
				} else {
					alert(resp.msg);
				}

			},

			error: function () {

				alert("出错了");
			}


		});
	}


	function horser_login() {
		var user_name = $("#user_name").val()
		var password = $("#password").val()

		$.ajax({

			type: "post",
			url: "/login/",
			data: JSON.stringify({"user_name": user_name, "password": password}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
					window.location.href = "/"
				} else if (resp.code === "000001") {
					alert(resp.msg);
				}
				else if (resp.code === "000002") {
					alert(resp.msg);
				}
				else {
					alert(resp.msg);
				}

			},

			error: function () {

				alert("出错了");
			}


		});
	}

    function add_input_field(obj) {



    	html = '<div class="form-inline">' +
			' <input id="input_field" name="interface_name" placeholder="参数名称" class="form-control params_input">' +
			'<select id="interface_name" name="interface_name"  class="form-control params_need"><option>必需</option><option>非必需</option></select>' +
			'<textarea class="form-control params_demo" style="height:34px;width: 55%" placeholder="参数实例"></textarea>' +'&nbsp;'+'<button class="btn btn-warning btn-sm" onclick="delete_input_fields(this)" >删除</button>'+


			'</div>'

		$("#input_field_set").append(html)


	}


	function select_domain(obj) {

		var domain_name = $(obj).text();

		$.ajax({
			type: "post",
			url: "/select_domain/",
			data: JSON.stringify({"domain_name": domain_name}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					window.location.href = "/"
				}
			},
			error: function () {
				alert("出错了");
			}
		});

	}


function edit_subsys(obj) {

		var tr = $(obj).parent().parent()
		var sub_sys_id = tr.children("td#sub_sys_id").text()
		var sub_sys_name_edit = tr.children("td#sub_sys_name_edit").find("input").val()
		var svn_address_edit = tr.children("td#svn_address_edit").find("input").val()
		var git_address_edit = tr.children("td#git_address_edit").find("input").val()


		$.ajax({
			type: "post",
			url: "/edit_subsys/",
			data: JSON.stringify({"sub_sys_id":sub_sys_id,"sub_sys_name_edit": sub_sys_name_edit,"svn_address_edit":svn_address_edit,"git_address_edit":git_address_edit}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
					window.location.reload()
				} else if (resp.code === "000001") {
					alert(resp.msg);
				}


			},
			error: function () {
				alert("出错了");
			}
		});

}








function edit_category(obj) {

    	var tr = $(obj).parent().parent()
		var category_id = tr.children("td#category_id").text()
		var category_name_edit = tr.children("td#category_name_edit").find("input").val()

		$.ajax({
			type: "post",
			url: "/edit_category/",
			data: JSON.stringify({"category_id": category_id,"category_name_edit":category_name_edit}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
					window.location.reload()
				} else if (resp.code === "000001") {
					alert(resp.msg);
				}

			},
			error: function () {
				alert("出错了");
			}
		});

}


function delete_category(obj) {

    	var tr = $(obj).parent().parent()




}


function delete_subsys(obj) {

    	var tr = $(obj).parent().parent()
		var sub_sys_id = tr.children("td#sub_sys_id").text()


		$.ajax({
			type: "post",
			url: "/delete_subsys/",
			data: JSON.stringify({"sub_sys_id": sub_sys_id}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
					window.location.reload()
				} else if (resp.code === "000001") {
					alert(resp.msg);
				}

			},
			error: function () {
				alert("出错了");
			}
		});

}



function delete_input_fields(obj) {

    	$(obj).parent().remove()


}


function interface_edit_show() {



    	var interface_name = $("#interface_name").text(); //取值
		var interface_url = $("#interface_url").text();
		var interface_type = $("#interface_type").text();
		var interface_subsys = $("#interface_subsys").text();
		var interface_category = $("#interface_category").text();
		var interface_mock = $("#interface_mock").attr("href");

		$("#interface_name_edit").val(interface_name);//赋值
		$("#interface_url_edit").val(interface_url);
		$("#interface_mock_edit").val(interface_mock);
		$("#interface_type_edit").val(interface_type);
		$("#interface_subsys_edit").val(interface_subsys);
		$("#interface_category_edit").val(interface_category);




    	$("#modal_interface_basic").modal("show")


}


function parms_edit_show(obj) {

    	$("#modal_interface_parms").modal("show")


}


function parms_delete_show(obj) {

    	$("#modal_interface_delete_parms").modal("show")


}


function parms_add_show() {

    	$("#modal_interface_add_parms").modal("show")


}



function interface_edit() {

		var interface_id = $("#interface_id").text()
    	var interface_name = $("#interface_name_edit").val()
		var interface_url = $("#interface_url_edit").val()
		var interface_mock = $("#interface_mock_edit").val()
		var interface_type = $("#interface_type_edit").val()
		var interface_subsys = $("#interface_subsys_edit").val()
		var interface_category = $("#interface_category_edit").val()


		$.ajax({
			type: "post",
			url: "/interface_edit/",
			data: JSON.stringify({"interface_name": interface_name,"interface_url": interface_url,
				"interface_mock": interface_mock,"interface_type":interface_type,
				"interface_subsys":interface_subsys,"interface_category":interface_category,"interface_id":interface_id}),
			cache: false,
			async: false,
			dataType: "json",
			success: function (resp) {
				if (resp.code === "000000") {
					alert(resp.msg);
					window.location.reload()
				} else if (resp.code === "000001") {
					alert(resp.msg);
				}else if (resp.code === "000002") {
					alert(resp.msg);
				}

			},
			error: function () {
				alert("出错了");
			}
		});

}