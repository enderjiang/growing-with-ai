from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
#To use reportlab in Mandarin, make sure you install the mandarin font in following folder
#Lib\site-packages\reportlab\fonts
#and define it at the beginning of program

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))
c = canvas.Canvas(BASE_DIR+'/book/'+"hello.pdf")
c.setFont('SimHei',12)
c.drawString(100,100,"世界你好2")
c.showPage()
c.save()



#learning how to change paragraph
# https://www.geeksforgeeks.org/textwrap-text-wrapping-filling-python/