import matplotlib.pyplot as plt


def plot_procedure_trajectory(procedure_name, procedure_trajectory):
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.axis('off')
    plt.title(procedure_name, fontsize=14, ha='center', va='top')
    ax.text(0, 1, procedure_trajectory, fontsize=12, ha='left', va='top')
    plt.show()
