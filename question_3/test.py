a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sites = [0, 9]
tmp_list = a[sites[0]:sites[1]]
tmp_list.reverse()
a[sites[0]:sites[1]] = tmp_list
print(a)