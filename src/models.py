from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()
    
class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    singup_date: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user_id: Mapped[List["FavoritesPlanets"]] = relationship(back_populates="Users")
    user_id: Mapped[List["FavoritesCharacters"]] = relationship(back_populates="Users")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    race: Mapped[str] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)

    character_id: Mapped[List["FavoritesCharacters"]] = relationship(back_populates="characters")
    origin_planet: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    parent: Mapped["Planets"] = relationship(back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)

    planet_id: Mapped[List["FavoritesPlanets"]] = relationship(back_populates="planets")
    children: Mapped[List["Characters"]] = relationship(back_populates="planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class FavoritesCharacters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    parent: Mapped["Users"] = relationship(back_populates="favoritesCharacters")
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    parent: Mapped["Characters"] = relationship(back_populates="favoritesCharacters")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "character": self.character_id,
            # do not serialize the password, its a security breach
        }
    
class FavoritesPlanets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    parent: Mapped["Users"] = relationship(back_populates="favoritesPlanets")
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    parent: Mapped["Planets"] = relationship(back_populates="favoritesPlanets")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "planet": self.planet_id,
            # do not serialize the password, its a security breach
        }
