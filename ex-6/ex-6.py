# -*- coding:utf-8 -*-
import os
from flask import Flask, render_template, json, request, redirect, session, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ksy1452254'
app.config['MYSQL_DATABASE_DB'] = 'manager'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

app.secret_key = 'you will never know'
mysql.init_app(app)


# 注销功能，退出登录
@app.route('/manager_logout')
def manager_logout():
    session.pop('manager', None)    # 销毁会话
    return redirect('/')


# 返回root管理员主页
@app.route('/show_manager_home')
def show_manager_home():
    m = session.get('manager')
    if m is 1:
        return render_template('root_home.html')
    elif m > 0:
        return render_template('ord_home.html')
    else:
        return render_template('error.html', error=u'未授权访问！')


# 管理员登录功能，登陆失败时返回错误信息
@app.route('/manager_validate_login', methods=['POST'])
def manager_validate_login():
    try:
        account = request.form['inputAccount']
        password = request.form['inputPassword']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_validateManagerlogin', (account,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][1]), password):
                session['manager'] = data[0][0]
                return redirect('/show_manager_home')
            else:
                return render_template('error.html', error=u'账号或密码错误！')
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


#  root权限的管理员添加普通管理员功能，不成功时需要返回错误信息
@app.route('/create_manager', methods=['POST'])
def create_manager():
    try:
        if session.get('manager'):      # 检测会话是否有效
            account = request.form['Account']
            password = request.form['Password']
            conn = mysql.connect()
            cursor = conn.cursor()      # 连接数据库，获得数据指针
            hash_psd = generate_password_hash(password)
            cursor.callproc('sp_createManager', (account, hash_psd))
            data = cursor.fetchall()    # 获取数据库返回信息
            if len(data) == 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '管理员已经存在！'})
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/delete_manager', methods=['POST'])
def delete_manager():
    try:
        if session.get('manager'):
            manager_id = request.form['Id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteManager', (manager_id, ))
            result = cursor.fetchall()
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': '删除失败！'})
        else:
            return render_template('error.html', u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


# 获得所有的管理员信息
@app.route('/get_all_manager')
def get_all_manager():
    try:
        if session.get('manager'):
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getallManager', )
            managers = cursor.fetchall()
            managers_dict = []
            if cursor.rowcount is 0:  # 表示查找集合为空
                return json.dumps(managers_dict)
            else:
                for m in managers:
                    m_dict = {
                        'Id': m[0],
                        'Account': m[1],
                        'Level': m[2]
                    }
                    managers_dict.append(m_dict)
                return json.dumps(managers_dict)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/get_manager_byid')
def get_manager_byid():
    try:
        if session.get('manager'):
            manager_id = session.get('manager')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getManager_byid', (manager_id,))
            result = cursor.fetchall()
            manager = list()
            manager.append({'Id': result[0][0], 'Account': result[0][1], 'Level': result[0][2]})
            return json.dumps(manager)
        else:
            return render_template('error.html', error=u'未授权访问！')
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/')
def index():
    return render_template('index.html')


#  root权限的管理员添加普通管理员功能，不成功时需要返回错误信息
@app.route('/manager_sign', methods=['POST'])
def manager_sign():
    try:
        account = request.form['Account']
        password = request.form['Password']
        conn = mysql.connect()
        cursor = conn.cursor()      # 连接数据库，获得数据指针
        hash_psd = generate_password_hash(password)
        cursor.callproc('sp_createManager', (account, hash_psd))
        data = cursor.fetchall()    # 获取数据库返回信息
        if len(data) == 0:
            conn.commit()
            return json.dumps({'status': 'OK'})
        else:
            return json.dumps({'status': '管理员已经存在！'})
    except Exception as e:
        print e
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
