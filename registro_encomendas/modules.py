import sqlite3
import webbrowser
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox, ttk

import awesometkinter as atk
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, SimpleDocTemplate

import mysql.connector
