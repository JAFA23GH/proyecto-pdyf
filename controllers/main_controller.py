from views.main_view import MainView

class MainController:
    def __init__(self):
        self.view = MainView(None)
        self.view.Show()