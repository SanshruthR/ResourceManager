import psutil
import tkinter as tk
from tkinter import font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update_graph():
    # Get the list of processes
    processes = []
    for proc in psutil.process_iter(["name", "memory_info"]):
        try:
            name = proc.info["name"]
            memory = proc.info["memory_info"].rss / (1024 * 1024)
            processes.append((name, memory))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort the processes by memory usage
    processes.sort(key=lambda x: x[1], reverse=True)

    # Update the pie chart
    names, memory = zip(*processes[:10])
    pie_chart.clear()
    pie_chart.pie(memory, labels=names)

    # Redraw the canvas
    canvas.draw()

    # Schedule the next update
    root.after(1000, update_graph)

# Create the main window
root = tk.Tk()
root.title("Memory Usage Monitor")

# Set the size of the window to 500 by 600
root.geometry("500x600")
root.resizable(False, False)

# Create the title label
title_font = font.Font(family="Helvetica", size=24)
title_label = tk.Label(root, text="Memory Usage", font=title_font,fg='teal')
title_label.pack(pady=10)

# Create the pie chart
figure = Figure(figsize=(6, 6))
pie_chart = figure.add_subplot(1, 1, 1)
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack()

# Create the link label
link_font = font.Font(size=12)
link_label = tk.Label(root, text="https://github.com/SanshruthR", font=link_font, bg="teal", fg='white')
link_label.place(x=165,y=560)



# Start the update loop
update_graph()

# Run the main loop
root.mainloop()