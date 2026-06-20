def min_palindrome_partitions(s):
    n = len(s)

    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True

    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length - 1

            if s[i] == s[j]:
                if length == 2 or is_pal[i+1][j-1]:
                    is_pal[i][j] = True
    
    dp = [float('inf')] * n
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0
            continue

        for j in range(1, i+1):
            if is_pal[j][i] and dp[j - 1] + 1 < dp[i]:
                dp[i] = dp[j - 1] + 1
    
    return dp[n - 1] + 1


print(min_palindrome_partitions("abddbba"))