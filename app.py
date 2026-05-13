from flask import Flask, render_template_string, request, redirect, url_for, session
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)
app.secret_key = "campus_anti_bully_2026_secret_888"

# 邮箱配置（和之前保持一致）
SENDER_EMAIL = "2833146163@qq.com"
SENDER_PASSWORD = "sfodsoojqvipdgac"
RECEIVER_EMAIL = "2833146163@qq.com"

# 基础HTML模板（带渐变背景和磨砂玻璃效果）
BASE_HTML = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>校园防欺凌安全系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: "微软雅黑", sans-serif; }
        body {
            background: linear-gradient(135deg, #111827 0%, #242a5c 100%);
            color: #fff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container { max-width: 720px; width: 100%; display: flex; flex-direction: column; gap: 24px; }
        .title { text-align: center; font-size: 36px; font-weight: bold; margin: 20px 0; }
        .glass-card {
            background: rgba(45, 55, 86, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(74, 91, 139, 0.5);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .btn-group { display: flex; flex-direction: column; gap: 16px; }
        .btn {
            padding: 16px;
            border-radius: 12px;
            font-size: 18px;
            border: none;
            color: #fff;
            background: #3b82f6;
            text-decoration: none;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn:hover { background: #2563eb; transform: translateY(-2px); }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.1);
            color: #fff;
            font-size: 16px;
        }
        .tab { display: flex; gap: 12px; margin-bottom: 20px; }
        .tab a {
            padding: 10px 20px;
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: #fff;
            text-decoration: none;
        }
        .tab a.active { background: #3b82f6; }
        .content {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 12px;
            padding: 20px;
            min-height: 300px;
            line-height: 1.8;
        }
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
    return render_template_string(BASE_HTML.replace('{% block content %}', '''
    <h1 class="title">校园防欺凌安全系统</h1>
    <div class="glass-card">
        <div class="btn-group">
            <a href="/student" class="btn">🧑‍🎓 学生入口</a>
            <a href="/login" class="btn">👨‍🏫 管理员登录</a>
        </div>
    </div>
    '''))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['role'] = 'admin'
            return redirect('/manage')
        return '<script>alert("账号或密码错误");history.back();</script>'
    return render_template_string(BASE_HTML.replace('{% block content %}', '''
    <h1 class="title">管理员登录</h1>
    <div class="glass-card">
        <form method="POST">
            <input name="username" placeholder="账号" required>
            <input name="password" type="password" placeholder="密码" required>
            <button type="submit" class="btn">登录</button>
        </form>
    </div>
    '''))


@app.route('/student')
def student_home():
    return render_template_string(BASE_HTML.replace('{% block content %}', '''
    <div class="tab">
        <a href="/student" class="active">🏠 一键求助</a>
        <a href="/report">📝 匿名举报</a>
        <a href="/knowledge">📚 安全知识</a>
    </div>
    <div class="glass-card">
        <div class="btn-group">
            <a href="/send_sos" class="btn" style="background: #ef4444;">🚨 一键求助</a>
        </div>
    </div>
    '''))


@app.route('/send_sos')
def send_sos():
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = MIMEText(f"【紧急求助】\n时间：{now}\n学生遭遇欺凌，请立即处理！", "plain", "utf-8")
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "校园欺凌求助"

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        with open("求助记录.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] 学生求助\n")

        return '<script>alert("求助通知已发送！");location.href="/student";</script>'
    except:
        return '<script>alert("发送失败，请检查邮箱配置");location.href="/student";</script>'


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        typ = request.form.get('type')
        content = request.form.get('content')
        if not typ or not content:
            return '<script>alert("请填写完整信息");history.back();</script>'
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("举报记录.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] 类型：{typ}\n内容：{content}\n------------------------------------\n")
        return '<script>alert("举报提交成功！");location.href="/student";</script>'
    return render_template_string(BASE_HTML.replace('{% block content %}', '''
    <div class="tab">
        <a href="/student">🏠 一键求助</a>
        <a href="/report" class="active">📝 匿名举报</a>
        <a href="/knowledge">📚 安全知识</a>
    </div>
    <div class="glass-card">
        <form method="POST">
            <select name="type" required>
                <option value="肢体欺凌">肢体欺凌</option>
                <option value="语言辱骂">语言辱骂</option>
                <option value="网络欺凌">网络欺凌</option>
                <option value="孤立排挤">孤立排挤</option>
                <option value="抢夺财物">抢夺财物</option>
            </select>
            <textarea name="content" rows="6" placeholder="请描述事件经过" required></textarea>
            <button type="submit" class="btn">提交举报</button>
        </form>
    </div>
    '''))


@app.route('/knowledge')
def knowledge():
    return render_template_string(BASE_HTML.replace('{% block content %}', '''
    <div class="tab">
        <a href="/student">🏠 一键求助</a>
        <a href="/report">📝 匿名举报</a>
        <a href="/knowledge" class="active">📚 安全知识</a>
    </div>
    <div class="glass-card content">
        <h3>校园欺凌安全知识</h3><br>
        一、欺凌类型<br>
        1. 肢体欺凌：殴打、推搡、抢夺物品<br>
        2. 语言欺凌：辱骂、侮辱性外号<br>
        3. 社交欺凌：孤立、排挤<br>
        4. 网络欺凌：造谣、P图、曝光隐私<br><br>
        二、正确做法<br>
        1. 保护自身安全<br>
        2. 不单独对峙<br>
        3. 及时告诉老师、家长<br>
        4. 保留证据<br>
        5. 使用系统求助/举报<br><br>
        三、重要提醒<br>
        遇到欺凌不要沉默！求助不是懦弱，是勇敢！
    </div>
    '''))


@app.route('/manage')
def manage():
    if session.get('role') != 'admin':
        return redirect('/login')
    try:
        with open("求助记录.txt", "r", encoding="utf-8") as f:
            sos_records = f.read()
    except:
        sos_records = "暂无求助记录"
    try:
        with open("举报记录.txt", "r", encoding="utf-8") as f:
            report_records = f.read()
    except:
        report_records = "暂无举报记录"
    return render_template_string(BASE_HTML.replace('{% block content %}', f'''
    <div class="tab">
        <a href="/manage?sos=1" class="{'active' if request.args.get('sos') else ''}">📄 求助记录</a>
        <a href="/manage" class="{'active' if not request.args.get('sos') else ''}">📋 举报记录</a>
    </div>
    <div class="glass-card content">
        {sos_records if request.args.get('sos') else report_records}
    </div>
    '''))


# 适配 Vercel 的入口
def handler(event, context):
    return app(event, context)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)