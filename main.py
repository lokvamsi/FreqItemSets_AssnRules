#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 11:30:50 2018

@author: kshitij
"""

from itertools import chain,combinations
import collections
from collections import defaultdict
import sys
input = open("groceries.csv","rU")
def getSubsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])

database = []
MIN_SUP = 0.05
MIN_CON = 0.4
RULES = 0 # 0 GIVES FRQ ITEMS AND 1 GIVES RULES


orig_stdout = sys.stdout
if RULES==0:
    f = open('Freq_Items_sup:0.05,conf:0.4.txt','w') 
else:
    f = open('Assn_Rules_sup:0.05,conf:0.4.txt','w')     
sys.stdout = f

for i in input:
    res = i.strip().rstrip(',')
    record = set(res.split(','))
    database.append(record)

#print(len(database))

#
allsupport = collections.Counter(chain.from_iterable(database))

#FOR FREQ ITEM SETS
if RULES==0:
    first=[]
    for i in allsupport.keys():
        supp=allsupport[i]/len(database)
        if supp>=MIN_SUP:
            first.append(i)
            print(i,'(',allsupport[i],')')
    

#iterate through allsupport check min support and add to list
#print frew item set

#allsupport = defaultdict(int)
lstmax = []
for i in allsupport.keys():
    a = []
    a.append(i)
    lstmax.append(a)
    

def genSupport(pairs,minsupport):
    if len(pairs) == 0:
        return None
    global allsupport
    currset = defaultdict(int)
    lst = []
    if len(pairs[0]) > 1:
        #print(pairs)
        for i in pairs:
            for trans in database:
                i = tuple(i)
                if set(i).issubset(trans):
    
                    allsupport[tuple(sorted(i))] += 1
                    currset[i] +=1
    else:
        currset = allsupport

               
    for i in currset.keys():
        support = currset[i]/len(database)
        #print(support)
        if support >= minsupport:
            lst.append(i)
            
    return lst


def joinSet(pairs):
    lst = []
    for a in range(len(pairs)):
        for b in range(a,len(pairs)):
            i = sorted(pairs[a])
            j = sorted(pairs[b])
            if i[:-1] == j[:-1]:
                res = set(i) | set(j)
                if len(res) == len(i)+1:
                    lst.append(list(res))
                    
    return(lst)
                

#a = genSupport(ck,.01)
#print(a)


canidates = genSupport(lstmax,MIN_SUP)
ck = [i for i in combinations(canidates,2)]
ck = genSupport(ck,MIN_SUP)
#print("Starting loop")
freqItems = []

while(ck is not None):
#    print("Iteration next")
#    print(ck)
#    print("Iteration next")
    ans_ck = ck
    freqItems.append(ck)
    canidates = joinSet(ck)
    ck = genSupport(canidates,MIN_SUP)

def get_rules(itemset):
    for itemset in listoflist:
        subset = [i for i in getSubsets(itemset)]
        itemset = set(itemset)
        for item in subset:
            lhs = tuple(itemset.difference(item))
            rhs = item
            if len(lhs) > 0 and len(rhs)>0:
                rule = (lhs, rhs)
                if len(lhs) == 1: 
                    lhs = lhs[0]
                    confidence = allsupport[tuple(sorted(itemset))]/allsupport[lhs]
                else:
                    confidence = allsupport[tuple(sorted(itemset))]/allsupport[tuple(sorted(lhs))]
                if confidence > MIN_CON:
                    #print(allsupport[rule[0][0]])
                    if(allsupport[tuple(sorted(lhs))]):
                        lhscount=allsupport[tuple(sorted(lhs))]
                    else:
                        lhscount=allsupport[lhs]    
                    print(lhs,'(',lhscount,')==>',rhs[0],'(',allsupport[rhs[0]],')-conf(',confidence,')')
#                    print(rule, confidence)

if RULES==1:            
    for listoflist in freqItems:
        get_rules(listoflist)
    
#FOR FREQ ITEM SETS
if RULES==0:
    for i in range(len(freqItems)):
        for j in freqItems[i]:
            print(j,'(',allsupport[tuple(sorted(j))],')')

        

sys.stdout = orig_stdout
f.close()          