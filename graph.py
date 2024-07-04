import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from scipy.interpolate import make_interp_spline
import io


# 날짜와 체중 데이터 추출
def print_graph(user_data):
    dates = pd.to_datetime(user_data["dates"])
    weights = user_data["weights"]

    # 그래프 그리기
    plt.figure(figsize=(10, 5))

    # 데이터가 특정 개수 이상이면 스플라인 보간 사용
    if len(dates) > 10:
        # 날짜를 숫자로 변환
        dates_num = np.array([date.timestamp() for date in dates])
        weights = np.array(weights)

        # 스플라인 보간
        spline = make_interp_spline(dates_num, weights)
        dates_smooth = np.linspace(dates_num.min(), dates_num.max(), 300)
        weights_smooth = spline(dates_smooth)

        # 숫자를 날짜로 변환
        dates_smooth = [datetime.fromtimestamp(ts) for ts in dates_smooth]

        plt.plot(dates_smooth, weights_smooth, color="b")
    else:
        plt.plot(dates, weights, marker="o", linestyle="-", color="b")

    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.title("")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=0)

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return img
