__author__ = 'mikael'
import matplotlib.pyplot as plt, mpld3
import matplotlib
import commonweb
import sys


def graphPage(mylog, label1, label2):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.set_title('Temperature')

    ax.set_xlabel('time')
    ax.set_ylabel('temperature')

    bx = fig.add_subplot(111)

    dx = sorted(mylog)
    dy = []
    dz = []
    for dt in dx:
        status = mylog[dt]
        dy.append(status[label1]['actual'])
        dz.append(status[label2]['actual'])

    print sys.getsizeof(mylog)
    dates = matplotlib.dates.date2num(dx)
    ax.plot_date(dates, dy, 'r-', label=label1)
    bx.plot_date(dates, dz, 'b-', label=label2)
    plt.legend()

    common = commonweb.commonweb()

    graphpg = mpld3.fig_to_html(fig)

    graphpg = graphpg + common.footer()
    graphpg = graphpg + "</body>"

    return(graphpg)
