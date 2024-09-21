import flet as ft
from login import LoginApp

def main(page: ft.Page):
    LoginApp(page)

ft.app(target=main)
