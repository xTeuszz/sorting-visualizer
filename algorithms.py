import time


def bubble_sort(arr, draw, delay):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            draw(arr, compare=[j, j + 1])
            time.sleep(delay)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw(arr, swap=[j, j + 1])
                time.sleep(delay)
    draw(arr, done=True)


def selection_sort(arr, draw, delay):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw(arr, compare=[min_idx, j])
            time.sleep(delay)
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw(arr, swap=[i, min_idx])
        time.sleep(delay)
    draw(arr, done=True)


def insertion_sort(arr, draw, delay):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            draw(arr, compare=[j, j + 1])
            time.sleep(delay)
            arr[j + 1] = arr[j]
            draw(arr, swap=[j, j + 1])
            time.sleep(delay)
            j -= 1
        arr[j + 1] = key
    draw(arr, done=True)


def merge_sort(arr, draw, delay, l=None, r=None):
    if l is None:
        l = 0
    if r is None:
        r = len(arr) - 1
    if l < r:
        m = (l + r) // 2
        merge_sort(arr, draw, delay, l, m)
        merge_sort(arr, draw, delay, m + 1, r)
        _merge(arr, draw, delay, l, m, r)
    if l == 0 and r == len(arr) - 1:
        draw(arr, done=True)


def _merge(arr, draw, delay, l, m, r):
    left  = arr[l:m + 1]
    right = arr[m + 1:r + 1]
    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        draw(arr, compare=[l + i, m + 1 + j])
        time.sleep(delay)
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        draw(arr, swap=[k])
        time.sleep(delay)
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        draw(arr, swap=[k - 1])
        time.sleep(delay)
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        draw(arr, swap=[k - 1])
        time.sleep(delay)


def quick_sort(arr, draw, delay, low=None, high=None, top=True):
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = _partition(arr, draw, delay, low, high)
        quick_sort(arr, draw, delay, low, pi - 1, False)
        quick_sort(arr, draw, delay, pi + 1, high, False)
    if top:
        draw(arr, done=True)


def _partition(arr, draw, delay, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        draw(arr, compare=[j, high])
        time.sleep(delay)
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            draw(arr, swap=[i, j])
            time.sleep(delay)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw(arr, swap=[i + 1, high])
    time.sleep(delay)
    return i + 1


ALGORITHMS = {
    "Bubble Sort":    bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort":     merge_sort,
    "Quick Sort":     quick_sort,
}
