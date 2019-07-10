import csv
import numpy as np
import matplotlib.pyplot as plt

def plot(array):
    print('plotting histogram for match percentages')
    print('close plot to see stats')
    plt.title('match percentages')
    plt.xlabel('match percentages')
    plt.ylabel('number of clusters')
    ticks = [0,10,20,30,40,50,60,70,80,90,100]
    plt.xticks(ticks)
    s = ('total number of clusters: '+str(len(total_summaries))+
        '\nnumber of valid clusters: '+str(good_clusters)+
        '\naverage number of summaries per cluster: '+str(avg_num_summaries)+
        '\nnumber of removed clusters: '+str(removed)+
        '\nmean: '+str(avg_match_percent)+
        '\nmedian: '+str(np.median(match_percents))+
        '\nstd dev: '+str(np.std(match_percents)))
    plt.text(-4,7,s)
    plt.hist(array, bins=ticks)
    plt.savefig('../clustering/match_percentages.png')
    plt.show()

if __name__ == '__main__':
    with open('../clustering/sample_cluster_analysis.csv') as f:
        reader = csv.DictReader(f)

        total_summaries = []
        match_percents = []
        good_clusters = 0
        removed = 0

        for row in reader:
            total_summaries.append(row['num_summaries'])
            if row['quit'] != 'Y':
                match_percents.append(row['match_percents'])
            else:
                removed += 1
            if row['clustered_yn'] == 'yes':
                good_clusters += 1
        match_percents = np.array(match_percents).astype(np.float)
        total_summaries = np.array(total_summaries).astype(np.float)

        avg_match_percent = np.mean(match_percents)
        avg_num_summaries = np.mean(total_summaries)

        print('total number of clusters: '+str(len(total_summaries)))
        print('number of valid clusters: '+str(good_clusters))
        print('average number of summaries per cluster: '+str(avg_num_summaries))
        plot(match_percents, 'match percentages')
        print('mean: '+str(avg_match_percent)+'\nmedian: '+str(np.median(match_percents))+
            '\nstd dev: '+str(np.std(match_percents)))
