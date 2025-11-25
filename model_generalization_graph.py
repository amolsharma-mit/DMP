import matplotlib.pyplot as plt
import numpy as np

# Labels (Model + Dataset)
labels = [
    "deepseek-RMS", "deepseek-OPS",
    "sonar-RMS", "sonar-OPS",
    "gemini-RMS", "gemini-OPS",
    "gpt5-RMS", "gpt5-OPS"
]

# ------------------------------
# CLASS EXTRACTION METRICS
# ------------------------------
class_precision = [0.9231, 0.7647, 0.4107, 0.4107, 0.7692, 0.7432, 0.7857, 0.7714]
class_recall    = [0.5946, 0.7027, 0.4800, 0.4181, 0.7813, 0.7037, 0.6563, 0.6750]
class_f1        = [0.7241, 0.7324, 0.4425, 0.4144, 0.7752, 0.7229, 0.7143, 0.7200]

# ------------------------------
# RELATIONSHIP EXTRACTION METRICS
# ------------------------------
rel_precision = [0.7576, 0.7730, 0.2469, 0.2029, 0.5385, 0.3559, 0.4103, 0.3571]
rel_recall    = [0.4902, 0.3455, 0.3372, 0.1282, 0.4595, 0.3582, 0.4375, 0.5568]
rel_f1        = [0.5952, 0.4754, 0.2852, 0.1570, 0.4954, 0.3570, 0.4235, 0.4333]

x = np.arange(len(labels))       # positions
width = 0.25                     # bar width

# ------------------------------
# FIGURE 1 — CLASS EXTRACTION
# ------------------------------
fig1, ax1 = plt.subplots(figsize=(14, 7))

ax1.bar(x - width, class_precision, width, label="Precision")
ax1.bar(x,         class_recall,    width, label="Recall")
ax1.bar(x + width, class_f1,        width, label="F1 Score")

ax1.set_title("Class Extraction Performance")
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45, ha="right")
ax1.set_ylabel("Score")
ax1.set_xlabel("Model-Dataset")
ax1.legend()

plt.tight_layout()
plt.show()

# ------------------------------
# FIGURE 2 — RELATIONSHIP EXTRACTION
# ------------------------------
fig2, ax2 = plt.subplots(figsize=(14, 7))

ax2.bar(x - width, rel_precision, width, label="Precision")
ax2.bar(x,         rel_recall,    width, label="Recall")
ax2.bar(x + width, rel_f1,        width, label="F1 Score")

ax2.set_title("Relationship Extraction Performance")
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=45, ha="right")
ax2.set_ylabel("Score")
ax2.set_xlabel("Model-Dataset")
ax2.legend()

plt.tight_layout()
plt.show()
