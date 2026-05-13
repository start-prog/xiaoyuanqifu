from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "campus_anti_bully_2026_secret_888"

USER_DATA = {
    "teacher": {"pwd": "Teacher2026", "role": "老师"},
    "admin": {"pwd": "Admin2026", "role": "管理员"}
}

BASE_HTML = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>校园防欺凌安全系统</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:"微软雅黑",sans-serif;}
        body{background-color: #000030;color: #ffffff;min-height: 100vh;padding: 20px;}
        .container{max-width: 700px;margin: 0 auto;}
        .title{text-align: center;font-size: 30px;font-weight: bold;margin: 40px 0;}
        .btn{display: block;width: 100%;padding: 16px;margin: 12px 0;font-size: 18px;border: none;border-radius: 10px;color: #fff;cursor: pointer;text-decoration: none;text-align: center;}
        .btn-blue{background:#1E6FCE;}
        .btn-green{background:#27ae60;}
        .btn-purple{background:#9b59b6;}
        .btn-red{background:#e74c3c;}
        .btn-pink{background:#ff6b6b;}
        .box{background:rgba(255,255,255,0.12);padding:25px;border-radius:12px;margin:20px 0;}
        input,textarea,select{width:100%;padding:12px 15px;margin:10px 0;border-radius:8px;border:none;font-size:16px;background:#f5f5f5;color:#333;}
        .tab{display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;}
        .tab a{background:rgba(255,255,255,0.15);padding:12px 20px;border-radius:8px;color:#fff;text-decoration:none;}
        .tab a.active{background:rgba(255,255,255,0.3);}
        .content{background:rgba(255,255,255,0.08);padding:25px;border-radius:12px;min-height:320px;line-height:1.8;}
        .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px;}
        .logout-btn{padding:8px 15px;font-size:14px;}
    </style>
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    html = BASE_HTML.replace('{% block content %}', '''
    <div class="title">校园防欺凌安全系统</div>
    <a href="/student" class="btn btn-blue">👨‍🎓 学生入口（直接进入）</a>
    <a href="/login/teacher" class="btn btn-green">👩‍🏫 老师登录</a>
    <a href="/login/admin" class="btn btn-purple">🔧 管理员登录</a>
    ''')
    return render_template_string(html)

@app.route('/student')
def student_enter():
    session['role'] = "学生"
    return redirect('/student/home')

@app.route('/login/<role_type>')
def login_page(role_type):
    tip = "老师登录" if role_type == "teacher" else "管理员登录"
    html = BASE_HTML.replace('{% block content %}', f'''
    <div class="title">{tip}</div>
    <div class="box">
        <form action="/check/{role_type}" method="post">
            <input name="username" placeholder="请输入账号" required>
            <input name="password" type="password" placeholder="请输入密码" required>
            <button class="btn btn-blue">确认登录</button>
        </form>
    </div>
    ''')
    return render_template_string(html)

@app.route('/check/<role_type>', methods=['POST'])
def check_login(role_type):
    username = request.form.get("username")
    pwd = request.form.get("password")
    if username in USER_DATA and USER_DATA[username]["pwd"] == pwd:
        session['role'] = USER_DATA[username]["role"]
        return redirect('/manage')
    return '''<script>alert("账号或密码错误");history.back();</script>'''

@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect('/')

@app.route('/student/home')
def stu_home():
    if session.get('role') != "学生":
        return redirect('/')
    content = '''
    <div class="top">
        <h2>学生中心 - 一键求助</h2>
        <a href="/logout" class="btn btn-pink logout-btn">退出登录</a>
    </div>
    <div class="tab">
        <a href="/student/home" class="active">🏠 一键求助</a>
        <a href="/student/report">📝 匿名举报</a>
        <a href="/student/know">📚 安全知识</a>
    </div>
    <div class="content">
        <a href="/do_sos" class="btn btn-red">🚨 紧急一键求助</a>
        <p style="text-align:center;margin-top:30px;font-size:16px;">遇到校园欺凌，可立即发起求助</p>
    </div>
    '''
    return render_template_string(BASE_HTML.replace('{% block content %}', content))

@app.route('/student/report')
def stu_report():
    if session.get('role') != "学生":
        return redirect('/')
    content = '''
    <div class="top">
        <h2>学生中心 - 匿名举报</h2>
        <a href="/logout" class="btn btn-pink logout-btn">退出登录</a>
    </div>
    <div class="tab">
        <a href="/student/home">🏠 一键求助</a>
        <a href="/student/report" class="active">📝 匿名举报</a>
        <a href="/student/know">📚 安全知识</a>
    </div>
    <div class="content">
        <form action="/submit_report" method="post">
            <select name="type">
                <option>肢体欺凌</option>
                <option>语言辱骂</option>
                <option>网络欺凌</option>
                <option>孤立排挤</option>
                <option>抢夺财物</option>
            </select>
            <textarea name="content" rows="6" placeholder="请详细描述事件经过" required></textarea>
            <input name="addr" placeholder="事发地点（选填）">
            <button class="btn btn-blue">提交匿名举报</button>
        </form>
    </div>
    '''
    return render_template_string(BASE_HTML.replace('{% block content %}', content))

@app.route('/student/know')
def stu_know():
    if session.get('role') != "学生":
        return redirect('/')
    content = '''
    <div class="top">
        <h2>校园安全知识</h2>
        <a href="/logout" class="btn btn-pink logout-btn">退出登录</a>
    </div>
    <div class="tab">
        <a href="/student/home">🏠 一键求助</a>
        <a href="/student/report">📝 匿名举报</a>
        <a href="/student/know" class="active">📚 安全知识</a>
    </div>
    <div class="content">
一、常见校园欺凌类型<br>
1.肢体欺凌：殴打、推搡、抢夺物品<br>
2.语言欺凌：辱骂、起侮辱性外号<br>
3.社交欺凌：故意孤立、拉帮排挤<br>
4.网络欺凌：造谣、曝光隐私、恶意P图<br><br>

二、遭遇欺凌正确做法<br>
1.优先保护自身人身安全<br>
2.不冲动对峙，避免激化矛盾<br>
3.及时告知家长、班主任、学校老师<br>
4.保留聊天记录、照片、录音等证据<br>
5.使用本系统一键求助、匿名举报<br><br>

三、自我保护准则<br>
✅ 遇到欺凌不要默默忍受<br>
✅ 勇敢求助不是懦弱<br>
✅ 拒绝欺凌、从我做起
    </div>
    '''
    return render_template_string(BASE_HTML.replace('{% block content %}', content))

@app.route('/do_sos')
def do_sos():
    return '''<script>alert("求助提交成功！工作人员将及时关注");location.href="/student/home";</script>'''

@app.route('/submit_report', methods=['POST'])
def submit_report():
    return '''<script>alert("匿名举报提交成功");location.href="/student/report";</script>'''

@app.route('/manage')
def manage_page():
    role = session.get('role')
    if not role or role not in ['老师','管理员']:
        return redirect('/')

    content = f'''
    <div class="top">
        <h2>{role} 管理中心</h2>
        <a href="/logout" class="btn btn-pink logout-btn">退出登录</a>
    </div>
    <div class="tab">
        <a href="/manage?sos=1" class="{'active' if request.args.get('sos') else ''}">📄 求助记录</a>
        <a href="/manage" class="{'active' if not request.args.get('sos') else ''}">📋 举报记录</a>
    </div>
    <div class="content" style="white-space:pre-wrap;">
{{"【求助记录】\\n暂无记录" if request.args.get("sos") else "【举报记录】\\n暂无记录"}}
    </div>
    '''
    return render_template_string(BASE_HTML.replace('{% block content %}', content))

def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)