import wx

class VentanaGestionarEntidades(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, *args, **kw):
        super(VentanaGestionarEntidades, self).__init__(parent, title="Gestionar Entidades", size=(600, 400), *args, **kw)
        self.controlador = controlador
        self.usuario = usuario
        self.rol = rol
        self.entities = ["Tipo de Brecha", "Tipo de Proyecto", "Procesos Corregidos", 
                         "Procesos Realizados", "Investigadores", "Empresas", "Subtipo de Ficha", 
                         "Tipo de Irregularidad", "Subtipo de Irregularidad", "Procedencia Casos"]
        
        self.InitUI()

        # Manejar el evento de cierre de la ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)
    
    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Entity Selector
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        entity_lbl = wx.StaticText(panel, label="Seleccione la entidad a gestionar:")
        hbox1.Add(entity_lbl, flag=wx.RIGHT, border=8)
        self.entity_choice = wx.Choice(panel, choices=self.entities)
        self.entity_choice.Bind(wx.EVT_CHOICE, self.OnEntitySelected)
        hbox1.Add(self.entity_choice, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # Placeholder for dynamic content
        self.dynamic_panel = wx.Panel(panel)
        vbox.Add(self.dynamic_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        panel.SetSizer(vbox)
        self.Centre()
        self.Show()
    
    def OnEntitySelected(self, event):
        entity = self.entity_choice.GetStringSelection()
        self.LoadEntityManagementUI(entity)
    
    def LoadEntityManagementUI(self, entity):
        # Clear existing content
        for child in self.dynamic_panel.GetChildren():
            child.Destroy()
        
        # Create new content based on selected entity
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Fetch records for the selected entity
        records = self.GetEntityRecords(entity)
        
        # Record List
        self.record_list = wx.ListCtrl(self.dynamic_panel, style=wx.LC_REPORT)
        self.record_list.InsertColumn(0, 'ID', width=50)
        self.record_list.InsertColumn(1, 'Nombre', width=200)
        for idx, record in enumerate(records):
            self.record_list.InsertItem(idx, str(record['id']))
            self.record_list.SetItem(idx, 1, record['name'])
        vbox.Add(self.record_list, proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=10)
        
        # Action Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(self.dynamic_panel, label='Agregar')
        add_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnAddRecord(entity))
        hbox.Add(add_btn, flag=wx.RIGHT, border=5)
        edit_btn = wx.Button(self.dynamic_panel, label='Editar')
        edit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnEditRecord(entity))
        hbox.Add(edit_btn, flag=wx.RIGHT, border=5)
        delete_btn = wx.Button(self.dynamic_panel, label='Eliminar')
        delete_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnDeleteRecord(entity))
        hbox.Add(delete_btn)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER)
        
        self.dynamic_panel.SetSizer(vbox)
        self.dynamic_panel.Layout()
    
    def GetEntityRecords(self, entity):
        # Placeholder method to get records from the database or data source
        # For now, return dummy data
        dummy_data = [{'id': 1, 'name': f'{entity} A'}, {'id': 2, 'name': f'{entity} B'}]
        return dummy_data
    
    def OnAddRecord(self, entity):
        dlg = EntityDialog(self, title=f"Agregar {entity}", entity=entity)
        dlg.ShowModal()
        dlg.Destroy()
        # Refresh the UI after adding
        self.LoadEntityManagementUI(entity)
    
    def OnEditRecord(self, entity):
        selected_item = self.record_list.GetFirstSelected()
        if selected_item == -1:
            wx.MessageBox('Seleccione un registro para editar.', 'Error', wx.OK | wx.ICON_ERROR)
            return
        record_id = int(self.record_list.GetItemText(selected_item))
        dlg = EntityDialog(self, title=f"Editar {entity}", entity=entity, record_id=record_id)
        dlg.ShowModal()
        dlg.Destroy()
        # Refresh the UI after editing
        self.LoadEntityManagementUI(entity)
    
    def OnDeleteRecord(self, entity):
        selected_item = self.record_list.GetFirstSelected()
        if selected_item == -1:
            wx.MessageBox('Seleccione un registro para eliminar.', 'Error', wx.OK | wx.ICON_ERROR)
            return
        record_id = int(self.record_list.GetItemText(selected_item))
        # Implement deletion logic here
        confirm = wx.MessageBox(f'¿Está seguro de eliminar el registro {record_id}?', 'Confirmar', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if confirm == wx.YES:
            # Delete the record
            wx.MessageBox('Registro eliminado.', 'Información', wx.OK | wx.ICON_INFORMATION)
            self.LoadEntityManagementUI(entity)

class EntityDialog(wx.Dialog):
    def __init__(self, parent, title, entity, record_id=None):
        super(EntityDialog, self).__init__(parent, title=title, size=(350, 250))
        
        self.entity = entity
        self.record_id = record_id
        self.is_edit = record_id is not None
        
        self.InitUI()
        if self.is_edit:
            self.LoadRecordData()
        
    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Depending on the entity, define the fields. For simplicity, let's assume each entity has only a 'name' field.
        lbl = wx.StaticText(self, label="Nombre:")
        vbox.Add(lbl, flag=wx.LEFT | wx.TOP, border=10)
        self.name_txt = wx.TextCtrl(self)
        vbox.Add(self.name_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # Action Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        save_btn = wx.Button(self, label='Guardar')
        save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        hbox.Add(save_btn, flag=wx.RIGHT, border=5)
        cancel_btn = wx.Button(self, label='Cancelar')
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)
        hbox.Add(cancel_btn)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        
        self.SetSizer(vbox)
    
    def LoadRecordData(self):
        # Load data for the record with self.record_id
        # This is a placeholder. Replace with actual data retrieval.
        record = {'id': self.record_id, 'name': f'{self.entity} Nombre'}
        self.name_txt.SetValue(record['name'])
    
    def OnSave(self, event):
        name = self.name_txt.GetValue()
        if not name:
            wx.MessageBox('El campo "Nombre" es obligatorio.', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if self.is_edit:
            # Update the record
            wx.MessageBox('Registro actualizado exitosamente.', 'Información', wx.OK | wx.ICON_INFORMATION)
        else:
            # Create a new record
            wx.MessageBox('Registro creado exitosamente.', 'Información', wx.OK | wx.ICON_INFORMATION)
        self.Destroy()
    
    def OnCancel(self, event):
        self.Destroy()

    def on_close(self, event):
        """Maneja el cierre de la ventana."""
        dialogo = wx.MessageDialog(self, "¿Estás seguro de que quieres salir?", "Cerrar aplicación", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = dialogo.ShowModal()
        if respuesta == wx.ID_YES:
            self.Destroy()  # Cierra la ventana
            wx.Exit()  # Cierra la aplicación completamente
        else:
            event.Veto()  # Cancela el cierre de la ventana

