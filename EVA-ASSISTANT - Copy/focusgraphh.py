import matplotlib.pyplot as pt

def focus_graph():
    with open("focus.txt", "r") as file:
        content = file.read().strip().split(",")

    # Filter out empty strings
    content = [float(i) for i in content if i.strip()]

    x1 = list(range(len(content)))

    print(content)
    y1 = content

    pt.plot(x1, y1, color="red", marker="o")
    pt.title("YOUR FOCUSED TIME", fontsize=16)
    pt.xlabel("Times", fontsize=14)
    pt.ylabel("Focus Time", fontsize=14)
    pt.grid()
    pt.show()

# Call the function to plot the graph
focus_graph()
