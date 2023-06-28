import wx
import scraping
from urllib.parse import urlparse

class Mywin(wx.Frame): 
   def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title, size = (300,350)) 
      panel = wx.Panel(self) 
      box = wx.BoxSizer(wx.VERTICAL)
      
      self.title = wx.StaticText(panel, label="Scraping App", style=wx.ALIGN_CENTER)
      box.Add(self.title, 0, wx.EXPAND | wx.ALL, 5)
      
      url_sizer = wx.BoxSizer(wx.HORIZONTAL)
      url_label = wx.StaticText(panel, label="URL：")
      url_sizer.Add(url_label, 0, wx.ALL|wx.CENTER, 5)
      self.text = wx.TextCtrl(panel, size = (250,60), style=wx.TE_MULTILINE)
      url_sizer.Add(self.text, 1, wx.EXPAND | wx.ALL, 5)
      box.Add(url_sizer, 0, wx.EXPAND | wx.ALL, 5)
      
      delay_sizer = wx.BoxSizer(wx.HORIZONTAL)
      delay_label = wx.StaticText(panel, label="遅延時間：")
      delay_sizer.Add(delay_label, 0, wx.ALL|wx.CENTER, 5)
      self.delay_box = wx.TextCtrl(panel, size=(60, 20))
      self.delay_box.SetValue('0.7')  # 遅延時間を入力
      delay_sizer.Add(self.delay_box, 0, wx.ALL|wx.CENTER, 5)
      box.Add(delay_sizer, 0, wx.EXPAND | wx.ALL, 5)

      btn = wx.Button(panel, -1, "Scrape!")
      box.Add(btn, 0, wx.EXPAND | wx.ALL, 5)
      
      panel.SetSizer(box)
      self.Bind(wx.EVT_BUTTON, self.OnClicked, btn)
      self.Centre() 
      self.Show(True) 
  
   def OnClicked(self, event):
      url = self.text.GetValue()
      if not url.strip():  # URLが空白または未入力の場合
        dlg = wx.MessageDialog(self, "URLを入力してください。", "Warning", wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()
        return
      main_url = urlparse(url).netloc
      try:
        delay = float(self.delay_box.GetValue())
      except ValueError:
        dlg = wx.MessageDialog(self, "適切な遅延時間（数値）を入力してください。", "Warning", wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()
        return
      data = scraping.explore_links_until_exhausted(url, main_url, delay)
      scraping.write_to_csv(data, 'output.csv')
      dlg = wx.MessageDialog(self, "Scraping Completed! Data written to output.csv.", "Info", wx.OK)
      dlg.ShowModal()
      dlg.Destroy() 
  
app = wx.App() 
Mywin(None,"Scraping App")
app.MainLoop()
