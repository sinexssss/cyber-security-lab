from flask import Flask, request, redirect

app = Flask(__name__)

users = {}
notes = {}

current_user = ""


@app.route("/")
def home():
    return """
    <html>
    <head>
        <title> notes </title>

        <style>
            body{
                font-family: Arial;
                background: linear-gradient(135deg,#ffd6eb,#ffeef8);
                text-align:center;
                padding:40px;
            }

            .card{
                background:white;
                width:500px;
                margin:auto;
                padding:30px;
                border-radius:25px;
                box-shadow:0 0 20px rgba(0,0,0,0.1);
            }

            h1{
                color:#ff4fa3;
            }

            input{
                width:80%;
                padding:12px;
                border-radius:12px;
                border:1px solid #ffb6d9;
            }

            button{
                background:#ff66b3;
                color:white;
                border:none;
                padding:12px 20px;
                border-radius:12px;
                cursor:pointer;
            }

            button:hover{
                background:#ff3d9a;
            }
        </style>

    </head>

    <body>

        <div class="card">

            <h1>🌸 YOUR SECRET NOTES 🌸</h1>

            <h2>Регистрация</h2>

            <form action="/register" method="post">
                <input name="username" placeholder="Логин"><br><br>
                <input name="password" placeholder="Пароль"><br><br>
                <button>Зарегистрироваться</button>
            </form>

            <hr>

            <h2>Вход</h2>

            <form action="/login" method="post">
                <input name="username" placeholder="Логин"><br><br>
                <input name="password" placeholder="Пароль"><br><br>
                <button>Войти</button>
            </form>

        </div>

    </body>
    </html>
    """


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    users[username] = password
    notes[username] = []

    return """
    <h2>💖 Регистрация успешна!</h2>
    <a href="/">На главную</a>
    """


@app.route("/login", methods=["POST"])
def login():
    global current_user

    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        current_user = username
        return redirect("/notes")

    return """
    <h2>❌ Неверный логин или пароль</h2>
    <a href="/">Назад</a>
    """


@app.route("/notes")
def show_notes():
    result = ""

    for i, note in enumerate(notes[current_user]):
        result += f"""
        <div style="
            background:#fff0f7;
            padding:15px;
            margin:10px;
            border-radius:15px;
        ">
            {note}
            <br><br>
            <a href="/delete/{i}">🗑️ Удалить</a> |
            <a href="/edit/{i}">✏️ Изменить</a>
        </div>
        """

    return f"""
    <html>
    <body style="
        background:#ffe6f2;
        font-family:Arial;
        text-align:center;
        padding:40px;
    ">

    <div style="
        background:white;
        width:650px;
        margin:auto;
        padding:30px;
        border-radius:25px;
    ">

    <div style="margin-bottom:20px;">
        <a href="/" style="
            background:#ff66b3;
            color:white;
            padding:10px 15px;
            border-radius:12px;
            text-decoration:none;
            margin-right:10px;
        ">
            ← Главное меню
        </a>

        <a href="/logout" style="
            background:#ff4fa3;
            color:white;
            padding:10px 15px;
            border-radius:12px;
            text-decoration:none;
        ">
            🚪 Выйти
        </a>
    </div>

    <h1 style="color:#ff4fa3;">
        🌸 Добро пожаловать, {current_user}
    </h1>

    <h3>📝 Всего заметок: {len(notes[current_user])}</h3>

    {result}

    <hr>

    <form action="/add_note" method="post">
        <input name="note" placeholder="Введите новую заметку">
        <br><br>
        <button>➕ Добавить заметку</button>
    </form>

    </div>

    </body>
    </html>
    """


@app.route("/add_note", methods=["POST"])
def add_note():
    note = request.form["note"]
    notes[current_user].append(note)
    return redirect("/notes")


@app.route("/delete/<int:index>")
def delete(index):
    if index < len(notes[current_user]):
        notes[current_user].pop(index)
    return redirect("/notes")


@app.route("/edit/<int:index>")
def edit(index):
    old_note = notes[current_user][index]

    return f"""
    <html>
    <body style="
        background:#ffe6f2;
        text-align:center;
        font-family:Arial;
        padding:40px;
    ">

    <h2>✏️ Редактирование заметки</h2>

    <form action="/save_edit/{index}" method="post">
        <input name="note" value="{old_note}" style="width:400px;padding:12px;">
        <br><br>
        <button>💾 Сохранить</button>
    </form>

    </body>
    </html>
    """


@app.route("/save_edit/<int:index>", methods=["POST"])
def save_edit(index):
    notes[current_user][index] = request.form["note"]
    return redirect("/notes")


@app.route("/logout")
def logout():
    global current_user
    current_user = ""
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)