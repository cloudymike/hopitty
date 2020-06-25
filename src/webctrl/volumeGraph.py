__author__ = 'mikael'
import matplotlib
matplotlib.use('Agg')


import matplotlib.pyplot as plt, mpld3
import commonweb
import sys


def volumeGraph(mylog, label1, label2,currentRecipeName):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.set_title(currentRecipeName)

    ax.set_xlabel('time')
    ax.set_ylabel('volume')

    bx = fig.add_subplot(111)

    logdata = sorted(mylog)
    d1 = []
    d2 = []
    for dt in logdata:
        status = mylog[dt]
        d1.append(status[label1]['actual'])
        d2.append(status[label2]['actual'])

    #print sys.getsizeof(mylog)
    dates = matplotlib.dates.date2num(logdata)
    ax.plot_date(dates, d1, 'r-', label=label1)
    bx.plot_date(dates, d2, 'b-', label=label2)
    plt.legend(bbox_to_anchor=(1, 0.3))

    common = commonweb.commonweb()

    graphpg = mpld3.fig_to_html(fig)

    graphpg = graphpg + common.footer()
    graphpg = graphpg + "</body>"
    graphpg = common.header("Volume", True) + graphpg

    return(graphpg)
