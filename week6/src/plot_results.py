"""Plot source-reported results, without rerunning models or inventing measurements."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def build_charts():
    destination = ROOT / 'images' / 'charts'
    destination.mkdir(parents=True, exist_ok=True)
    with (ROOT / 'data/results.csv').open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    labels = ['Original model\nClean accuracy', 'Modified model\nClean accuracy', 'Modified model\nTargeted ASR']
    values = [float(row['Value']) for row in rows]
    fig, ax = plt.subplots(figsize=(9.5, 5.0), layout='constrained')
    bars = ax.bar(labels, values, width=0.60)
    ax.bar_label(bars, labels=[f'{v:.2f}%' for v in values], padding=5, fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Percent')
    ax.set_title('Week 6 | Reported evaluation results', loc='left', fontsize=16, pad=18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', length=0, pad=9)
    ax.text(0.0, -0.22, 'Source: supplied results.csv and saved notebook evaluation.\nASR excludes true airplane inputs; accuracy and ASR measure different outcomes.',
            transform=ax.transAxes, fontsize=9, va='top')
    fig.savefig(destination / 'reported_metrics.png', dpi=180, bbox_inches='tight')
    fig.savefig(destination / 'reported_metrics.svg', bbox_inches='tight')
    plt.close(fig)

    with (ROOT / 'data/training_history.csv').open(newline='', encoding='utf-8') as stream:
        history = list(csv.DictReader(stream))
    clean = [r for r in history if r['stage'] == 'clean']
    backdoor = [r for r in history if r['stage'] == 'backdoor']
    fig, ax = plt.subplots(figsize=(9.5, 4.7), layout='constrained')
    ax.plot([int(r['epoch']) for r in clean], [float(r['loss']) for r in clean],
            marker='o', label='Original training; clean labels')
    ax.plot([5 + int(r['epoch']) for r in backdoor], [float(r['loss']) for r in backdoor],
            marker='s', linestyle='--', label='Copied model; poisoned fine-tuning')
    ax.set_xticks(range(1, 9))
    ax.set_xlabel('Training stage position (5 original + 3 fine-tuning epochs)')
    ax.set_ylabel('Mean batch cross-entropy loss')
    ax.set_title('Week 6 | Saved training losses', loc='left', fontsize=16, pad=16)
    ax.legend(frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(0, -0.20, 'Derived from the retained notebook outputs. The two stages use different labels\nand learning rates; this is not an equal-budget model comparison.',
            transform=ax.transAxes, fontsize=9, va='top')
    fig.savefig(destination / 'training_loss.png', dpi=180, bbox_inches='tight')
    fig.savefig(destination / 'training_loss.svg', bbox_inches='tight')
    plt.close(fig)
    return destination


if __name__ == '__main__':
    print('Charts written to:', build_charts())
