#!/usr/bin/env python

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import matplotlib.cbook as cbook

#from matplotlib import pyplot as plt
from matplotlib.dates import date2num

from statsmodels.distributions.empirical_distribution import ECDF

from collections import Counter

import pandas as pd

from ..guifiwrapper.guifiwrapper import *

#root = 3671
root = 2444
g = CNMLWrapper(root)


def nodeDegreeECDF():
    nodeD = [n.totalLinks for n in g.nodes.values()]
    counter = Counter(nodeD).items()
    print counter
    ecdf = ECDF(nodeD)
    print ecdf
    # Initilaze figure to print later
    fig = plt.Figure()
    fig.set_canvas(plt.gcf().canvas)
    plt.plot(ecdf.x, ecdf.y)
    # Set graph parameters
    plt.title("Node Degree ECDF")
    plt.ylabel("Frequency")
    plt.xlabel("Node Degree")
    plt.xlim(-1,50)
    plt.show()
    # Print to PDF
    figfile = os.path.join(os.getcwd(),'figs',str(root)+"_node_degree_ECDF")
    fig.savefig(figfile, format='png')


def totalLinksFrequencies():
    totalLinks = len(g.totallinks)
    ap = [0 for n in g.totallinks.values() if n.type == "ap/client"]
    totalAp = len(ap)
    wds = [0 for n in g.totallinks.values() if n.type == "wds"]
    totalWds = len(wds)
    #intraLinks = [l for l in g.totallinks.values() if l.nodeA.parentZone.id == l.nodeB.parentZone.id]
    #totalIntraLinks = len(intraLinks)

    totalWorkingLinks = len(g.links) #no self-links
    workingAp = [0 for n in g.links.values() if n.type == "ap/client"]
    totalWorkingAp = len(workingAp)
    workingWds = [0 for n in g.links.values() if n.type == "wds"]
    totalWorkingWds = len(workingWds)

    workingIntraLinks = [l for l in g.links.values() if l.nodeA.parentZone.id == l.nodeB.parentZone.id]
    totalWorkingIntraLinks = len(workingIntraLinks)
    workingIntraAp = [0 for n in workingIntraLinks if n.type == "ap/client"]
    totalWorkingIntraAp = len(workingIntraAp)
    workingIntraWds = [0 for n in workingIntraLinks if n.type == "wds"]
    totalWorkingIntraWds = len(workingIntraWds)

    types = ('Total','Total\nWorking','Total\nWorking\nIntrazone')
    values = (totalLinks, totalWorkingLinks, totalWorkingIntraLinks)

    typesAp = ('Total AP','Total AP\nWorking','Total AP\nWorking\nIntrazone')
    valuesAp = (totalAp, totalWorkingAp, totalWorkingIntraAp)

    typesWds = ('Total WDS','Total WDS\nWorking','Total WDS\nWorking\nIntrazone')
    valuesWds = (totalWds, totalWorkingWds, totalWorkingIntraWds)


    ind = np.arange(3)
    width = 0.25


    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, values, width, color='black')
    rects2 = ax.bar(ind+width, valuesAp, width, color='blue')
    rects3 = ax.bar(ind+2*width, valuesWds, width, color='red')

    ax.legend((rects1[0], rects2[0], rects3[0]), ('Overall', 'AP/client','WDS'))

    ax.set_xlim(-width,len(ind)+width)
    #ax.set_ylim(0,45)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('links')
    ax.set_title(g.zone.title+' Links Frequency')
    xTickMarks = [str(i) for i in types]
    ax.set_xticks(ind+3*width/2)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=10)
    plt.show()
    #figfile = os.path.join(os.getcwd(),'figs','links',str(root)+"_links_frequency")
    #fig.savefig(figfile, format='png')


def linkTypesFrequencies():
    linkTypes = [n.type for n in g.links.values() ]
    totalNodes = len(linkTypes)
    linkTypes = Counter(linkTypes).items()
    linkTypesNumber = len(linkTypes)
    types = [typ for (typ,values) in linkTypes]
    values = [float(value)/float(totalNodes) for (typ,value) in linkTypes]

    ind = np.arange(linkTypesNumber)
    width = 0.35


    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects = ax.bar(ind,values, width, color='black')
    ax.set_xlim(-width,len(ind)+width)
    #ax.set_ylim(0,45)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Node Type')
    ax.set_title(g.zone.title+' Node Types Frequency')
    xTickMarks = [str(i) for i in types]
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=10)
    plt.show()
    #figfile = os.path.join(os.getcwd(),'figs','links',str(root)+"_link_types_frequency.png")
    #fig.savefig(figfile, format='png')




if __name__ == "__main__":
    import os
    basedir = os.path.join(os.getcwd(),'figs')
    figslinksdir = os.path.join(basedir,'figs','links')
    for d in [figsdir,figslinksdir]:
        if not os.path.exists(d):
            os.makedirs(d)

    #nodeDegreeECDF()
    totalLinksFrequencies()
    #linkTypesFrequencies()
