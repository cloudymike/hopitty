__author__ = 'mikael'
import matplotlib.pyplot as plt, mpld3
import matplotlib
import commonweb
import sys


def graphPage(mylog, label1, label2, label3):
    print mylog
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
        if label2  in status:
            d2.append(status[label2]['actual'])
        else:
            d2.append(0)
        if label3  in status:
            d3.append(status[label3]['actual'])
        else:
            d3.append(0)

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
