from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "chat.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False, default="Аноним")
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(5), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.id} {self.author}>"


with app.app_context():
    db.create_all()


MAX_MESSAGES = 100


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            error = "Введите ник."
            return render_template(
                "register.html",
                error=error,
                username=""
            )

        session["username"] = username
        return redirect(url_for("chat"))

    return render_template(
        "register.html",
        error=None,
        username=session.get("username", "")
    )


@app.route("/", methods=["GET", "POST"])
def chat():
    username = session.get("username")
    if not username:
        return redirect(url_for("register"))

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if text:
            msg = Message(
                author=username,
                text=text,
                time=datetime.now().strftime("%H:%M")
            )
            db.session.add(msg)
            db.session.commit()

            total = Message.query.count()
            if total > MAX_MESSAGES:
                to_delete = (
                    Message.query
                    .order_by(Message.created_at)
                    .limit(total - MAX_MESSAGES)
                    .all()
                )
                for m in to_delete:
                    db.session.delete(m)
                db.session.commit()

        return redirect(url_for("chat"))

    messages = (
        Message.query
        .order_by(Message.created_at.desc())
        .limit(MAX_MESSAGES)
        .all()
    )
    messages = list(reversed(messages))

    return render_template(
        "chat.html",
        messages=messages,
        username=username
    )


@app.route("/stats")
def stats():
    stats = (
        db.session.query(
            Message.author,
            func.count(Message.id).label("count")
        )
        .group_by(Message.author)
        .order_by(func.count(Message.id).desc())
        .all()
    )

    total_messages = db.session.query(func.count(Message.id)).scalar() or 0
    current_user = session.get("username")

    return render_template(
        "stats.html",
        stats=stats,
        total_messages=total_messages,
        current_user=current_user
    )


@app.route("/clear")
def clear():
    Message.query.delete()
    db.session.commit()
    return redirect(url_for("chat"))


if __name__ == "__main__":
    app.run(debug=True)