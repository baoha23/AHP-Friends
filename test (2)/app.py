from flask import Flask, render_template, request
import numpy as np
import pandas as pd

app = Flask(__name__)

def convert_to_float(value):
    if '/' in value:
        fraction_parts = value.split('/')
        numerator = float(fraction_parts[0])
        denominator = float(fraction_parts[1])
        return round(numerator / denominator, 4)
    else:
        return round(float(value), 4)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/process_matrix', methods=['POST'])
def process_matrix():
    data = []

    row1 = []
    value11 = 1
    value12 = float(request.form.get("12"))
    value13 = float(request.form.get("13"))
    value14 = float(request.form.get("14"))
    value15 = float(request.form.get("15"))
    row1.extend([value11, value12, value13, value14, value15])

    row2 = []
    value21 = 1 / (float(request.form.get("12")) if request.form.get("12").isdigit() else float(request.form.get("12")))
    value22 = 1
    value23 = convert_to_float(request.form.get("23"))
    value24 = convert_to_float(request.form.get("24"))
    value25 = float(request.form.get("25"))
    row2.extend([value21, value22, value23, value24, value25])

    row3 = []
    value31 = 1 / (float(request.form.get("13")) if request.form.get("13").isdigit() else float(request.form.get("13")))
    value32 = 1 / (convert_to_float(request.form.get("23")) if request.form.get("23").isdigit() else convert_to_float(request.form.get("23")))
    value33 = 1
    value34 = convert_to_float(request.form.get("34"))
    value35 = float(request.form.get("35"))
    row3.extend([value31, value32, value33, value34, value35])

    row4 = []
    value41 = 1 / (float(request.form.get("14")) if request.form.get("14").isdigit() else float(request.form.get("14")))
    value42 = 1 / (convert_to_float(request.form.get("24")) if request.form.get("24").isdigit() else convert_to_float(request.form.get("24")))
    value43 = 1 / (convert_to_float(request.form.get("34")) if request.form.get("34").isdigit() else convert_to_float(request.form.get("34")))
    value44 = 1
    value45 = float(request.form.get("45"))
    row4.extend([value41, value42, value43, value44, value45])

    row5 = []
    value51 = 1 / (float(request.form.get("15")) if request.form.get("15").isdigit() else float(request.form.get("15")))
    value52 = 1 / (float(request.form.get("25")) if request.form.get("25").isdigit() else float(request.form.get("25")))
    value53 = 1 / (float(request.form.get("35")) if request.form.get("35").isdigit() else float(request.form.get("35")))
    value54 = 1 / (float(request.form.get("45")) if request.form.get("45").isdigit() else float(request.form.get("45")))
    value55 = 1
    row5.extend([value51, value52, value53, value54, value55])

    data.extend([row1, row2, row3, row4, row5])

    matrix = np.array(data).round(2)  # Chuyển DataFrame thành ma trận NumPy với số lẻ làm tròn đến 2 chữ số thập phân

    # Tính tổng của mỗi cột
    column_sum = matrix.sum(axis=0)

    # Tính ma trận so sánh cặp
    pairwise_matrix = np.round(matrix / column_sum, 4)

    # Tính trọng số của các tiêu chí
    criteria_weights = np.mean(pairwise_matrix, axis=1)
    normalized_weights = criteria_weights / np.sum(criteria_weights)
    # Làm tròn normalized_weights với 4 chữ số thập phân
    normalized_weights = np.round(normalized_weights, 4)
        # Tạo ma trận theo trọng số của các tiêu chí và làm tròn
    weighted_matrix = np.round(matrix * normalized_weights, 4)
        
    # Tính Weighted Sum Value theo tổng của mỗi hàng của ma trận theo trọng số và làm tròn
    weighted_sum_value = np.round(np.sum(weighted_matrix, axis=1), 4)
        
    # Tính Consistency vector và làm tròn
    consistency_vector = np.round(weighted_sum_value / normalized_weights, 4)

    # Tính Lambda Max (λmax)
    lambda_max = np.mean(consistency_vector)

    # Số lượng tiêu chí
    n = len(normalized_weights)

    # Tính Consistency Index (CI)
    CI = (lambda_max - n) / (n - 1)

    # Bảng tham chiếu để tính tỉ số nhất quán CR
    RI = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    RI_n = RI[n]

    # Tính tỉ số nhất quán CR
    CR = CI / RI_n if RI_n != 0 else 0
    
    # Thêm cột mới cho ma trận so sánh cặp
    pairwise_matrix_with_weights = np.column_stack((normalized_weights, pairwise_matrix))

    # Truyền dữ liệu vào trang result.html và render trang đó
    criteria_data = ["Giá tiền", "Hãng sản xuất", "Ram", "Màn hình", "Trọng lượng"]
    result = {
        'matrix': matrix.tolist(),  # Chuyển ma trận NumPy thành danh sách
        'column_sum': column_sum.tolist(),
        'pairwise_matrix_with_weights': pairwise_matrix.tolist(),  # Chuyển đổi ma trận so sánh cặp có trọng số thành danh sách
        # Các khóa khác ở đây
        'normalized_weights': normalized_weights.tolist(),  # Chuyển đổi trọng số chuẩn hóa thành danh sách
        'weighted_matrix': weighted_matrix.tolist(),  # Chuyển đổi ma trận theo trọng số thành danh sách
        'weighted_sum_value': weighted_sum_value.tolist(),  # Chuyển đổi Weighted Sum Value thành danh sách
        'consistency_vector': consistency_vector.tolist(), # Thêm Consistency vector vào kết quả
        'lambda_max': lambda_max,
        'n': n,
        'CI': CI,
        'CR': CR
    }

    return render_template('ketqua.html', result=result, criteria_data=criteria_data)

if __name__ == '__main__':
    app.run(debug=True)
