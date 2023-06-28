import wx
import scraping
from urllib.parse import urlparse

class Mywin(wx.Frame): 
   def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title, size = (300,350)) 
      panel = wx.Panel(self) 
      box = wx.BoxSizer(wx.VERTICAL)

      self.text = wx.TextCtrl(panel, style = wx.TE_MULTILINE, size = (250,150))
      box.Add(self.text, 1, wx.EXPAND | wx.ALL, 5)

      self.delay_box = wx.TextCtrl(panel, size=(250, 20))
      self.delay_box.SetValue('0.7')  # Set initial delay value
      box.Add(self.delay_box, 0, wx.EXPAND | wx.ALL, 5)

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
