#!/usr/bin/env python3
"""Summarize one completed run without altering its outputs or scoring oracle."""

import json
from pathlib import Path
import sys

from runner import DIMENSIONS, REVISIONS, ROOT


def main():
    run = Path(sys.argv[1]).resolve()
    expected = json.loads((ROOT / 'expectations.json').read_text())
    report = json.loads((run / 'scores.json').read_text())
    result = {'run': str(run), 'agents': {}}
    for agent in REVISIONS:
        cells = [c for c in report['cells'] if c['agent'] == agent]
        stats = {'aggregate': report['per_agent'][agent], 'dimensions': {},
                 'verdict_matches': 0, 'false_blocked_cases': [], 'missed_blocker_cases': [],
                 'cost_usd': 0, 'task_seconds': 0, 'cases': {}}
        for dimension in DIMENSIONS:
            values = [c['score'] for c in cells if c['scorer'] == dimension]
            stats['dimensions'][dimension] = sum(values) / len(values)
        for task, oracle in expected.items():
            output = run / agent / task
            review = json.loads((output / 'review.json').read_text())
            metadata = json.loads((output / 'metadata.json').read_text())
            stats['cost_usd'] += metadata['summary']['cost_usd']
            stats['task_seconds'] += metadata['duration_s']
            stats['verdict_matches'] += review['verdict'] == oracle['verdict']
            actual_blocker = any(f['severity'] == 'blocker' for f in review['findings'])
            wanted_blocker = any(f['severity'] == 'blocker' for f in oracle['findings'])
            if actual_blocker and not wanted_blocker:
                stats['false_blocked_cases'].append(task)
            if wanted_blocker and not actual_blocker:
                stats['missed_blocker_cases'].append(task)
            stats['cases'][task] = {'expected_verdict': oracle['verdict'],
                                   'actual_verdict': review['verdict'],
                                   'score': report['per_pair'][f'{agent}/{task}']}
        result['agents'][agent] = stats
    result['total_task_cost_usd'] = sum(s['cost_usd'] for s in result['agents'].values())
    result['total_task_seconds'] = sum(s['task_seconds'] for s in result['agents'].values())
    (run / 'benchmark-summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Agent      Aggregate  Verdict*  Findings  Gates  Summary  False blockers  Cost')
    for agent, s in result['agents'].items():
        d = s['dimensions']
        print(f"{agent:10} {s['aggregate']:8.1%}  {s['verdict_matches']:2}/{len(expected)}     "
              f"{d['findings']:7.1%}  {d['gates']:5.1%}  {d['summary']:7.1%}  "
              f"{len(s['false_blocked_cases']):14}  ${s['cost_usd']:.4f}")
    print('* Literal verdict accuracy, independently of schema failures; review the text to confirm correctness.')
    print(f"Total reported task cost ${result['total_task_cost_usd']:.4f}; preflights excluded.")


if __name__ == '__main__':
    main()
