# src/extension/extesion.py
from flask_login import LoginManager
from flask_mail import Mail
from flask_mysqldb import MySQL
from forms import crearEventoForm,contactoform,perfilform,registerForm,loginform,CambiarContraseñaForm
from flask import Flask, render_template, redirect, url_for, request, flash,Blueprint,send_file
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from entities.ModelUser import ModelUser
from utils.email_sender import plantilla_bienvenida,enviar_correo_bienvenida,generar_y_enviar_entrada_qr
import cloudinary
import cloudinary.uploader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import qrcode
from urllib.parse import unquote
from itsdangerous import URLSafeTimedSerializer
from config import Config
from werkzeug.security import generate_password_hash
from datetime import datetime
from filtros import format_hora,format_fecha
db = MySQL()
mail = Mail()
login_manager = LoginManager()
