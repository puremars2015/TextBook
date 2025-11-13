from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="zh-Hant">
<head>
    <meta charset="utf-8">
    <title>Hello</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
"""

@app.route("/")
def index():
        return render_template_string(HTML)

if __name__ == "__main__":
        # 開發用伺服器，可改為 host="0.0.0.0" 在網路上可存取
        app.run(host="0.0.0.0", port=80, debug=True)