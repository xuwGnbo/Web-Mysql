/*增加一条管理员信息*/
function AddManager() {
    var a=$('#addAccount').val();
    var p=$('#addPassword').val();
    if(a==""||p==""){
        alert("管理员信息不能为空！");
    }
    else {
        var req1 = new RegExp(/^(ord[0-9]{5})$/); //检测管理员用户名的正则表达式
        var req2 = new RegExp(/^[0-9]*[a-zA-Z]+[0-9]+[A-Za-z]*$/); //检测管理员登录密码的正则表达式
        if (req1.test(a)){
            if(req2.test(p)&&p.length>=6){
                $.ajax({
                    url: '/create_manager',
                    data: {
                        Account: a,
                        Password: p
                    },
                    type: 'POST',
                    success: function (res) {
                        $('#addMagDlg').modal('hide');
                        var result = JSON.parse(res);
                        if(result.status =='OK'){
                            GetManagers();
                        }
                        else{
                            alert(result.status);
                        }
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            }
            else{
                alert('密码强度不够！');
            }
        }
        else{
            alert('账户名不符合要求！');
        }
    }
}

/*确认删除框*/
function ConfirmDeleteMag(elem) {
    localStorage.setItem('deleteId', $(elem).attr('mag-id'));
    $('#deleteMagDlg').modal();
}

/*删除该管理员*/
function DeleteMag() {
    $.ajax({
        url: '/delete_manager',
        data: {Id: localStorage.getItem('deleteId')},
        type: 'POST',
        success: function(res) {
            $('#deleteMagDlg').modal('hide');
            var result = JSON.parse(res);
            if(result.status=='OK'){
                GetManagers();
            }
            else{
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}


 /*获得管理员信息*/
function GetManagerInfo(){
    $.ajax({
        url: '/get_manager_byid',
        type: 'GET',
        success: function (res) {
            var magObj = JSON.parse(res);
            $('#MAccount').html( "<label>账号:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</label>"+magObj[0]['Account']);
            $('#MLevel').html("<label>权限:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</label>"+magObj[0]['Level']);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

/*匿名函数获得所有管理员信息*/
$(function () {
    GetManagers();
    GetManagerInfo();
})

/*获得所有的管理员信息*/
function GetManagers() {
    $.ajax({
        url: '/get_all_manager',
        type: 'GET',
        success: function (res) {
            var managerObj = JSON.parse(res);
            $('#list_manager').empty();
            $('#list_Manager_Temp').tmpl(managerObj).appendTo('#list_manager');
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function check_user_info() {     // 检查用户信息的有效性
    var a=$('#inputAccount').val();
    var p=$('#inputPassword').val();
    if(a==""||p==""){
        alert("管理员信息不能为空！");
        return false;
    }
    else {
        var req1 = new RegExp(/^(ord[0-9]{5})$/); //检测管理员用户名的正则表达式
        var req2 = new RegExp(/^[0-9]*[a-zA-Z]+[0-9]+[A-Za-z]*$/); //检测管理员登录密码的正则表达式
        if (req1.test(a)){
            if(req2.test(p)&&p.length>=6){
                return true;
            }
            else{
                alert('密码强度不够！');
                return false;
            }
        }
        else{
            alert('账户名不符合要求！');
            return false;
        }
    }
}


$(function () {     //点击注册按钮
    $('#btn_SignIn').click(function () {
        var a=$('#inputAccount').val();
        var p=$('#inputPassword').val();
        if(a==""||p==""){
            alert("管理员信息不能为空！");
        }
        else {
            var req1 = new RegExp(/^(ord[0-9]{5})$/); //检测管理员用户名的正则表达式
            var req2 = new RegExp(/^[0-9]*[a-zA-Z]+[0-9]+[A-Za-z]*$/); //检测管理员登录密码的正则表达式
            if (req1.test(a)){
                if(req2.test(p)&&p.length>=6){
                    $.ajax({
                        url: '/manager_sign',
                        data: {
                            Account: a,
                            Password: p
                        },
                        type: 'POST',
                        success: function (res) {
                            var result = JSON.parse(res);
                            if(result.status =='OK'){
                                alert('注册成功！');
                            }
                            else{
                                alert(result.status);
                            }
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                }
            else{
                alert('密码强度不够！');
            }
        }
        else{
            alert('账户名不符合要求！');
        }
    }
    })

})