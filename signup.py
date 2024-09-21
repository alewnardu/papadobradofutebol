import flet as ft
from database import Database
from login import LoginApp

class SignupApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()

        self.username_input = ft.TextField(label="Usuário", width=300)
        self.password_input = ft.TextField(label="Senha", password=True, width=300)
        self.password_confirm_input = ft.TextField(label="Confirmar senha", password=True, width=300)
        self.signup_button = ft.ElevatedButton("Cadastrar", on_click=self.signup_clicked)
        self.back_to_login_link = ft.TextButton("Voltar ao Login", on_click=self.back_to_login)

        self.page.add(self.username_input, self.password_input, self.password_confirm_input, self.signup_button, self.back_to_login_link)

    def signup_clicked(self, e):
        username = self.username_input.value
        password = self.password_input.value
        password_confirm = self.password_confirm_input.value
        if((password and password_confirm) and password == password_confirm):
            result = self.db.add_user(username, password)
        else:
            self.page.add(ft.Text("As senhas não coincidem!", color="red"))
        
        if result["success"]:
            self.page.add(ft.Text(result["message"], color="green"))
        else:
            self.page.add(ft.Text(result["message"], color="red"))


    def back_to_login(self, e):
        from login import LoginApp  # Importação aqui para evitar ciclo
        self.page.clean()
        LoginApp(self.page)
