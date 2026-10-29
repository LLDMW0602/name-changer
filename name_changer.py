from flask import Flask, request, render_template_string
import pymysql

app = Flask(__name__)

DB_CONFIG = {
    'host': '175.178.191.110',
    'port': 3306,
    'user': 'idac',
    'password': 'idac123456',
    'database': 'aimedb',
    'charset': 'utf8mb4'
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>游戏改名工具</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; margin-bottom: 20px; color: #333; font-size: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; color: #666; font-size: 14px; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
        input:focus { outline: none; border-color: #4CAF50; }
        button { width: 100%; padding: 12px; background: #4CAF50; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #45a049; }
        .result { margin-top: 20px; padding: 15px; border-radius: 6px; text-align: center; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>游戏改名工具</h1>
        <form method="POST">
            <div class="form-group">
                <label>User ID</label>
                <input type="number" name="user_id" placeholder="输入你的 User ID" required>
            </div>
            <div class="form-group">
                <label>新游戏名</label>
                <input type="text" name="new_name" placeholder="输入新名字（最多12字）" maxlength="12" required>
            </div>
            <button type="submit">确认修改</button>
        </form>
        {% if result %}
        <div class="result {{ result_type }}">{{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    result_type = None

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_name = request.form.get('new_name', '').strip()

        try:
            user_id = int(user_id)
        except ValueError:
            result = "❌ User ID 格式错误，请输入数字"
            result_type = "error"
            return render_template_string(HTML, result=result, result_type=result_type)

        if len(new_name) > 12:
            result = "❌ 名字太长了，最多 12 个字符"
            result_type = "error"
            return render_template_string(HTML, result=result, result_type=result_type)

        try:
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE idac_profile SET username = %s WHERE user = %s",
                (new_name, user_id)
            )
            conn.commit()

            if cursor.rowcount > 0:
                result = f"✅ 修改成功！游戏名已改为：{new_name}"
                result_type = "success"
            else:
                result = f"❌ 修改失败，UserID {user_id} 不存在"
                result_type = "error"
        except Exception as e:
            result = f"❌ 出错了：{str(e)}"
            result_type = "error"
        finally:
            if 'conn' in locals():
                conn.close()

    return render_template_string(HTML, result=result, result_type=result_type)
