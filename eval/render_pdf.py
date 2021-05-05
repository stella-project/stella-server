from db import *
from util import *
from config import *
import pandas as pd
import os
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table


def make_report(system_name):

    overall_stats = pd.read_csv('results/overall_stats.csv', index_col=0)

    c = canvas.Canvas(os.path.join('results', '_'.join([system_name, 'report.pdf'])), pagesize=A4)

    # pie chart
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'pie.svg'])))
    sx = sy = 0.9
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 125, 450
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    # WLT vs. Time chart
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'wlt_vs_time.svg'])))
    sx = sy = 0.9
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 75, 75
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    c.showPage()


    # WLT vs. Time chart (with outcomes)
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'wlt_vs_time_outcome.svg'])))
    sx = sy = 0.9
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 50, 425
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    # WLT vs. Sessions chart (with outcomes)
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'wlt_vs_sessions_outcome.svg'])))
    sx = sy = 0.9
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 50, 50
    renderPDF.draw(drawing, c, x, y, showBoundary=False)


    c.showPage()

    # Clicks
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'clicks.svg'])))
    drawing.rotate(-90)
    sx = sy = 0.6
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 40, 750  # coordinates (from left bottom)
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    # Sessions vs. Impressions
    drawing = svg2rlg(os.path.join('results', '_'.join([system_name, 'sessions_vs_impressions.svg'])))
    drawing.rotate(-90)
    sx = sy = 0.6
    drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
    drawing.scale(sx, sy)
    x, y = 320, 750  # coordinates (from left bottom)
    renderPDF.draw(drawing, c, x, y, showBoundary=False)

    c.showPage()

    data = [('System', system_name),
            (' ', ' ', ' '),
            ('Metric', 'Value', 'Description'),
            ('Win', int(overall_stats.loc[system_name]['Win']), 'A system "wins" if it has more clicks on results assigned to it \nby the interleaving than clicks on results by the baseline system.'),
            ('Loss', int(overall_stats.loc[system_name]['Loss']), 'Opposite of Win, i.e. number of times when the system has \nless clicks on results than the baseline system.'),
            ('Tie', int(overall_stats.loc[system_name]['Tie']), 'Equal number of clicks for your system and the baseline. \nOnly results having at least two clicks are included.'),
            ('Outcome', "{:1.4f}".format(overall_stats.loc[system_name]['Outcome']), '#Wins / (#Wins + #Loss)'),
            ('Sessions', int(overall_stats.loc[system_name]['Sessions']), 'Total number of sessions for which your system was used.'),
            ('Impressions', int(overall_stats.loc[system_name]['Impressions']), 'Total number of results for which your system was used.'),
            ('Clicks', int(overall_stats.loc[system_name]['Clicks']), 'Total number of clicks your system received.'),
            ('CTR', "{:1.4f}".format(overall_stats.loc[system_name]['CTR']), 'Click-through rate')]
    table = Table(data)
    table.wrapOn(c, 100, 100)
    table.drawOn(c, 80, 500)

    c.save()


if __name__ == '__main__':
    for system in systems.select().where(not_(systems.c.name.in_(NOT_PARTICIPATED))).execute().fetchall():
        make_report(system.name)