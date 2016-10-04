__author__ = 'mikael'
import matplotlib
matplotlib.use('Agg')


import matplotlib.pyplot as plt, mpld3
import commonweb
import sys


def graphPage(mylog, label1, label2, label3, label4):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.set_title('Temperature')

    ax.set_xlabel('time')
    ax.set_ylabel('temperature')

    bx = fig.add_subplot(111)
    cx = fig.add_subplot(111)
    dx = fig.add_subplot(111)

    logdata = sorted(mylog)
    d1 = []
    d2 = []
    d3 = []
    d4 = []
    for dt in logdata:
        status = mylog[dt]
        d1.append(status[label1]['actual'])
        d2.append(status[label2]['actual'])
        d3.append(status[label3]['actual'])
        d4.append(status[label4]['actual'])

    print sys.getsizeof(mylog)
    dates = matplotlib.dates.date2num(logdata)
    ax.plot_date(dates, d1, 'r-', label=label1)
    bx.plot_date(dates, d2, 'b-', label=label2)
    cx.plot_date(dates, d3, 'g-', label=label3)
    dx.plot_date(dates, d4, 'y-', label=label4)
    plt.legend(bbox_to_anchor=(1, 0.3))

    common = commonweb.commonweb()

    graphpg = mpld3.fig_to_html(fig)

    graphpg = graphpg + common.footer()
    graphpg = graphpg + "</body>"

    return(graphpg)
