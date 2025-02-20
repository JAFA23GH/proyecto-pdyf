import wx

class VentanaCerrarCaso(wx.Frame):
    def __init__(self, parent, usuario, rol, *args, **kw):
        super(VentanaCerrarCaso, self).__init__(parent, *args, **kw)

        self.usuario = usuario
        self.rol = rol

        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(pnl, label='Seleccione el caso:')
        vbox.Add(st1, flag=wx.LEFT | wx.TOP, border=10)

        self.case_choice = wx.Choice(pnl, choices=self.get_open_cases())
        vbox.Add(self.case_choice, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st2 = wx.StaticText(pnl, label='Observaciones:')
        vbox.Add(st2, flag=wx.LEFT | wx.TOP, border=10)
        
        self.obs_txt = wx.TextCtrl(pnl, style=wx.TE_MULTILINE)
        vbox.Add(self.obs_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st3 = wx.StaticText(pnl, label='Conclusiones:')
        vbox.Add(st3, flag=wx.LEFT | wx.TOP, border=10)
        
        self.concl_txt = wx.TextCtrl(pnl, style=wx.TE_MULTILINE)
        vbox.Add(self.concl_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st4 = wx.StaticText(pnl, label='Recomendaciones:')
        vbox.Add(st4, flag=wx.LEFT | wx.TOP, border=10)
        
        self.rec_txt = wx.TextCtrl(pnl, style=wx.TE_MULTILINE)
        vbox.Add(self.rec_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        close_btn = wx.Button(pnl, label='Cerrar Caso')
        close_btn.Bind(wx.EVT_BUTTON, self.OnCloseCase)
        hbox.Add(close_btn, flag=wx.RIGHT, border=10)

        cancel_btn = wx.Button(pnl, label='Cancelar')
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)
        hbox.Add(cancel_btn, flag=wx.RIGHT, border=10)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        pnl.SetSizer(vbox)

        self.SetSize((400, 600))
        self.SetTitle('Cerrar Caso de Investigación')
        self.Centre()

    def get_open_cases(self):
        # Método para obtener la lista de casos abiertos desde la base de datos o lógica de negocio
        return ["Caso 1", "Caso 2", "Caso 3"]

    def OnCloseCase(self, event):
        # Obtener los valores de los campos
        case = self.case_choice.GetStringSelection()
        observations = self.obs_txt.GetValue()
        conclusions = self.concl_txt.GetValue()
        recommendations = self.rec_txt.GetValue()

        if not case:
            wx.MessageBox('Seleccione un caso.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        if not observations or not conclusions or not recommendations:
            wx.MessageBox('Por favor, complete todos los campos.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Implementar la lógica para cerrar el caso
        wx.MessageBox(f'Caso "{case}" cerrado con éxito.', 'Información', wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def OnCancel(self, event):
        # Lógica para cancelar y cerrar la ventana
        self.Close()

def main():
    app = wx.App()
    ex = VentanaCerrarCaso(None, usuario="Juan", rol="Investigador")
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
