import csv
import sys
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from tqdm import tqdm
from rouge_analysis import rouge
from sms_analysis import wsms
from wmd_analysis import wmd

def find_pos_neg(pos_matrix, threshold_matrix):
    """Returns the number of true positives, false positives, true negatives, and false negatives."""

    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for x in range(len(pos_matrix)):
        for y in range(len(pos_matrix)):
            true_value = pos_matrix[x][y]
            if true_value == threshold_matrix[x][y]:
                if true_value == 1:
                    TP += 1
                else:
                    TN += 1
            else:
                if true_value == 0:
                    FP += 1
                else:
                    FN += 1

    return TP, FP, TN, FN

def threshold_matrix(threshold, score_matrix):
    """Returns a matrix indicating which pairs are good according to the given threshold"""

    matrix = []
    for row in score_matrix:
        scores = []
        for entry in row:
            if entry >= threshold:
                scores.append(1)
            else:
                scores.append(0)
        matrix.append(scores)

    return matrix

def precision(TP,FP):
    if TP == 0 and FP == 0:
        return 1
    return TP/(TP+FP)

def recall(TP,FN):
    return TP/(TP+FN)

def F1(precision, recall):
    return 2*((precision*recall)/(precision+recall))

def precision_recall_curve(cluster, score_matrix, thresholds, name):
    """Creates precision-recall curve and saves it to the data folder"""
    precisions = []
    recalls = []
    for threshold in thresholds:
        tm = threshold_matrix(threshold, score_matrix)
        TP, FP, TN, FN = find_pos_neg(true_matrices[cluster], tm)
        p = precision(TP,FP)
        precisions.append(p)
        r = recall(TP,FN)
        recalls.append(r)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.plot(recalls, precisions)
    plt.savefig('../data/'+name+'_prcurve_'+cluster+'.png')

def threshold_chart(cluster, score_matrix, thresholds, name):
    """Creates a csv file that has the TP, FP, TN, FN, precision and recall values
    for each threshold. Saves to data folder."""

    with open('../data/'+name+'_threshold_'+cluster+'.csv', 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['threshold','TP','FP','TN','FN','precision','recall'])
        for threshold in thresholds:
            tm = threshold_matrix(threshold, score_matrix)
            TP, FP, TN, FN = find_pos_neg(true_matrices[cluster], tm)
            p = precision(TP,FP)
            r = recall(TP,FN)
            writer.writerow([threshold,TP,FP,TN,FN,p,r])

def main(metric):
    plt.clf()
    #thresholds = np.linspace(0,1,21)
    thresholds = np.linspace(0,0.5,11)
    #thresholds = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09, 0.1]
    #thresholds = [0.76,0.78,0.8,0.82,0.84,0.86,0.88,0.9,0.92,0.94,0.96,0.98,1.0]
    precisions = []
    recalls = []
    with open('../data/'+metric+'_threshold_full.csv', 'w+') as csvfile: #switch here
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['threshold','TP','FP','TN','FN','precision','recall'])
        for threshold in thresholds:
            TPs = 0
            FPs = 0
            TNs = 0
            FNs = 0
            for key in clusters:
                if metric == 'wsms':
                    matrix = wsms(key)
                elif metric == 'rouge1':
                    matrix, a, b = rouge(clusters[key])
                elif metric == 'rouge2':
                    a, matrix, b = rouge(clusters[key])
                elif metric == 'rougel':
                    a, b, matrix = rouge(clusters[key])
                else: # metric == 'wmd':
                    matrix = wmd(clusters[key])
                tm = threshold_matrix(threshold, matrix)
                TP, FP, TN, FN = find_pos_neg(true_matrices[key], tm)
                TPs += TP
                FPs += FP
                TNs += TN
                FNs += FN
            p = precision(TPs,FPs)
            precisions.append(p)
            r = recall(TPs,FNs)
            recalls.append(r)
            writer.writerow([threshold,TPs,FPs,TNs,FNs,p,r])
    plt.title(metric)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.plot(recalls, precisions)
    plt.text(1.5,1, str(metrics.auc(recalls, precisions)))
    plt.savefig('../data/'+metric+'_full_prcurve.png') #switch here
    print(metrics.auc(recalls, precisions))

true_matrices = {
'sandy':[
    [1,0,1,1,1,0],
    [1,1,0,0,1,0],
    [0,1,1,1,0,0],
    [0,0,0,1,0,1],
    [1,1,1,0,1,0],
    [0,0,1,0,1,1]
],
'orlando':[
    [1,0,1,1,0,0,0,0,0,0,0],
    [1,1,0,1,0,0,1,1,1,0,0],
    [0,1,1,1,0,0,1,1,0,0,0],
    [1,0,1,1,1,0,0,1,1,1,1],
    [1,0,1,1,1,0,0,1,1,0,0],
    [0,1,0,1,1,1,0,0,1,0,0],
    [1,0,1,1,1,0,1,1,0,0,0],
    [1,0,1,1,1,0,0,1,1,1,1],
    [0,0,0,1,0,0,0,0,1,0,0],
    [1,0,1,1,1,0,0,1,1,1,1],
    [1,0,1,0,0,0,0,0,0,1,1]
],
'mandela':[
    [1,0,1,0,0,0,0,0,1],
    [0,1,1,0,0,0,0,0,0],
    [1,0,1,0,0,0,0,0,0],
    [1,0,1,1,0,0,1,1,0],
    [1,0,1,0,1,1,1,1,1],
    [1,0,1,0,0,1,1,1,0],
    [0,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,1]
],
'boston':[
    [1,1,0,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1]
]}

clusters = {
'sandy':[
"After Sandy hit the East Coast Monday night, more than 2 million New Jersey residents were left without power and feeling powerless",
"Superstorm Sandy crashed ashore this week, cutting a path of destruction several hundred miles long. Here are some numbers that help put it in perspective.",
"Hurricane Sandy struck the Northeast hard when it made landfall in New Jersey Tuesday night. New York Magazine's cover reflects the damage.",
"Hurricane Sandy is poised to become an “unprecedented” superstorm that could leave millions of people in the Northeast without power for days or even weeks, experts said Saturday.",
"One of the largest and fiercest storms to menace the East Coast in years caused widespread flooding, power outages and damage. At least 16 have died, AP reports.",
"The hurricane continued its march north, with powerful winds already affecting the region on Sunday and landfall expected on Monday or Tuesday.",
],
'orlando':[
"A shooting at a gay nightclub in Orlando killed at least 50 people on Sunday, June 12. Orlando police said they shot and killed the gunman.",
"Approximately 20 people have died after an attacker opened fire inside a gay nightclub in the Florida city of Orlando, police say.",
"Officials say at least 49 people were killed and dozens were injured in the shooting.",
"A terrorist opened fire inside a popular Orlando gay club near closing time early Sunday.",
"At least 42 people were taken to hospitals with injuries, police said. The shooter was killed in an exchange of gunfire with police.",
"Police in the US city of Orlando are telling people to stay away from a gay nightclub where a shooting has broken out and people are injured.'",
"Unconfirmed reports have emerged of a shooting at a nightclub in Orlando, Florida.'",
"At least 50 people are dead and dozens injured after a gunman opened fire at a gay nightclub in Orlando. What exactly happened?'",
"For three harrowing hours, as Omar Mateen carried out his rampage inside the Pulse nightclub in Orlando, clubgoers hid in bathrooms, in air-conditioning vents, under tables.'",
"It's the worst terror attack on American soil since 9/11, and the deadliest mass shooting in U.S. history.'",
"The gun massacre Sunday at an Orlando nightclub is the worst in the history of the U.S., where mass shootings are frighteningly common.'",
],
'mandela':[
"Nelson Mandela, who rose from militant antiapartheid activist to become the unifying president of a democratic South Africa and a global symbol of racial reconciliation, died at his Johannesburg home on Thursday. He was 95.",
"He was the country’s most potent symbol of unity, using the power of forgiveness and reconciliation.",
"The South African leader, who passionately fought apartheid, dies at age 95",
"Nelson Mandela, the anti-apartheid crusader and former South African president, died Dec. 5 at 95. We’re bringing you live updates here.",
"In a symbol befitting a nation in mourning, a dark gray cloud swept over Johannesburg on Friday as news spread that Nelson Mandela is dead.",
"The people of South Africa reacted Friday with deep sadness at the loss of a man considered by many to be the father of the nation, while mourners said it was also a time to celebrate the achievements of the anti-apartheid leader who emerged from prison to become South Africa's first black president.",
"When Nelson Mandela died on Thursday, people around the globe gathered to memorialize the man widely recognized as a beacon of courage, hope and freedom.",
"Mandela transformed his nation from oppressive regime to one of the most inclusive democracies on the planet.",
"In an extraordinary life that spanned the rural hills where he was groomed for tribal leadership, anti-apartheid activism, guerrilla warfare, 27 years of political imprisonment and, ultimately, the South African presidency, Mandela held a unique cachet that engendered respect and awe in capitals around the globe.'",
],
'boston':[
"At least two dead and dozens injured when bombs go off near finish line.",
"Two explosions rocked the finish line at the Boston Marathon on Monday, killing three and wounding at least 144 people",
"Pressure cookers are believed to have been used to make the crude bombs that sent torrents of deadly shrapnel hurling into a crowd of onlookers and competitors at Monday’s Boston Marathon, experts told Fox News",
"Two deadly bomb blasts, seconds apart, turned the 117th Boston Marathon – the nation’s premier event for elite and recreational runners – into a tragedy on Monday. Here is a timeline of how the day’s events unfolded: 9 a.m. ET — Race …",
"When two bombs detonated in the final stretch of the Boston Marathon on Monday afternoon, runners, spectators and people across the country and around the world were stunned by the public nature of",
"Mayhem descended on the Boston marathon Monday afternoon, when an explosion at the finish line killed at least two and injured at least 23. TIME is tracking the breaking news from the scene in downtown Boston. Follow here for constant updates. 5:45 p.m.",
"Two bombs exploded in the packed streets near the finish line of the Boston Marathon on Monday, killing two people and injuring more than 100 in a terrifying scene of shattered glass, billowing smoke, bloodstained pavement and severed limbs, authorities said",
"Blasts near the finish line of the renowned race caused dozens of injuries and scattered crowds.",
"Two deadly explosions brought the Boston Marathon and much of this city to a chaotic halt Monday, killing at least three people, injuring about 140 and once again raising the specter of terrorism on American soil.",
]}

if __name__ == '__main__':
    metric = sys.argv[1]
    assert metric in ['wsms','wmd','rouge1','rouge2','rougel'], 'You did not enter a valid metric.'
    main(metric)
