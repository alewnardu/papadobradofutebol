import flet as ft

class HomeApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Images Example"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 50
        self.page.update()

        img = ft.Image(
            src=f"/icons/icon-512.png",
            width=100,
            height=100,
            fit=ft.ImageFit.CONTAIN,
        )
        images = ft.Row(expand=1, wrap=False, scroll="always")

        self.page.add(img, images)

        for i in range(0, 30):
            images.controls.append(
                ft.Image(
                    src=f"https://picsum.photos/200/200?{i}",
                    width=200,
                    height=200,
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )
        self.page.update()
