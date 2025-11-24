import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------
# DATA PROVIDED BY THE USER
# ------------------------------------------------------

# CLASS EXTRACTION METRICS
vn_class_precision = [0.59, 0.45, 0.66]
vn_class_recall = [0.63, 0.68, 0.69]
vn_class_f1 = [0.61, 0.54, 0.68]

dmp_class_precision = [0.96, 0.91, 0.90]
dmp_class_recall = [0.84, 0.81, 0.68]
dmp_class_f1 = [0.90, 0.86, 0.78]

# RELATIONSHIP EXTRACTION METRICS
vn_rel_precision = [0.72, 0.33, 0.61]
vn_rel_recall = [0.66, 0.31, 0.37]
vn_rel_f1 = [0.69, 0.32, 0.46]

dmp_rel_precision = [1.00, 0.87, 0.87]
dmp_rel_recall = [0.70, 0.62, 0.41]
dmp_rel_f1 = [0.82, 0.72, 0.56]


# ------------------------------------------------------
# FIXED FUNCTION WITH CORRECT ORDERING
# ------------------------------------------------------

def plot_six_group_metric_figure(title, vn_prec, vn_rec, vn_f1, dmp_prec, dmp_rec, dmp_f1):
    # Correct ordering: VN-D1, DMP-D1, VN-D2, DMP-D2, VN-D3, DMP-D3
    precision = [
        vn_prec[0], dmp_prec[0],
        vn_prec[1], dmp_prec[1],
        vn_prec[2], dmp_prec[2]
    ]

    recall = [
        vn_rec[0], dmp_rec[0],
        vn_rec[1], dmp_rec[1],
        vn_rec[2], dmp_rec[2]
    ]

    f1 = [
        vn_f1[0], dmp_f1[0],
        vn_f1[1], dmp_f1[1],
        vn_f1[2], dmp_f1[2]
    ]

    groups = ["VN D1", "DMP D1", "VN D2", "DMP D2", "VN D3", "DMP D3"]

    x = np.arange(len(groups))  # 6 groups
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(x - width, precision, width, label='Precision')
    ax.bar(x, recall, width, label='Recall')
    ax.bar(x + width, f1, width, label='F1 Score')

    ax.set_xlabel('Model–Dataset Groups')
    ax.set_ylabel('Score')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.legend()

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------
# FIGURE 6 — CLASS EXTRACTION
# ------------------------------------------------------
plot_six_group_metric_figure(
    "Class Extraction Performance (VN vs DMP across Datasets)",
    vn_class_precision, vn_class_recall, vn_class_f1,
    dmp_class_precision, dmp_class_recall, dmp_class_f1
)

# ------------------------------------------------------
# FIGURE 7 — RELATIONSHIP EXTRACTION
# ------------------------------------------------------
plot_six_group_metric_figure(
    "Relationship Extraction Performance (VN vs DMP across Datasets)",
    vn_rel_precision, vn_rel_recall, vn_rel_f1,
    dmp_rel_precision, dmp_rel_recall, dmp_rel_f1
)



