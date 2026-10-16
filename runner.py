#!/usr/bin/env python3
"""Host-side fixture adapter and deterministic PATS scorers (standard library)."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

from fixtures import CASES

ROOT = Path(__file__).resolve().parent
SKILL = '.agents/skills/code-review/SKILL.md'
REVISIONS = {'baseline': '63a27d3b', 'ppa': 'e996ff5e', 'candidate': '508d7346', 'revised': '6f3e7815'}
DIMENSIONS = ('verdict', 'findings', 'gates', 'summary')


def prepare(agent, task, workdir, output):
    workdir.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / 'snapshots' / 'manifest.json').read_text())
    data = (ROOT / 'snapshots' / agent / 'SKILL.md').read_bytes()
    if hashlib.sha256(data).hexdigest() != manifest[agent]['sha256']:
        raise ValueError('Skill snapshot checksum mismatch')
    files = dict(CASES[task])
    files[SKILL] = data.decode()
    for relative, text in files.items():
        path = workdir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    # Retain the exact input bundle outside the sandbox for later human audit.
    shutil.copytree(workdir, output / 'inputs', dirs_exist_ok=True)
    shutil.copyfile(ROOT / 'prompt.md', output / 'prompt.md')
    (output / 'skill-version.json').write_text(json.dumps(manifest[agent], indent=2) + '\n')


def evaluate(review, expected, files):
    """Score exact outcomes separately; citations are structural, not semantic proof."""
    scores = dict.fromkeys(DIMENSIONS, 0.0)
    if not isinstance(review, dict) or review.get('scope') != 'local':
        return scores
    if (review.get('verdict') not in ('Approve', 'Comment', 'Request changes')
            or not isinstance(review.get('findings'), list)
            or not isinstance(review.get('gates'), dict)
            or any(review['gates'].get(k) not in ('pass', 'fail', 'n/a', 'not-assessed')
                   for k in expected['gates'])
            or review.get('comparison') not in ('assessed', 'not-assessed')
            or not isinstance(review.get('changes'), list)
            or not all(isinstance(c, str) and c in
                       ('parts', 'services', 'packages', 'scripts', 'version', 'repositories')
                       for c in review['changes'])
            or not isinstance(review.get('summary'), str) or not review['summary'].strip()):
        return scores
    for finding in review['findings']:
        if (not isinstance(finding, dict)
                or finding.get('category') not in ('ppa-provenance', 'eol-cap', 'recipe-regression', 'other')
                or finding.get('severity') not in ('blocker', 'nit')
                or not isinstance(finding.get('message'), str) or not finding['message'].strip()
                or not isinstance(finding.get('evidence'), list) or not finding['evidence']):
            return scores
        for cite in finding['evidence']:
            if (not isinstance(cite, dict) or not isinstance(cite.get('path'), str)
                    or type(cite.get('line')) is not int):
                return scores
    scores['verdict'] = float(review.get('verdict') == expected['verdict'])
    findings = review.get('findings')
    if isinstance(findings, list):
        actual = []
        valid = True
        for finding in findings:
            if not isinstance(finding, dict):
                valid = False
                break
            actual.append((finding.get('category'), finding.get('severity')))
            evidence = finding.get('evidence')
            if not isinstance(finding.get('message'), str) or not finding['message'].strip():
                valid = False
            if not isinstance(evidence, list) or not evidence:
                valid = False
                continue
            for cite in evidence:
                if not isinstance(cite, dict):
                    valid = False
                    continue
                path, line = cite.get('path'), cite.get('line')
                if (not isinstance(path, str) or path not in files or type(line) is not int
                        or not 1 <= line <= len(files[path].splitlines())):
                    valid = False
        wanted = [(f['category'], f['severity']) for f in expected['findings']]
        scores['findings'] = float(valid and len(actual) == len(wanted)
                                   and all(actual.count(f) == wanted.count(f) for f in wanted))
    gates = review.get('gates')
    if isinstance(gates, dict):
        scores['gates'] = sum(gates.get(k) == v for k, v in expected['gates'].items()) / len(expected['gates'])
    changes = review.get('changes')
    if isinstance(changes, list) and all(isinstance(x, str) for x in changes):
        scores['summary'] = float(
            review.get('comparison') == expected['comparison']
            and len(changes) == len(set(changes))
            and set(changes) == set(expected['changes'])
            and isinstance(review.get('summary'), str) and bool(review['summary'].strip()))
    return scores


def score(task, output, dimension):
    expected = json.loads((ROOT / 'expectations.json').read_text())[task]
    try:
        metadata = json.loads((output / 'metadata.json').read_text())
        if metadata.get('status') != 'ok' or metadata.get('exit_code') != 0:
            return 0.0
        if not (output / 'review.md').read_text().strip():
            return 0.0
        review = json.loads((output / 'review.json').read_text())
        return evaluate(review, expected, CASES[task])[dimension]
    except (OSError, ValueError, TypeError, AttributeError):
        return 0.0


def audit(run):
    report = json.loads((run / 'scores.json').read_text())
    cells = [(c['agent'], c['task'], c['scorer']) for c in report['cells']]
    wanted = {(a, t, s) for a in REVISIONS for t in CASES for s in DIMENSIONS}
    if len(cells) != len(wanted) or set(cells) != wanted:
        raise ValueError(f'Incomplete score matrix: {len(cells)} cells, expected {len(wanted)}')
    for agent in REVISIONS:
        for task in CASES:
            output = run / agent / task
            metadata = json.loads((output / 'metadata.json').read_text())
            if metadata.get('status') != 'ok' or metadata.get('exit_code') != 0:
                raise ValueError(f'Failed execution: {agent}/{task}')
            for name in ('review.md', 'review.json'):
                if not (output / name).read_text().strip():
                    raise ValueError(f'Missing output: {agent}/{task}/{name}')
    print(f'Complete matrix: {len(REVISIONS) * len(CASES)} successful executions, {len(wanted)} score cells. Inspect review text before drawing conclusions.')


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'audit':
        audit(Path(sys.argv[2]).resolve())
    else:
        task = os.environ['PATS_TASK_ID']
        output = Path(os.environ['PATS_OUTPUT_DIR'])
        if action == 'prepare':
            prepare(os.environ['PATS_AGENT_ID'], task, Path(os.environ['PATS_WORKDIR']), output)
        elif action == 'collect':
            for name in ('review.md', 'review.json'):
                source = Path(os.environ['PATS_WORKDIR']) / name
                if source.is_file():
                    shutil.copyfile(source, output / name)
        elif action == 'score':
            print(score(task, output, os.environ['PATS_SCORER_ID']))
        else:
            raise SystemExit(f'Unknown action: {action}')
