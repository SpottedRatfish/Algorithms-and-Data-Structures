import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import random
def heap(arr, n, i):
    root = i
    lc = 2*i + 1
    rc = 2*i + 2
    if lc < n  and arr[i] < arr[lc]:
        root = lc
    if rc < n and arr[root] < arr[rc]:
        root = rc
    if root != i:
        arr[i], arr[root] = arr[root], arr[i]
        heap(arr, n, root)


def heap_sort(arr):
    n = len(arr)
    for i in range(n//2, -1, -1):
        heap(arr, n, i)
        yield arr
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        heap(arr, i, 0)
        yield arr

def animate(_list, generator, title):
    n = len(_list)
    fig, ax = plt.subplots()
    ax.set_title(title)
 
    bar_rects = ax.bar(range(len(_list)), _list, align="edge")  
    ax.set_xlim(0, n)
    ax.set_ylim(0, int(1.1*n))
    text = ax.text(0.01, 0.95, "", transform = ax.transAxes)
    iteration = [0]
    def _animate(array, rects, iteration):
        for rect, val in zip(rects, array):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"iterations: {iteration[0]}")
   
    anim = FuncAnimation(fig, func=_animate,
        fargs=(bar_rects, iteration), frames=generator, interval=10,
        repeat=False)
    plt.show()

array = [i for i in range(100)]
random.shuffle(array)
if __name__ == "__main__":
    animate(array, heap_sort(array), "heap sort")