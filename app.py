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

      self.slider = wx.Slider(panel, value = 20, minValue = 0, maxValue = 30, size = (250, -1), style = wx.SL_LABELS)
      box.Add(self.slider, 0, wx.EXPAND | wx.ALL, 5)

      btn = wx.Button(panel, -1, "Scrape!")
      box.Add(btn, 0, wx.EXPAND | wx.ALL, 5)
      
      panel.SetSizer(box)
      self.Bind(wx.EVT_BUTTON, self.OnClicked, btn)
      self.Centre() 
      self.Show(True) 
  
   def OnClicked(self, event):
      url = self.text.GetValue()
      main_url = urlparse(url).netloc
      delay = self.slider.GetValue() / 10.0  # スライダーの値を10で割ることで、0.0から3.0の範囲を得る
      data = scraping.explore_links_until_exhausted(url, main_url, delay)
      scraping.write_to_csv(data, 'output.csv')
      dlg = wx.MessageDialog(self, "Scraping Completed! Data written to output.csv.", "Info", wx.OK)
      dlg.ShowModal()
      dlg.Destroy() 
  
app = wx.App() 
Mywin(None,"Scraping App")
app.MainLoop()
