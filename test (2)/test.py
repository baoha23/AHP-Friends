import numpy as np

# Tạo ma trận từ dữ liệu đã cung cấp
matrix = np.array([
    [1, 4/5, 4/6, 4/7, 4/3, 4/2],
    [1.25, 1, 5/6, 5/7, 5/3, 5/2],
    [1.50, 1.20, 1, 6/7, 6/3, 6/2],
    [1.75, 1.40, 1.17, 1, 7/3, 7/2],
    [0.75, 0.60, 0.50, 0.43, 1, 3/2 ],
    [0.50, 0.40, 1, 0.29, 0.67, 1 ]
])

# Tính tổng sum AHP của mỗi cột và in ra ma trận
print("Ma trận AHP:")
print(matrix)
column_sum = np.sum(matrix, axis=0)
print("Tổng sum AHP của mỗi cột:")
print("\t".join([f"{val:.2f}" for val in column_sum]))

# Tính ma trận so sánh cặp và in ra
pairwise_matrix = matrix / column_sum
print("Ma trận so sánh cặp:")
print(pairwise_matrix)

# Tính trọng số của các tiêu chí và in ra
criteria_weights = np.mean(pairwise_matrix, axis=1)
normalized_weights = criteria_weights / np.sum(criteria_weights)
print("Trọng số chuẩn hóa của các tiêu chí:")
print(normalized_weights)

# Tạo ma trận theo trọng số của các tiêu chí
weighted_matrix = matrix * normalized_weights


# In ra ma trận theo trọng số của các tiêu chí
print("Ma trận so sánh cặp theo trọng số của các tiêu chí:")
print(weighted_matrix)

# Tính Weighted Sum Value theo tổng của mỗi hàng của ma trận theo trọng số
weighted_sum_value = np.sum(weighted_matrix, axis=1)

# In ra Weighted Sum Value
print("\nWeighted Sum Value:")
print(weighted_sum_value)

# Tính Consistency vector
consistency_vector = weighted_sum_value / normalized_weights

# In ra Consistency vector
print("\nConsistency vector:")
print(consistency_vector)

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

# In ra kết quả
print("Lambda Max (λmax):", lambda_max)
print("Consistency Index (CI):", CI)
print("Consistency Ratio (CR):", CR)