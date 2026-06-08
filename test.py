import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# -------------------------------
# COMPREHENSIVE TEST CASES
# -------------------------------

# Test Case 1: Basic Detection
test_cases = [
    {
        'name': 'Basic Detection',
        'actual_drowsy': [0,1,1,0,1,0,1,0],
        'pred_drowsy': [0,1,0,0,1,0,1,0],
        'actual_fatigue': [0,0,1,1,0,1,0,1],
        'pred_fatigue': [0,0,1,0,0,1,0,1],
        'actual_water': [0,1,0,1,0,1,0,1],
        'pred_water': [0,1,0,0,0,1,0,1]
    },
    {
        'name': 'Extended Test',
        'actual_drowsy': [0,1,1,0,1,0,1,0,1,1,0,0],
        'pred_drowsy': [0,1,0,0,1,0,1,0,1,0,0,1],
        'actual_fatigue': [0,0,1,1,0,1,0,1,1,0,0,1],
        'pred_fatigue': [0,0,1,0,0,1,0,1,0,0,1,1],
        'actual_water': [0,1,0,1,0,1,0,1,0,0,1,1],
        'pred_water': [0,1,0,0,0,1,0,1,0,1,0,1]
    },
    {
        'name': 'High Accuracy Test',
        'actual_drowsy': [0,0,0,1,1,1,0,0,1,0],
        'pred_drowsy': [0,0,0,1,1,1,0,0,1,0],
        'actual_fatigue': [0,0,1,1,0,1,0,1,0,0],
        'pred_fatigue': [0,0,1,1,0,1,0,1,0,0],
        'actual_water': [0,1,0,1,0,1,0,1,0,1],
        'pred_water': [0,1,0,1,0,1,0,1,0,1]
    },
    {
        'name': 'Challenging Test',
        'actual_drowsy': [0,1,0,1,0,1,0,1,1,0],
        'pred_drowsy': [0,0,1,1,0,0,1,1,0,0],
        'actual_fatigue': [1,0,1,0,1,0,1,0,1,0],
        'pred_fatigue': [1,1,0,0,1,0,0,1,1,0],
        'actual_water': [0,1,0,1,0,1,0,1,0,1],
        'pred_water': [0,0,1,1,0,0,1,1,0,0]
    },
    {
        'name': 'Real-world Scenario',
        'actual_drowsy': [0,0,0,0,1,1,1,0,0,1,0,1,0,0,1],
        'pred_drowsy': [0,0,0,0,1,0,1,0,0,1,0,0,0,0,1],
        'actual_fatigue': [0,0,0,1,1,1,0,0,1,1,0,0,1,0,0],
        'pred_fatigue': [0,0,0,1,0,1,0,0,1,1,0,0,1,0,0],
        'actual_water': [0,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
        'pred_water': [0,0,1,0,0,0,1,0,1,0,1,0,0,0,1]
    }
]

# -------------------------------
# FUNCTION
# -------------------------------

def calculate_accuracy(actual, predicted):
    correct = sum(1 for a, p in zip(actual, predicted) if a == p)
    total = len(actual)
    incorrect = total - correct
    accuracy = (correct / total) * 100
    return accuracy, correct, incorrect, total

# -------------------------------
# COLLECT ALL TEST RESULTS
# -------------------------------

all_results = []
test_names = []

for test_case in test_cases:
    acc_d, cor_d, inc_d, tot_d = calculate_accuracy(test_case['actual_drowsy'], test_case['pred_drowsy'])
    acc_f, cor_f, inc_f, tot_f = calculate_accuracy(test_case['actual_fatigue'], test_case['pred_fatigue'])
    acc_h, cor_h, inc_h, tot_h = calculate_accuracy(test_case['actual_water'], test_case['pred_water'])
    
    all_results.append({
        'drowsiness': acc_d,
        'fatigue': acc_f,
        'hydration': acc_h,
        'drowsiness_correct': cor_d,
        'drowsiness_total': tot_d,
        'fatigue_correct': cor_f,
        'fatigue_total': tot_f,
        'hydration_correct': cor_h,
        'hydration_total': tot_h
    })
    test_names.append(test_case['name'])

# -------------------------------
# CALCULATE OVERALL AVERAGES
# -------------------------------

avg_drowsiness = np.mean([result['drowsiness'] for result in all_results])
avg_fatigue = np.mean([result['fatigue'] for result in all_results])
avg_hydration = np.mean([result['hydration'] for result in all_results])

total_drowsiness_correct = sum(result['drowsiness_correct'] for result in all_results)
total_drowsiness_tests = sum(result['drowsiness_total'] for result in all_results)
total_fatigue_correct = sum(result['fatigue_correct'] for result in all_results)
total_fatigue_tests = sum(result['fatigue_total'] for result in all_results)
total_hydration_correct = sum(result['hydration_correct'] for result in all_results)
total_hydration_tests = sum(result['hydration_total'] for result in all_results)

# -------------------------------
# CREATE COMPREHENSIVE ACCURACY GRAPH
# -------------------------------

# Set style for better visibility
plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 11,
    'figure.titlesize': 16
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
fig.suptitle('Smart Study Break System - Comprehensive Accuracy Analysis', fontsize=16, fontweight='bold', y=0.98)

# Graph 1: Individual Test Case Performance
x = np.arange(len(test_names))
width = 0.25

# Use stronger, more distinct colors
colors_drowsiness = '#1f77b4'  # Blue
colors_fatigue = '#ff7f0e'     # Orange  
colors_hydration = '#2ca02c'   # Green

bars1 = ax1.bar(x - width, [result['drowsiness'] for result in all_results], width, 
                label='Drowsiness Detection', color=colors_drowsiness, alpha=0.8, edgecolor='black', linewidth=1)
bars2 = ax1.bar(x, [result['fatigue'] for result in all_results], width, 
                label='Fatigue Detection', color=colors_fatigue, alpha=0.8, edgecolor='black', linewidth=1)
bars3 = ax1.bar(x + width, [result['hydration'] for result in all_results], width, 
                label='Hydration Reminder', color=colors_hydration, alpha=0.8, edgecolor='black', linewidth=1)

ax1.set_xlabel('Test Cases', fontweight='bold')
ax1.set_ylabel('Accuracy (%)', fontweight='bold')
ax1.set_title('Performance Analysis Across Different Test Scenarios', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(test_names, rotation=45, ha='right', fontweight='bold')
ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
ax1.set_ylim(0, 105)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_facecolor('#f8f9fa')

# Add value labels on bars with better formatting
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}%',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 2),
                     textcoords="offset points",
                     ha='center', va='bottom', 
                     fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

add_value_labels(bars1)
add_value_labels(bars2)
add_value_labels(bars3)

# Graph 2: Overall Average Performance
categories = ['Drowsiness\nDetection', 'Fatigue\nDetection', 'Hydration\nReminder']
averages = [avg_drowsiness, avg_fatigue, avg_hydration]
colors = [colors_drowsiness, colors_fatigue, colors_hydration]

bars = ax2.bar(categories, averages, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
ax2.set_ylabel('Average Accuracy (%)', fontweight='bold')
ax2.set_title('Overall System Performance Summary', fontweight='bold')
ax2.set_ylim(0, 105)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_facecolor('#f8f9fa')

# Add value labels and counts on bars with better formatting
for i, (bar, avg) in enumerate(zip(bars, averages)):
    height = bar.get_height()
    if i == 0:  # Drowsiness
        count_text = f'({total_drowsiness_correct}/{total_drowsiness_tests})'
        label = 'Drowsiness'
    elif i == 1:  # Fatigue
        count_text = f'({total_fatigue_correct}/{total_fatigue_tests})'
        label = 'Fatigue'
    else:  # Hydration
        count_text = f'({total_hydration_correct}/{total_hydration_tests})'
        label = 'Hydration'
    
    ax2.annotate(f'{avg:.1f}%\n{count_text}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom', 
                 fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9))

# -------------------------------
# COMPREHENSIVE CONCLUSION
# -------------------------------

conclusion = (
    f"Comprehensive Test Results Summary:\n\n"
    f"Test Cases Evaluated: {len(test_cases)}\n"
    f"Total Test Samples: {total_drowsiness_tests + total_fatigue_tests + total_hydration_tests}\n\n"
    f"Overall Performance:\n"
    f"• Drowsiness Detection: {avg_drowsiness:.1f}% average accuracy ({total_drowsiness_correct}/{total_drowsiness_tests} correct)\n"
    f"• Fatigue Detection: {avg_fatigue:.1f}% average accuracy ({total_fatigue_correct}/{total_fatigue_tests} correct)\n"
    f"• Hydration Reminder: {avg_hydration:.1f}% average accuracy ({total_hydration_correct}/{total_hydration_tests} correct)\n\n"
    f"Test Case Performance:\n"
)

for i, (name, result) in enumerate(zip(test_names, all_results)):
    conclusion += f"• {name}: D={result['drowsiness']:.1f}%, F={result['fatigue']:.1f}%, H={result['hydration']:.1f}%\n"

conclusion += f"\nSystem Overall Rating: {np.mean([avg_drowsiness, avg_fatigue, avg_hydration]):.1f}% accuracy"

# Adjust layout and add conclusion
plt.tight_layout()
plt.subplots_adjust(bottom=0.25)
plt.figtext(0.02, 0.02, conclusion, ha='left', fontsize=9, 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))

# Add timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
plt.figtext(0.98, 0.02, f"Generated: {timestamp}", ha='right', fontsize=8, style='italic')

plt.show()