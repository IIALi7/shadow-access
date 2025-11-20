from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

FLAG = "CSC{Cookie_Role_4dmin}"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    صفحة تسجيل الدخول:
    - GET: تعرض الفورم
    - POST: تستقبل username وتضبط الكوكيز role=user
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip() or "guest"

        resp = make_response(redirect(url_for("profile")))
        # نضبط كوكي بسيطة بدون أي حماية (هنا الفكرة)
        resp.set_cookie("username", username, httponly=False)
        resp.set_cookie("role", "user", httponly=False)
        return resp

    return render_template("index.html")


@app.route("/profile")
def profile():
    """
    صفحة البروفايل:
    - توضح لليوزر أن صلاحياته user
    - تلّمح أن لوحة الإدارة تعتمد على الكوكيز
    """
    username = request.cookies.get("username", "guest")
    role = request.cookies.get("role", "guest")
    return render_template("profile.html", username=username, role=role)


@app.route("/admin")
def admin():
    """
    صفحة لوحة الإدارة:
    - لو role=admin في الكوكي → نعرض الفلاق
    - غير كذا → رسالة رفض بسيطة تبين له دوره الحالي
    """
    role = request.cookies.get("role", "guest")
    is_admin = role == "admin"
    flag = FLAG if is_admin else None
    return render_template("admin.html", role=role, flag=flag, is_admin=is_admin)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
