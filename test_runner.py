"""Offline validation of fixture isolation and scoring, not model behavior."""

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import subprocess
import unittest

from fixtures import CASES
from runner import DIMENSIONS, REVISIONS, ROOT, SKILL, evaluate, prepare, score


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.expected = json.loads((ROOT / 'expectations.json').read_text())

    def answer(self, task):
        answer = copy.deepcopy(self.expected[task])
        answer.update(scope='local', summary='Synthetic scorer self-test; not a model answer.')
        for finding in answer['findings']:
            finding.update(message='Synthetic finding.', evidence=[{'path': 'context.md', 'line': 1}])
        return answer

    def test_published_cases_match_generator(self):
        for task, files in CASES.items():
            root = ROOT / 'cases' / task
            actual = {p.relative_to(root).as_posix(): p.read_text()
                      for p in root.rglob('*') if p.is_file()}
            self.assertEqual(actual, files)

    def test_published_artifacts_unchanged(self):
        hashes = json.loads((ROOT / 'results/artifact-checksums.json').read_text())
        for name, digest in hashes.items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest, name)

    def test_published_scores_reproduce(self):
        for label in ('round-one', 'round-two'):
            run = ROOT / 'results' / label
            recorded = json.loads((run / 'scores.json').read_text())
            for cell in recorded['cells']:
                self.assertEqual(score(cell['task'], run / cell['agent'] / cell['task'], cell['scorer']), cell['score'])

    def test_case_matrix(self):
        self.assertEqual(set(CASES), {f'case-{n:02}' for n in range(1, 13)})
        self.assertEqual(set(CASES), set(self.expected))
        for task, files in CASES.items():
            self.assertIn('2026-10-16', files['context.md'])
            self.assertIn('a/oci/demo/image.yaml', files['changes.diff'])
            self.assertIn('b/oci/demo/image.yaml', files['changes.diff'])
            self.assertEqual('recipes/before/rockcraft.yaml' in files, task != 'case-12')
            self.assertEqual('recipes/after/rockcraft.yaml' in files, task != 'case-12')
            for path in files:
                self.assertFalse(Path(path).is_absolute())
                self.assertNotIn('..', Path(path).parts)
            for path, text in files.items():
                if path.endswith('rockcraft.yaml'):
                    self.assertIn('override-prime: gen_manifest', text)

    def test_targeted_deltas(self):
        before = lambda task: CASES[task]['recipes/before/rockcraft.yaml']
        after = lambda task: CASES[task]['recipes/after/rockcraft.yaml']
        self.assertNotIn('package-repositories:', before('case-01'))
        self.assertIn('package-repositories:', after('case-01'))
        self.assertEqual(before('case-03'), before('case-05'))
        self.assertEqual(after('case-03'), after('case-05'))
        self.assertNotIn('\n-    commit:', CASES['case-04']['changes.diff'])
        self.assertIn('-    directory: rocks/old', CASES['case-04']['changes.diff'])
        for task, removed in [('case-06', '      - tini\n'), ('case-07', '      - libgomp1_libs\n')]:
            self.assertEqual(before(task).replace(removed, ''), after(task))
        self.assertEqual(before('case-08').replace('0750', '0700').replace('584792:584792', '0:0'), after('case-08'))
        self.assertEqual(before('case-11').replace('1.2.0', '1.2.1'), after('case-11'))

    def test_positive_answers(self):
        for task in CASES:
            with self.subTest(task=task):
                self.assertEqual(evaluate(self.answer(task), self.expected[task], CASES[task]), dict.fromkeys(DIMENSIONS, 1.0))

    def test_wrong_verdict(self):
        for task in CASES:
            answer = self.answer(task)
            answer['verdict'] = 'Comment' if answer['verdict'] != 'Comment' else 'Approve'
            self.assertEqual(evaluate(answer, self.expected[task], CASES[task])['verdict'], 0)

    def test_incomplete_schema(self):
        answer = self.answer('case-05')
        for key in ('scope', 'verdict', 'findings', 'gates', 'comparison', 'changes', 'summary'):
            incomplete = dict(answer)
            del incomplete[key]
            self.assertEqual(evaluate(incomplete, self.expected['case-05'], CASES['case-05']), dict.fromkeys(DIMENSIONS, 0.0))

    def test_false_blocker_and_missed_finding(self):
        for task in CASES:
            answer = self.answer(task)
            if answer['findings']:
                answer['findings'] = []
            else:
                answer['findings'] = [{'category': 'eol-cap', 'severity': 'blocker', 'message': 'Invented',
                                       'evidence': [{'path': 'context.md', 'line': 1}]}]
            self.assertEqual(evaluate(answer, self.expected[task], CASES[task])['findings'], 0)
        answer = self.answer('case-01')
        answer['findings'][0]['severity'] = 'blocker'
        self.assertEqual(evaluate(answer, self.expected['case-01'], CASES['case-01'])['findings'], 0)

    def test_invalid_citations(self):
        for cite in [{'path': 'missing', 'line': 1}, {'path': 'context.md', 'line': 99999},
                     {'path': 'context.md', 'line': True}, {'path': '../expectations.json', 'line': 1}]:
            answer = self.answer('case-06')
            answer['findings'][0]['evidence'] = [cite]
            self.assertEqual(evaluate(answer, self.expected['case-06'], CASES['case-06'])['findings'], 0)

    def test_fabricated_assessment(self):
        answer = self.answer('case-12')
        answer.update(comparison='assessed', changes=['version'])
        answer['gates'] = dict.fromkeys(answer['gates'], 'pass')
        actual = evaluate(answer, self.expected['case-12'], CASES['case-12'])
        self.assertEqual(actual['gates'], 0)
        self.assertEqual(actual['summary'], 0)

    def test_isolation_and_snapshots(self):
        for agent in REVISIONS:
            for task in CASES:
                with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
                    work, output = Path(tmp) / 'work', Path(tmp) / 'output'
                    prepare(agent, task, work, output)
                    actual = {p.relative_to(work).as_posix() for p in work.rglob('*') if p.is_file()}
                    self.assertEqual(actual, set(CASES[task]) | {SKILL})
                    self.assertFalse((work / 'expectations.json').exists())
                    self.assertTrue((output / 'inputs' / 'context.md').is_file())
                    self.assertEqual((output / 'prompt.md').read_text(), (ROOT / 'prompt.md').read_text())
                    self.assertIn('directly-pulled', (work / SKILL).read_text())

    def test_missing_malformed_and_failed_outputs(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            output = Path(tmp)
            for dimension in DIMENSIONS:
                self.assertEqual(score('case-01', output, dimension), 0)
            (output / 'metadata.json').write_text('{"status":"ok","exit_code":0}')
            (output / 'review.md').write_text('Synthetic review\n')
            (output / 'review.json').write_text('not JSON')
            self.assertEqual(score('case-01', output, 'verdict'), 0)
            (output / 'review.json').write_text(json.dumps(self.answer('case-01')))
            self.assertEqual(score('case-01', output, 'verdict'), 1)
            (output / 'metadata.json').write_text('{"status":"failed","exit_code":1}')
            self.assertEqual(score('case-01', output, 'verdict'), 0)

    def test_pats_scoring_integration(self):
        # Synthetic answers exercise PATS orchestration only; no agent is run.
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            run = Path(tmp)
            for agent in REVISIONS:
                for task in CASES:
                    output = run / agent / task
                    output.mkdir(parents=True)
                    (output / 'metadata.json').write_text('{"status":"ok","exit_code":0}')
                    (output / 'review.md').write_text('Synthetic scorer validation, not a model review.\n')
                    (output / 'review.json').write_text(json.dumps(self.answer(task)))
            result = subprocess.run(
                [os.environ.get('PATS_BIN', 'pats'), '-c', str(ROOT / 'pats.yaml'),
                 'score', '-s', 'full', '-r', str(run)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((run / 'scores.json').read_text())
            self.assertEqual(len(report['cells']), len(REVISIONS) * len(CASES) * len(DIMENSIONS))
            self.assertTrue(all(cell['score'] == 1 for cell in report['cells']))


if __name__ == '__main__':
    unittest.main()
