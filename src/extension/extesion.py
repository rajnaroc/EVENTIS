# src/extension/extesion.py
from flask_login import LoginManager
from flask_mail import Mail
from flask_mysqldb import MySQL
from forms import crearEventoForm,contactoform,perfilform,registerForm,loginform
from flask import Flask, render_template, redirect, url_for, request, flash,Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from entities.ModelUser import ModelUser
from utils.email_sender import plantilla_bienvenida,enviar_correo_bienvenida,generar_y_enviar_entrada_qr
import cloudinary
import cloudinary.uploader

db = MySQL()
mail = Mail()
login_manager = LoginManager()
