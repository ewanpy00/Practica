def sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0 or k > len(nums):
        return []

    result = []
    window = []  # indices, values in decreasing order

    for i, value in enumerate(nums):
        while window and nums[window[-1]] <= value:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.pop(0)
        if i >= k - 1:
            result.append(nums[window[0]])

    return result

# print(sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3))
# print(sliding_window_maximum([1, 2, 3], 4))
