from classes import Task


def merge_sort(list: list[Task]):
    if len(list) <= 1:
        return list
    mid = len(list) // 2
    left = merge_sort(list[:mid])
    right = merge_sort(list[mid:])
    return merge(left, right)



def merge(left: list[Task], right: list[Task]):
    sorted = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i].duration <= right[j].duration:
            sorted.append(left[i])
            i += 1
        else:
            sorted.append(right[j])
            j += 1
    sorted.extend(left[i:])
    sorted.extend(right[j:])
    return sorted

