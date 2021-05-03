import os
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4


def make_report(system_name):
    c = canvas.Canvas('_'.join([system_name, 'report.pdf']), pagesize=A4)

    # pie chart
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'pie.svg'])))
    sx = sy = 0.9
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 125, 450
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    # # WLT vs. Sessions chart
    # drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'wlt_vs_sessions.svg'])))
    # sx = sy = 0.7
    # drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    # drawing.scale(sx, sy)
    # x, y = 120, 350
    # renderPDF.draw(drawing, c, x, y, showBoundary=False)

    # WLT vs. Sessions chart (with outcomes)
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'wlt_vs_sessions_outcome.svg'])))
    sx = sy = 0.9
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 50, 50
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    c.showPage()

    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'clicks.svg'])))
    drawing.rotate(-90)
    sx = sy = 0.6
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 40, 750  # coordinates (from left bottom)
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'sessions_vs_impressions.svg'])))
    drawing.rotate(-90)
    sx = sy = 0.6
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 320, 750  # coordinates (from left bottom)
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    c.save()


if __name__ == '__main__':
    make_report('gesis_rec_pyterrier')