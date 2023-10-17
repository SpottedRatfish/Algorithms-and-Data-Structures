import numpy as np

  
def partition(array, low, end):
    pivot = array[end]
    i = low
    for j in range(low, end):
        if array[j] <= pivot:
            array[i], array[j] = array[j], array[i]
            i += 1
    array[i], array[end] = array[end], array[i]
    return i


def quick_sort(array):
    ranges = [(0, len(array)-1)] 
    while len(ranges) != 0:
        low, end = ranges.pop()
        if low < end:
            pivot_index = partition(array, low, end)
            ranges.append((low, pivot_index-1))
            ranges.append((pivot_index+1, end))
  
array = np.random.randint(1,100,100)
n = len(array)
if __name__ == "__main__":
    print(array)
    quick_sort(array)
    print("Using quick sort:")
    print(array)