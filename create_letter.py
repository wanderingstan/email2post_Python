# -*- coding: utf-8 -*-

#
# TODO: Accept an array of emails (with text and images) instead of one big text string
# TODO: Convert to a python object and get rid of globals!
#
# User's guide: http://www.reportlab.com/docs/reportlab-userguide.pdf
# Based on this sample code: https://bitbucket.org/rptlab/reportlab/src/c0d5cf334170a03a67ac8bc07b52e72e06f8aa81/demos/odyssey/fodyssey.py?at=default

import sys, copy, os
from reportlab.platypus import *
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
import reportlab.rl_config
reportlab.rl_config.invariant = 1

from e2p_config import config

import pprint
pp = pprint.PrettyPrinter(indent=4)

styles = getSampleStyleSheet()

def myPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def go(pdfFilename):
    """ Create the pdf """
    def myCanvasMaker(fn,**kw):
        from reportlab.pdfgen.canvas import Canvas
        canv = Canvas(fn,**kw)
        # attach our callback to the canvas
        canv.myOnDrawCB = myOnDrawCB
        return canv

    doc = BaseDocTemplate(pdfFilename,showBoundary=0)

    #Two Columns
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
                        doc.height, id='col2')
    doc.addPageTemplates([
                        PageTemplate(id='TwoCol',frames=[frame1,frame2], onPage=myPages),
                        ])
    doc.build(Elements,canvasmaker=myCanvasMaker)

Elements = [] # BAD global var

def myOnDrawCB(canv,kind,label):
    """
    Boilerplate page stuff, e.g. footer text
    """
    print 'myOnDrawCB(%s)'%kind, 'Page number=', canv.getPageNumber(), 'label value=', label

ParaStyle = copy.deepcopy(styles["Normal"])
ParaStyle.spaceBefore = 0.1*inch
ParaStyle.alignment = TA_JUSTIFY
ParaStyle.fontName = "Times-Roman"

useTwoCol = 'notwocol' not in sys.argv
def spacer(inches):
    Elements.append(Spacer(0.1*inch, inches*inch))

def p(txt, style=ParaStyle):
    Elements.append(Paragraph(txt, style))

    # im = Image("fetter.jpg", width=2*inch, height=2*inch)
    # im.hAlign = 'LEFT'
    # Elements.append(im)

def pdfFromText(text, pdfFilename):
    """ 
    Create a pdf from a text string 
    """
    from time import time
    E = []
    text = text.strip()
    L=map(str.strip,text.split('\n'))

    def mainText(L):
        """
        Go through lines, convert to paragraphs.
        """
        P = []
        while L:
            E=[]
            while L and L[0]:
                E.append(L.pop(0))
            P.append(E)
            if L:
                while not L[0]: L.pop(0)
        yield P

    for P in mainText(L):
        for x in P:
            E.append([p,' '.join(x)])

    del L
    # What the hell is happening here?
    for i in xrange(len(E)):
        E[i][0](*E[i][1:])
    del E
    go(pdfFilename)

test_email_text = """
This is a test email
"""

# # need to re-instll xcode tools:
# # http://stackoverflow.com/questions/19548011/cannot-install-lxml-on-mac-os-x-10-9
# import lxml
# from lxml.html.clean import clean_html
# c = clean.Cleaner(allowed_tags=['b','i'], remove_unknown_tags=False)
# ted = clean_html(bob)


# print ted

if __name__=='__main__':
    pdfFromText(test_email_text,"sample1.pdf")

    