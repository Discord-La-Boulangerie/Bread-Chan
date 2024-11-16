import os
from typing import Any
from dotenv import load_dotenv
from sqlalchemy import Table, Column, BigInteger, Boolean, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Credentials:
    def __init__(self):
        load_dotenv()
        self.host: str = os.getenv("db_host")
        self.user: str = os.getenv("db_user")
        self.password: str = os.getenv("db_password")
        self.database: str = os.getenv("db_name")
        self.port: int = 3306

    def to_dict(self) -> Any:
        return {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database
        }


class GuildConfig(Base):
    __tablename__ = 'guild_config'
    guild_id = Column(BigInteger, primary_key=True)
    public = Column(Boolean, nullable=False, default=False)
    word_react_enabled = Column(Boolean, nullable=False, default=False)
    auto_post_enabled = Column(Boolean, nullable=False, default=False)
    auto_post_channel = Column(BigInteger)
    one_msg_role_id = Column(BigInteger, nullable=False, default=0)
    one_msg_channel = Column(Boolean, nullable=False, default=False)


class UserRoles(Base):
    __tablename__ = 'user_roles'
    role_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    guild_id = Column(BigInteger, ForeignKey('guild_config.guild_id'))


class GuildWelc(Base):
    __tablename__ = 'guild_welc'
    guild_id = Column(BigInteger, primary_key=True)
    welcome_channel_id = Column(BigInteger)
    welcome_message = Column(String(4000), nullable=False,
                             default="Bienvenue sur {server_name} {member_name} !")
    enabled = Column(Boolean, nullable=False, default=False)
    img_url = Column(String(200))
    guild_id_fk = Column(BigInteger, ForeignKey('guild_config.guild_id'))


class GuildBye(Base):
    __tablename__ = 'guild_bye'
    guild_id = Column(BigInteger, primary_key=True)
    goodbye_channel_id = Column(BigInteger)
    goodbye_message = Column(String(
        4000), nullable=False, default="{member_name} a quitté le serveur, au revoir !")
    enabled = Column(Boolean, nullable=False, default=False)
    img_url = Column(String(200))
    guild_id_fk = Column(BigInteger, ForeignKey('guild_config.guild_id'))


class AutoRoles(Base):
    __tablename__ = 'auto_roles'
    guild_id = Column(BigInteger, primary_key=True)
    role_1 = Column(BigInteger)
    role_2 = Column(BigInteger)
    role_3 = Column(BigInteger)
    role_4 = Column(BigInteger)
    enabled = Column(Boolean, nullable=False, default=False)
    guild_id_fk = Column(BigInteger, ForeignKey('guild_config.guild_id'))


class EpicGameNotifier(Base):
    __tablename__ = 'epic_game_notifier'
    guild_id = Column(BigInteger, primary_key=True)
    enabled = Column(Boolean, nullable=False, default=False)
    guild_id_fk = Column(BigInteger, ForeignKey('guild_config.guild_id'))


class WMCredentials(Base):
    __tablename__ = 'wm_credentials'
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
