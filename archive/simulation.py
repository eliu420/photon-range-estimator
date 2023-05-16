import data_files
from testing_class import testing
from algorithm_class import range_est
import pandas as pd

summary = pd.DataFrame({
    'File': [],
    'cached_avg': [],
    'Accuracy': []
})
cached_avg = 5
nRuns = 1
for run in data_files.runs_dict.keys():
    print(run)
    df2 = testing().add_variables(data_files.runs_dict[run])
    range_list = []
    for i in range(len(df2)):
        dataStream = testing().parse_csv(df2)
        range_rem = range_est(58).overall_dist_avg(dataStream, cached_avg)
        range_list.append(range_rem)
        cached_avg = range_est(58).update_avg(dataStream, cached_avg, nRuns)
    accuracy = testing().test_accuracy(df2, range_list, 500)
    # print(accuracy, cached_avg)

    summary.loc[len(file_summary.index)] = [
        file, 
        cached_avg,
        accuracy
        ]
    
print(summary)