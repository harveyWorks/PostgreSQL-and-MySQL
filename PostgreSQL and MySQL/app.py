from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///artists.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

bootstrap = Bootstrap5(app)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Artist(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str]
    song_title: Mapped[str]
    genre: Mapped[str]
    albums = relationship("Album", back_populates="artist", cascade="all, delete")

class Album(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    title: Mapped[str]
    release_year: Mapped[int]
    
    artist_id: Mapped[int] = mapped_column(Integer, ForeignKey("artist.id"), nullable=False)
    artist = relationship("Artist", back_populates="albums")

@app.route("/")
def home():
    artists = Artist.query.options(db.joinedload(Artist.albums)).all()
    return render_template("home.html", artists=artists)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        song_title = request.form["song_title"]
        genre = request.form["genre"]
        album_title = request.form["album_title"]
        release_year = request.form["release_year"]

        artist = Artist(name=name, song_title=song_title, genre=genre)
        db.session.add(artist)
        db.session.commit()

        if album_title and release_year:
            album = Album(title=album_title, release_year=int(release_year), artist_id=artist.id)
            db.session.add(album)
            db.session.commit()

        return redirect(url_for("home"))
    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)
