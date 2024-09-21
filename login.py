import flet as ft
from database import Database
from home import HomeApp

class LoginApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()

        self.username_input = ft.TextField(label="Usuário", width=300)
        self.password_input = ft.TextField(label="Senha", password=True, width=300)
        self.login_button = ft.ElevatedButton("Login", on_click=self.login_clicked)
        self.signup_link = ft.TextButton("Cadastrar", on_click=self.show_signup)

        self.page.add(self.username_input, self.password_input, self.login_button, self.signup_link)
        

    def login_clicked(self, e):
        username = self.username_input.value
        password = self.password_input.value
        if self.db.verify_credentials(username, password):
            self.page.clean()
            HomeApp(self.page)
        else:
            self.page.add(ft.Text("Usuário ou senha inválidos!", color="red"))


    def show_signup(self, e):
        from signup import SignupApp  # Importação aqui para evitar ciclo
        self.page.clean()
        SignupApp(self.page)
