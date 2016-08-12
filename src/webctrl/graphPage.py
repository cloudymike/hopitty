__author__ = 'mikael'
import matplotlib.pyplot as plt, mpld3
import matplotlib
import commonweb
import sys

matplotlib.use('Agg')

def graphPage(mylog, label1, label2, label3):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.set_title('Temperature')

    ax.set_xlabel('time')
    ax.set_ylabel('temperature')

    bx = fig.add_subplot(111)
    cx = fig.add_subplot(111)

    dx = sorted(mylog)
    d1 = []
    d2 = []
    d3 = []
    for dt in dx:
        status = mylog[dt]
        d1.append(status[label1]['actual'])
        d2.append(status[label2]['actual'])
        d3.append(status[label3]['actual'])

    print sys.getsizeof(mylog)
    dates = matplotlib.dates.date2num(dx)
    ax.plot_date(dates, d1, 'r-', label=label1)
    bx.plot_date(dates, d2, 'b-', label=label2)
    cx.plot_date(dates, d3, 'g-', label=label3)
    plt.legend(bbox_to_anchor=(1, 0.2))

    common = commonweb.commonweb()

    graphpg = mpld3.fig_to_html(fig)

    graphpg = graphpg + common.footer()
    graphpg = graphpg + "</body>"

    return(graphpg)
