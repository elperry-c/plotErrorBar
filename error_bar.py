import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
import datetime as dt

# 年月日時分秒を2桁ずつ
def output_datetime():
    d = dt.datetime.now()
    return d.strftime('%y%m%d%H%M%S')


#plt.rcParams['font.family'] = 'Yu Gothic'
plt.rcParams['xtick.direction'] = 'out'#x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'out'#y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.major.width'] = 1#x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1#y軸主目盛り線の線幅
plt.rcParams['font.size'] = 28 #フォントの大きさ
# plt.rcParams['axes.linewidth'] = 0.8# 軸の線幅edge linewidth。囲みの太さ

# 実行ファイルのあるディレクトリまでのパス名を取得
cur_dir = os.path.dirname(__file__)

# 実行ファイルのあるディレクトリ内のcsvファイル名のlistを取得
csv_list = glob.glob(cur_dir + '/*.csv')

# 出力ディレクトリ
output_dir = cur_dir + '/out'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for filename in csv_list:
    df = pd.read_csv(filename)
    col_name = [name for name in df]
    print("まばたきのタイミング: ") # デバッグ用
    print(col_name) # デバッグ用
    # mean
    mean =  [df[col].mean() for col in col_name]
    print("Mean(平均): ")
    print(mean)
    # SE
    se = [df[col].sem() for col in col_name]
    print("SE(標準誤差): ")
    print(se)

    #### グラフ描画
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111)
    # グリッド線の設定
    ax.grid(axis='y', which="major", color="gray", alpha=0.5,
            linestyle="--", linewidth=0.5)
    # エラーバー付き棒グラフ描画 
    ax.bar(col_name, mean, color="0.7", width=0.4, yerr=se, capsize=10)
    # 軸設定
    ax.set_xlabel('Timing of blinking', labelpad=10, fontsize=32)
    ax.set_ylabel('Score [px]', labelpad=8, fontsize=32)
    # 枠線の表示
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 注釈の追加
    h0, h1, h2 = 79, 84, 91 # 高さの基準 (垂直線，平行線描画用)
    ax.set_ylim([0, h2])
    ax.text(0, h2+5, "*$p<0.05$", size=28, horizontalalignment="center")
    ax.text(0.99, h2, "*", size=24, horizontalalignment="center")
    ax.text(1.47, h1, "*", size=24, horizontalalignment="center")
    ax.text(2.51, h2, "*", size=24, horizontalalignment="center")
    plt.vlines([0], h0, h2, "0.2", linewidth=1)
    plt.vlines([1], h0, h1, "0.2", linewidth=1)
    plt.vlines([1.98], h0, h2, "0.2", linewidth=1)
    plt.vlines([1.94], h0, h1, "0.2", linewidth=1)
    plt.vlines([2.02], h0, h2, "0.2", linewidth=1)
    plt.vlines([3], h0, h2, "0.2", linewidth=1)
    plt.hlines([h2], 0, 1.98, "0.2", linewidth=1)
    plt.hlines([h1], 1, 1.94, "0.2", linewidth=1)
    plt.hlines([h2], 2.02, 3, "0.2", linewidth=1)
    # tight tayout
    plt.tight_layout()
    # pdf出力
    output_file = output_dir + '/' + output_datetime() + '_ErrorBar.pdf'
    plt.savefig(output_file)
    print(output_file + '\n')
    plt.clf()
