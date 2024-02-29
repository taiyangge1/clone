import pandas as pd
import torch
from torch.nn.utils.rnn import pad_sequence
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



#导入数据集，文件目录记得改
# Load your dataset
df = pd.read_excel(r"C:\Users\24766\Desktop\Wimbledon_featured_matches.xlsx")


#这里是数据预处理，首先把字符串改成数字，然后剔除偏差大的值，按照match_id分组，每一组的缺失值用本组的中位数补齐，若整租都没数据（比如某场比赛一列全是0，就用该列的中位数补齐）
# -------------------------------------------------------------------
# Convert the traditional tennis scores to continuous numbers
score_mapping = {0: 0, 15: 1, 30: 2, 40: 3, 'AD': 4}
df['p1_score'] = df['p1_score'].map(score_mapping).fillna(df['p1_score'])
df['p2_score'] = df['p2_score'].map(score_mapping).fillna(df['p2_score'])

# Convert 'winner_shot_type' from 'F', 'B' to 1, 2
shot_type_mapping = {'F': 1, 'B': 2}
df['winner_shot_type'] = df['winner_shot_type'].map(shot_type_mapping).fillna(df['winner_shot_type'])

# Choose the right features
features_to_scale = [
    "p1_unf_err",  # player 1 made an unforced error
    "p2_unf_err",  # player 2 made an unforced error
    "p1_double_fault",  # player 1 missed both serves and lost the point
    "p2_double_fault",  # player 2 missed both serves and lost the point
    "p1_sets",  # sets won by player 1
    "p2_sets",  # sets won by player 2
    "p1_games",  # games won by player 1 in current set
    "p2_games",  # games won by player 2 in current set
    "p1_score",  # player 1's score within current game
    "p2_score",  # player 2's score within current game
    "server",  # server of the point
    "serve_no",  # first or second serve
    "p1_winner",  # player 1 hit an untouchable winning shot
    "p2_winner",  # player 2 hit an untouchable winning shot
    #"speed_mph",  # speed of serve (miles per hour; mph)
    "p1_distance_run",  # player 1's distance ran during point (meters)
    "p2_distance_run",  # player 2's distance ran during point (meters)
    "rally_count",  # number of shots during the point
    "p1_ace",  # player 1 hit an untouchable winning serve
    "p2_ace",  # player 2 hit an untouchable winning serve
]

columns_to_keep = ['match_id', 'elapsed_time'] + features_to_scale
df_subset = df[columns_to_keep]

# -------------------------------------------------------------------
# Function to replace outliers with the group's median
def replace_outliers_with_median(group, features):
    for feature in features:
        Q1 = group[feature].quantile(0.25)
        Q3 = group[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        median = group[feature].median()
        group[feature] = group[feature].apply(lambda x: median if x < lower_bound or x > upper_bound else x)
    return group

# Apply the function to each match_id group
df_processed = df.groupby('match_id').apply(lambda group: replace_outliers_with_median(group, features_to_scale))


# Function to fill missing values with the median and scale features for each group
df_median = df[features_to_scale].median()

def process_group(group):
    # 对于每个特征列
    for column in features_to_scale:
        # 如果整个组的该列都是缺失值
        if group[column].isnull().all():
            # 使用整个DataFrame该列的中位数来填充
            group[column].fillna(df_median[column], inplace=True)
        # 如果不是整个组都缺失，但有缺失值
        elif group[column].isnull().any():
            # 使用组内的中位数来填充
            group[column].fillna(group[column].median(), inplace=True)
    # 标准化特征
    scaler = StandardScaler()
    group[features_to_scale] = scaler.fit_transform(group[features_to_scale])
    return group

# Apply the function to each match_id group
df_subset_processed = df_subset.groupby('match_id').apply(process_group)
df_subset_processed.reset_index(drop=True, inplace=True)

# Determine which player wins the game
def determine_winner(group):
    final_state = group.iloc[-1]
    if final_state['p1_sets'] > final_state['p2_sets']:
        group['winner'] = 0
    elif final_state['p1_sets'] < final_state['p2_sets']:
        group['winner'] = 1
    else:
        if final_state['p1_games'] > final_state['p2_games']:
            group['winner'] = 0
        elif final_state['p1_games'] < final_state['p2_games']:
            group['winner'] = 1
        else:
            if final_state['p1_score'] > final_state['p2_score']:
                group['winner'] = 0
            else:
                group['winner'] = 1
    return group

df = df_subset_processed.groupby('match_id').apply(determine_winner)
df['winner'] = df['winner'].astype(int)
# -------------------------------------------------------------------

#现在是SVC向量机预测数据，根据已选的特征预测双方选手每场比赛中（match），各个赢球（得分时间点）的胜率，效果比随机森林好
# -------------------------------------------------------------------
# Determine which player wins the game
def determine_winner(group):
    final_state = group.iloc[-1]
    if final_state['p1_sets'] > final_state['p2_sets']:
        group['winner'] = 0
    elif final_state['p1_sets'] < final_state['p2_sets']:
        group['winner'] = 1
    else:
        if final_state['p1_games'] > final_state['p2_games']:
            group['winner'] = 0
        elif final_state['p1_games'] < final_state['p2_games']:
            group['winner'] = 1
        else:
            if final_state['p1_score'] > final_state['p2_score']:
                group['winner'] = 0
            else:
                group['winner'] = 1
    return group

df = df_subset_processed.groupby('match_id').apply(determine_winner)
df['winner'] = df['winner'].astype(int)
# -------------------------------------------------------------------
# 重置索引，确保match_id和elapsed_time作为列存在
df_reset = df.reset_index(drop=True)

# 分割数据集之前，保留elapsed_time的值
X = df[[
    "match_id", "elapsed_time", "p1_unf_err", "p2_unf_err", "p1_double_fault", "p2_double_fault",
    "p1_sets", "p2_sets", "p1_games", "p2_games", "p1_score", "p2_score", "server", "serve_no",
    "p1_winner", "p2_winner", "p1_distance_run", "p2_distance_run", "rally_count", "p1_ace", "p2_ace",
]]
y = df['winner']

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 从 X_train 和 X_test 中分离出 match_id，然后将它们分别存储
train_match_id = X_train['match_id']
test_match_id = X_test['match_id']
train_elapsed_time=X_train['elapsed_time']
test_elapsed_time=X_test['elapsed_time']

X_train = X_train.drop(columns=['match_id', 'elapsed_time'])
X_test = X_test.drop(columns=['match_id', 'elapsed_time'])

# 特征缩放
scaler = StandardScaler()
# 假设这里的X_train和X_test已经不包含'match_id'和'elapsed_time'
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 初始化SVM分类器
svc = SVC(probability=True, kernel='rbf', C=1.0, gamma='auto')

# 训练模型
svc.fit(X_train_scaled, y_train)

# 进行预测
y_pred_proba = svc.predict_proba(X_test_scaled)

# 获取类别为1的预测概率作为player1的胜率，类别为0的预测概率作为player2的胜率
player1_win_rate = y_pred_proba[:, 1]
player2_win_rate = y_pred_proba[:, 0]

# 之前保存的match_id和elapsed_time需要这样添加回df_final
df_final = pd.DataFrame(X_test_scaled, columns=X_train.columns)  # 假设X_train.columns已经不包含被删除的列
df_final['player1_win_rate'] = player1_win_rate
df_final['player2_win_rate'] = player2_win_rate
df_final['match_id'] = test_match_id.values  # 直接使用.values获取之前保存的numpy数组
df_final['elapsed_time'] = test_elapsed_time.values  # 同上

# 保存到Excel
print(df_final.head())
df_final.to_excel(r"C:\Users\24766\Desktop\final_Wimbledon_featured_matches_with_win_rate.xlsx", index=False)
# -------------------------------------------------------------------

#这是画图，按照match_id分组，每场分别画图

# -------------------------------------------------------------------
unique_match_ids = df_final['match_id'].unique()
df_final['elapsed_time_in_minutes'] = df_final['elapsed_time'].apply(lambda x: x.hour * 60 + x.minute)

# 确保数据按转换后的时间排序并且已经创建了 elapsed_time_in_minutes 列
for match_id in unique_match_ids:
    match_data = df_final[df_final['match_id'] == match_id]
    match_data = match_data.sort_values(by='elapsed_time_in_minutes')

    # 设置图形大小
    plt.figure(figsize=(12, 8))

    # 获取x轴的标签
    x_labels = match_data['elapsed_time_in_minutes'].values

    # 获取选手1和选手2胜率的数据
    player1_rates = match_data['player1_win_rate'].values
    player2_rates = match_data['player2_win_rate'].values

    # 绘制堆叠柱状图
    plt.bar(x_labels, player1_rates, color='blue', width=0.4, label='Player 1 Win Rate')
    plt.bar(x_labels, player2_rates, bottom=player1_rates, color='yellow', width=0.4, label='Player 2 Win Rate')

    # 绘制选手1胜率的顶部边界作为折线图
    plt.plot(x_labels, player1_rates, color='black', marker='o', linestyle='-', linewidth=2, markersize=5,
             label='Player 1 Win Rate Boundary')

    # 添加图例
    plt.legend()

    # 添加标题和轴标签
    plt.title(f'Win Rate Comparison Over Time for Match ID {match_id}')
    plt.xlabel('Elapsed Time (minutes)')
    plt.ylabel('Win Rate')

    # 显示图形
    plt.show()

# -------------------------------------------------------------------
#创建时间序列，以从得分时刻及其前面的所有时刻的数据作为输入，以0作为填充保证序列形状的一致性
# -------------------------------------------------------------------
sequences = []  # 用于存储每个序列的列表
win_rates = []  # 用于存储每个序列对应的胜率标签的列表

for match_id in df_final['match_id'].unique():
    match_data = df_final[df_final['match_id'] == match_id]
    for end_index in range(1, len(match_data) + 1):
        # 获取序列数据
        seq = match_data.iloc[:end_index][[
            "p1_unf_err", "p2_unf_err", "p1_double_fault", "p2_double_fault",
            "p1_sets", "p2_sets", "p1_games", "p2_games",
            "p1_score", "p2_score", "server", "serve_no",
            "p1_winner", "p2_winner", "p1_distance_run",
            "p2_distance_run", "rally_count", "p1_ace", "p2_ace", 'player1_win_rate', 'player2_win_rate'
        ]].values
        sequences.append(torch.tensor(seq, dtype=torch.float))

        # 获取该序列最后一个时间点的胜率
        last_point_win_rate = match_data.iloc[end_index - 1][['player1_win_rate', 'player2_win_rate']].values.astype(
            np.float32)
        win_rates.append(torch.tensor(last_point_win_rate, dtype=torch.float))

# 使用pad_sequence对序列进行填充，以便它们具有相同的长度
padded_sequences = pad_sequence(sequences, batch_first=True, padding_value=0)
# 将胜率列表转换为Tensor
win_rates_tensor = torch.stack(win_rates)

print("Padded sequences shape:", padded_sequences.shape)
print("Win rates tensor shape:", win_rates_tensor.shape)

# -------------------------------------------------------------------
#构建lstm模型
# -------------------------------------------------------------------
class MatchPredictionLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim=2, num_layers=1):
        super(MatchPredictionLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.linear(out[:, -1, :])  # 只取最后一个时间步的输出
        return out


# 实例化模型、损失函数和优化器
model = MatchPredictionLSTM(input_dim, hidden_dim).to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

# 训练模型
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()

    outputs = model(padded_sequences)
    loss = criterion(outputs, win_rates_tensor)  # 确保win_rates_tensor形状与outputs匹配

    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# -------------------------------------------------------------------
#推理
# -------------------------------------------------------------------
# 使用pad_sequence来确保所有序列长度一致
padded_sequences = pad_sequence(sequences, batch_first=True)

# 模型预测
model.eval()
with torch.no_grad():
    predictions = model(padded_sequences)

# 可视化每场比赛的胜率随时间的变化
for i, match_id in enumerate(df_final['match_id'].unique()):
    pred = predictions[i].cpu().numpy()
    times = np.arange(pred.shape[0])
    plt.figure(figsize=(10, 6))
    plt.plot(times, pred, label='Player 1 Win Rate', color='yellow')
    plt.xlabel('Time Step')
    plt.ylabel('Win Rate')
    plt.title(f'Win Rate Over Time (Match ID: {match_id})')
    plt.legend()
    plt.show()