import matplotlib.pyplot as plt
import numpy as np
species  = ['Dog\n(4 classes)', 'Cattle\n(3 classes)', 'Poultry\n(4 classes)']
accuracy = [89, 92, 98]
macro_f1 = [87, 93, 97]
wtd_f1   = [89, 92, 98]
x = np.arange(len(species))
w = 0.25
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w,   accuracy, w, label='Accuracy (%)',       color='
ax.bar(x,       macro_f1, w, label='Macro F1 (%)',       color='
ax.bar(x + w,   wtd_f1,   w, label='Weighted F1 (%)',    color='
ax.set_xticks(x); ax.set_xticklabels(species, fontsize=11)
ax.set_ylabel('Score (%)'); ax.set_ylim([80, 102])
ax.legend(); ax.grid(axis='y', alpha=0.3)
for bars in ax.containers:
    ax.bar_label(bars, fmt='%d%%', padding=2, fontsize=8)
ax.set_title('Model Performance Comparison Across Animal Species', fontweight='bold')
plt.tight_layout()
plt.savefig('fig61_performance_comparison.png', dpi=300, bbox_inches='tight')