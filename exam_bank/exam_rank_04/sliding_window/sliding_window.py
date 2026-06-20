def max_sliding_window(nums, k):
    result = []

    start_w = 0
    end_w = k

    while end_w < len(nums) + 1:
        result.append(max(nums[start_w:end_w]))
        start_w += 1
        end_w += 1

    return result

l = [1, 2, 5, -1, 0, 3]
k = 3
print(max_sliding_window(l, k))
