import pprint

pp = pprint.PrettyPrinter(indent=4)

#Copyright ReportLab Europe Ltd. 2000-2012
#see license.txt for license details
__version__=''' $Id$ '''
__doc__=''

#REPORTLAB_TEST_SCRIPT
import sys, copy, os
from reportlab.platypus import *
_NEW_PARA=os.environ.get('NEW_PARA','0')[0] in ('y','Y','1')
_REDCAP=int(os.environ.get('REDCAP','0'))
_CALLBACK=os.environ.get('CALLBACK','0')[0] in ('y','Y','1')
if _NEW_PARA:
    def Paragraph(s,style):
        from rlextra.radxml.para import Paragraph as PPPP
        return PPPP(s,style)

from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

import reportlab.rl_config
reportlab.rl_config.invariant = 1

styles = getSampleStyleSheet()

def myPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def go():
    def myCanvasMaker(fn,**kw):
        from reportlab.pdfgen.canvas import Canvas
        canv = Canvas(fn,**kw)
        # attach our callback to the canvas
        canv.myOnDrawCB = myOnDrawCB
        return canv

    doc = BaseDocTemplate('dodyssey.pdf',showBoundary=0)

    #Two Columns
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
                        doc.height, id='col2')
    doc.addPageTemplates([
                        PageTemplate(id='TwoCol',frames=[frame1,frame2], onPage=myPages),
                        ])
    doc.build(Elements,canvasmaker=myCanvasMaker)

Elements = []

ChapterStyle = copy.deepcopy(styles["Heading1"])
ChapterStyle.alignment = TA_CENTER
ChapterStyle.fontsize = 14
InitialStyle = copy.deepcopy(ChapterStyle)
InitialStyle.fontsize = 16
InitialStyle.leading = 20
PreStyle = styles["Code"]

def myOnDrawCB(canv,kind,label):
    print 'myOnDrawCB(%s)'%kind, 'Page number=', canv.getPageNumber(), 'label value=', label

ParaStyle = copy.deepcopy(styles["Normal"])
ParaStyle.spaceBefore = 0.1*inch
if 'right' in sys.argv:
    ParaStyle.alignment = TA_RIGHT
elif 'left' in sys.argv:
    ParaStyle.alignment = TA_LEFT
elif 'justify' in sys.argv:
    ParaStyle.alignment = TA_JUSTIFY
elif 'center' in sys.argv or 'centre' in sys.argv:
    ParaStyle.alignment = TA_CENTER
else:
    ParaStyle.alignment = TA_JUSTIFY

useTwoCol = 'notwocol' not in sys.argv
def spacer(inches):
    Elements.append(Spacer(0.1*inch, inches*inch))

def p(txt, style=ParaStyle):
    Elements.append(Paragraph(txt, style))

def pre(txt, style=PreStyle):
    spacer(0.1)
    p = Preformatted(txt, style)
    Elements.append(p)

def parseOdyssey(fn):
    from time import time
    E = []
    t0=time()
    text = open(fn,'r').read().strip()

    L=map(str.strip,text.split('\n'))
    print "\n\My way\n\n"
    pp.pprint(L)

    exit

    def ambleText(L):
        """ Preamble text """
        while L and not L[0]: L.pop(0)
        while L:
            T=[]
            while L and L[0]:
                T.append(L.pop(0))
            yield T
            while L and not L[0]: L.pop(0)

    def mainText(L):
        """Go through lines, convert to paragraphs."""
        while L:
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

    # no postamble, please
    # for T in ambleText(POSTAMBLE):
    #     E.append([p,'\n'.join(T)])
    del L
    # pp.pprint(E)
    for i in xrange(len(E)):
        E[i][0](*E[i][1:])
    del E
    go()


def run():
    for fn in ('odyssey.full.txt','odyssey.txt'):
        if os.path.isfile(fn):
            parseOdyssey(fn)
            break

def doProf(profname,func,*args,**kwd):
        import hotshot, hotshot.stats
        prof = hotshot.Profile(profname)
        prof.runcall(func)
        prof.close()
        stats = hotshot.stats.load(profname)
        stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats(20)

if __name__=='__main__':
    if '--prof' in sys.argv:
        doProf('dodyssey.prof',run)
    else:
        run()
        