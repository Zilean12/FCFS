import pandas

df = pandas.read_csv('text.txt', sep=' ', header=None, names=['Process', 'arrival_time', 'burst_time'])

Start_process = df['Process'][df['arrival_time'] == 0].min() 
if pandas.isna(Start_process):
    Start_process = df['Process'].min()

df = df.sort_values(by=['arrival_time', 'Process'])

ct = df['burst_time'].iloc[0] if Start_process == df['Process'].iloc[0] else 0
TAT = [ct - df['arrival_time'].iloc[0]]

WT = [TAT[0] - df['burst_time'].iloc[0]]
for K in range(1, len(df)):
    if df['Process'].iloc[K] == Start_process:
        ct = df['burst_time'].iloc[K]
    else:
        if df['arrival_time'].iloc[K] > ct:
            ct = df['arrival_time'].iloc[K] + df['burst_time'].iloc[K]
        else:
            ct += df['burst_time'].iloc[K]
    TAT.append(ct - df['arrival_time'].iloc[K])
    WT.append(TAT[-1] - df['burst_time'].iloc[K])

df['CT'] = ct
df['TAT'] = TAT
df['WT'] = WT
df['rt'] = df['WT'].where(df['WT'] > 0, 0)

df['RD'] = df['rt'] / df['burst_time']


Gantt = ''  
C = 0      
for K, row in df.iterrows():
    if row['Process'] == Start_process:
        Gantt += f'Process{row["Process"]}|{row["burst_time"] + C}|'
        C += row['burst_time']
    else:
        if row['arrival_time'] > C:
            Gantt += f'Idle|{row["arrival_time"]}|Process{row["Process"]}|{row["burst_time"] + row["arrival_time"]}|'
            C = row['burst_time'] + row['arrival_time']
        else:
            Gantt += f'Process{row["Process"]}|{row["burst_time"] + C}|'
            C += row['burst_time']


# print("Gantt Chart")
# print(Gantt)
print(df.drop(columns='CT').to_string(index=False))
# print(f'Avg Waiting Time: {df["WT"].mean():.2f}')
# print(f'Avg Turn Around Time: {df["TAT"].mean():.3f}')
# print(f'Avg Response Time: {df["rt"].mean():.2f}')
# print(f'Avg Response Delay: {df["RD"].mean():.3f}')

