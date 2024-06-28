import tkinter as tk
from tkinter import messagebox
import math

def find_starting_point(points):
    current_min_point = points[0]
    for point in points:
        if point['y'] < current_min_point['y']:
            current_min_point = point
        elif point['y'] == current_min_point['y']:
            if point['x'] < current_min_point['x']:
                current_min_point = point
    return current_min_point

def sort_points(points, p0):
    sorted_points = sorted(points, key=lambda point: (math.atan2(point['y'] - p0['y'], point['x'] - p0['x']), point['x'], point['y']))
    result = []
    for point in sorted_points:
        if len(result) < 2:
            result.append(point)
        else:
            last_point = result[-1]
            last_angle = math.atan2(last_point['y'] - p0['y'], last_point['x'] - p0['x'])
            current_angle = math.atan2(point['y'] - p0['y'], point['x'] - p0['x'])
            if abs(last_angle - current_angle) < 1e-9:
                last_distance = abs(last_point['x'] - p0['x']) + abs(last_point['y'] - p0['y'])
                current_distance = abs(point['x'] - p0['x']) + abs(point['y'] - p0['y'])
                if current_distance > last_distance:
                    result[-1] = point
            else:
                result.append(point)
    return result

def ccw(a, b, c):
    return (b['x'] - a['x']) * (c['y'] - a['y']) - (c['x'] - a['x']) * (b['y'] - a['y'])

def next_to_top(stack):
    return stack[-2]

def top(stack):
    return stack[-1]

def graham_scan(points, delay):
    if len(points) < 2:
        return []
    p0 = find_starting_point(points)
    sorted_points = sort_points(points, p0)
    stack = []
    for point in sorted_points:
        while len(stack) > 1 and ccw(next_to_top(stack), top(stack), point) <= 0:
            stack.pop()
            plot_convex_hull(points, stack, point, delay)
        stack.append(point)
        plot_convex_hull(points, stack, point, delay)
    return stack

def plot_convex_hull(points, hull, current_point=None, delay=500):
    canvas.delete("all")
    for point in points:
        x = center_x + point['x'] * scale
        y = center_y - point['y'] * scale
        canvas.create_oval(x-3, y-3, x+3, y+3, fill='blue')

    if len(hull) > 1:
        hull_points = [coord for point in hull for coord in (center_x + point['x'] * scale, center_y - point['y'] * scale)]
        hull_points += [center_x + hull[0]['x'] * scale, center_y - hull[0]['y'] * scale]  # Zamknij otoczkę
        canvas.create_line(hull_points, fill='red')

    if current_point:
        x = center_x + current_point['x'] * scale
        y = center_y - current_point['y'] * scale
        canvas.create_oval(x-5, y-5, x+5, y+5, fill='green')

    root.update()
    root.after(delay)

def add_point():
    try:
        x = int(entry_x.get())
        y = int(entry_y.get())
        if -30 <= x <= 30 and -30 <= y <= 30:
            points.append({'x': x, 'y': y})
            entry_x.delete(0, tk.END)
            entry_y.delete(0, tk.END)
            plot_convex_hull(points, [])
        else:
            messagebox.showerror("Błąd", "Punkt poza dozwolonym zakresem (-30 do 30)!")
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawne współrzędne!")

def start_algorithm():
    try:
        delay = int(entry_delay.get())
    except ValueError:
        delay = 1000  # Default delay
    graham_scan(points, delay)

# Utwórz okno tkinter
root = tk.Tk()
root.title("Wizualizacja Algorytmu Grahama")
width, height = 1920, 1080
center_x, center_y = (width - 300) // 2, height // 2
scale = (height - 100) / 70  # Skala dostosowana do zakresu od -35 do 35 z marginesem

root.geometry(f"{width}x{height}")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=20, pady=20)

tk.Label(frame, text="X:").grid(row=0, column=0)
entry_x = tk.Entry(frame)
entry_x.grid(row=0, column=1)

tk.Label(frame, text="Y:").grid(row=1, column=0)
entry_y = tk.Entry(frame)
entry_y.grid(row=1, column=1)

tk.Label(frame, text="Czas (ms):").grid(row=2, column=0)
entry_delay = tk.Entry(frame)
entry_delay.grid(row=2, column=1)
entry_delay.insert(0, "1000")

add_button = tk.Button(frame, text="Dodaj Punkt", command=add_point)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

start_button = tk.Button(frame, text="Start", command=start_algorithm)
start_button.grid(row=4, column=0, columnspan=2, pady=5)

canvas = tk.Canvas(root, width=width - 300, height=height, bg='white')
canvas.pack(side=tk.RIGHT)

points = []

root.mainloop()
