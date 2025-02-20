import wx
from controllers.login_controller import LoginController

class App(wx.App):
    def OnInit(self):
        self.login_controller = LoginController()
        
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()