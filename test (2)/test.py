import numpy as np

# Tạo ma trận từ dữ liệu đã cung cấp
matrix = np.array([
    [1, 5, 4, 7, 7],
    [1/5, 1, 1/4, 1/2, 2],
    [1/4, 4, 1, 1/2, 4],
    [1/7, 2, 2, 1, 4],
    [1/7, 1/2, 1/4, 1/4, 1]
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