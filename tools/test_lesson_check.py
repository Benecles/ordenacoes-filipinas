"""Offline behavior tests: python3 -m unittest tools.test_lesson_check."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import lesson_check as lc
from tools.shell import shell


def frame(body='', lang='pt-BR'):
    scripts = ''.join(f'<script src="../../assets/{s}?v=123" defer></script>' for s in lc.SCRIPTS)
    return f'<html lang="{lang}"><head>{scripts}</head><body><button class="theme-toggle">Modo noite</button>{body}</body></html>'


class CounterTests(unittest.TestCase):
    def test_disjoint_categories_and_nested_inline_words(self):
        source = '''<h1>Título</h1><section class="wide chapter" id="one"><h2>Capítulo um</h2>
        <p>Uma peti<em>ção</em> inicial.</p><aside class="dec fonte"><blockquote>Uma fonte.</blockquote></aside>
        <blockquote>Outra fonte.</blockquote><figure><svg><text>Figura</text></svg><figcaption>Legenda</figcaption><blockquote>Citação desenhada</blockquote></figure>
        </section><p>Fim.</p>'''
        r = lc.word_report(source)
        self.assertEqual(r['chapters'][0], {'id': 'one', 'title': 'Capítulo um', 'own_prose': 5, 'quotations': 4, 'figure_text': 4, 'total': 13})
        self.assertEqual(r['outside_chapters']['own_prose'], 2)
        self.assertEqual(r['totals']['total'], 15)

    def test_hidden_and_nonreader_text_excluded(self):
        r = lc.word_report('''<head><title>Title</title></head><style>style</style><script>script</script>
        <nav>Menu</nav><template>Template</template><div hidden>Arquivo</div>
        <p style="display: none">Invisível</p>
        <!-- comment --><p>Visível &amp; chão</p>''')
        self.assertEqual(r['totals'], dict(own_prose=2, quotations=0, figure_text=0, total=2))

    def test_verbatim_exam_is_not_authored(self):
        r = lc.word_report('<p>Comentário.</p><div class="verbatim"><p class="bet-q">Pergunta?</p><ol><li>Opção.</li></ol></div><aside class="exam-ground">Fundamento.</aside>')
        self.assertEqual(r['totals']['own_prose'], 2)
        self.assertEqual(r['totals']['quotations'], 2)

    def test_blocks_do_not_join_and_inline_does_not_split(self):
        r = lc.word_report('<p>co<em>isa</em></p><p>outra</p><p>ação-objeto</p>')
        self.assertEqual(r['totals']['own_prose'], 4)

    def test_self_closing_svg_and_multiple_chapters(self):
        r = lc.word_report('<section class="chapter"><figure><svg><path/><text>Um</text></svg></figure><p>Dois</p></section><section class="chapter"><p>Três</p></section>')
        self.assertEqual([r['own_prose'] for r in r['chapters']], [1, 1])
        self.assertEqual(r['totals']['figure_text'], 1)


class LinterTests(unittest.TestCase):
    def test_quotes_and_figures_cannot_trigger_prose_or_marks_rules(self):
        result = lc.check(frame('''<blockquote><p>Vale ressaltar <span class="term">isto</span>.</p></blockquote>
            <figure><p>Vale ressaltar <span class="term">isto</span>.</p></figure>
            <aside class="fonte"><p>Vale ressaltar <span class="term">isto</span>.</p></aside>'''))
        self.assertFalse([f for f in result['findings'] if f['check'].startswith(('C13/', 'C24/'))])

    def test_portuguese_is_explicit_even_when_text_is_short(self):
        result = lc.check(frame('<p>Vale ressaltar o papel crucial da lei.</p>'))
        self.assertEqual(result['language'], 'pt')
        self.assertIn('C13/formulaic-metatext', {f['check'] for f in result['findings']})
        self.assertEqual(result['status'], 'PASS')  # prompts, not linguistic verdicts

    def test_english_package_import(self):
        result = lc.check(frame('<p>It is important to note that this plays a pivotal role.</p>', 'en-US'))
        self.assertEqual(result['language'], 'en')
        self.assertTrue(any(f['check'].startswith('C13/') for f in result['findings']))

    def test_mark_rules_enforced_on_own_prose(self):
        result = lc.check(frame('<p><span class="term">Prazo</span></p>'))
        self.assertIn('C24/term-no-def', {f['check'] for f in result['findings']})
        self.assertEqual(result['status'], 'FAIL')

    def test_calibrated_long_colour_and_bold_are_warnings(self):
        result = lc.check(frame('<p><strong>Regra principal</strong><span class="held">um dois três quatro cinco seis sete oito nove</span></p>'))
        self.assertEqual(result['status'], 'PASS')
        self.assertIn('C24/held-too-long', {f['check'] for f in result['findings']})


class MechanicalTests(unittest.TestCase):
    def codes(self, source):
        return {f['check'] for f in lc.check(frame(source))['findings']}

    def test_each_concrete_complaint_is_detected(self):
        cases = {
            'C02': '<p>Começar?</p><section class="chapter"></section>',
            'C20': '<p class="lede">Por quê?</p>',
            'C31': '<header class="hero"><button data-call>Escolha</button></header>',
            'C34': '<figure class="hero"><svg><animate repeatCount="indefinite"/></svg></figure>',
            'C50': '<h1>' + 'palavra ' * 20 + '</h1>',
            'C61': '<article class="bet"><h3>Prova 2018/2</h3></article>',
            'C62': '<article class="bet"></article><section class="chapter"></section>',
            'C63': '<style>p{color:#aabbcc}</style>',
            'C66': '<style>.highlight{background:orange}</style>',
            'C68': '<style>button:focus{outline:1px solid blue}</style>',
            'C69': '<svg><title>Tooltip</title><path/></svg>',
            'C73': '<figure><button data-version="two">Versão</button></figure>',
            'C75': '<p><mark>Ênfase</mark></p>',
            'C82': '<details class="exam-card"><summary>Pergunta</summary></details>',
        }
        for code, body in cases.items():
            with self.subTest(code=code):
                self.assertIn(code, self.codes(body))

    def test_highlight_scope_and_washes(self):
        self.assertNotIn('C75', self.codes('<blockquote><mark>Fonte</mark></blockquote><figure><mark>Figura</mark></figure>'))
        for body in ["<span class='highlight'>Texto</span>", '<p><em style="background-color:orange">Texto</em></p>']:
            self.assertIn('C75', self.codes(body))
        self.assertIn('C75', self.codes('<style>.wash{background:orange}</style><p><span class="wash">Texto</span></p>'))
        self.assertNotIn('C75', self.codes('<style>.key{background:orange}</style><aside class="fonte"><span class="key">Fonte</span></aside>'))
        self.assertNotIn('C75', self.codes('<style>.held{background:none}</style><span class="held" style="background:transparent">Texto</span>'))

    def test_hex_scope_does_not_confuse_ids_links_comments_or_quotes(self):
        self.assertNotIn('C63', self.codes('<style>/* color:#fff */ #abc{color:var(--ink)}</style><p id="abc">#abc</p><a href="#def">Link</a>'))
        self.assertIn('C63', self.codes("<svg><path fill='#fff'/></svg>"))

    def test_no_title_width_verdict_without_browser(self):
        r = lc.check(frame('<h1>' + 'Long title ' * 20 + '</h1>'))
        self.assertEqual(next(f for f in r['findings'] if f['check'] == 'C50')['severity'], 'warning')


class ContractTests(unittest.TestCase):
    def test_script_missing_and_duplicate_toggle_fail(self):
        for script in lc.SCRIPTS:
            with self.subTest(script=script):
                source = frame().replace(f'<script src="../../assets/{script}?v=123" defer></script>', '')
                self.assertIn('SHELL-SCRIPTS', {f['check'] for f in lc.contract(source)})
        for body in [frame().replace('class="theme-toggle"', 'class="other"'), frame('<button class="theme-toggle"></button>')]:
            self.assertIn('SHELL-TOGGLE', {f['check'] for f in lc.contract(body)})
        self.assertEqual(lc.contract(frame()), [])

    def test_each_media_branch_requires_portrait(self):
        for css in ['@media(max-width:760px){p{color:blue}}', '@media(max-width:900px) and (orientation:portrait), (max-width:700px){p{color:blue}}']:
            with self.subTest(css=css):
                r = lc.media_parity('<style>' + css + '</style>')
                self.assertTrue(r)
                self.assertIn('and (orientation:portrait)', r[0]['message'])
        for css in ['@media (max-width:760px) and (orientation:portrait){p{color:blue}}', '@media(min-width:800px){p{color:blue}}', '/* @media(max-width:100px){} */']:
            self.assertFalse(lc.media_parity('<style>' + css + '</style>'))

    def test_shell_uses_same_word_counter(self):
        with patch.object(lc, 'word_report', return_value={'totals': {'own_prose': 5000}}) as counter:
            findings = shell.lints('<p>One word</p>', 'lesson')
        counter.assert_called_once()
        self.assertTrue(any('5000 own-prose words' in f for f in findings))

    def test_shell_minimum_is_advisory_after_calibration(self):
        findings = shell.lints('<p>Texto breve</p>', 'lesson')
        self.assertTrue(any(f.startswith('WARN C53:') for f in findings))

    def test_shell_calls_lesson_checker_and_checks_all_page_contracts(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'sample.html'
            with patch.object(shell, 'SRC', Path(tmp)), contextlib.redirect_stdout(io.StringIO()):
                for kind in ['page', 'lesson']:
                    src.write_text(f'<!--shell\ncourse: processo-civil-i\nkind: {kind}\ntitle: Sample\nbar: Sample\n-->\n<p>Text</p>')
                    with patch.object(shell, 'lints', return_value=[]), patch.object(lc, 'check', wraps=lc.check) as checker:
                        _, page = shell.render(src)
                    self.assertEqual(checker.call_count, int(kind == 'lesson'))
                    self.assertFalse(lc.contract(page))
                src.write_text('<!--shell\ncourse: processo-civil-i\ntitle: Sample\nbar: Sample\n-->\n<style>@media(max-width:760px){p{color:blue}}</style>')
                with self.assertRaisesRegex(SystemExit, 'orientation:portrait'):
                    shell.render(src)

    def test_cli_json_and_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'lesson.html'
            for body, status in [('<p>Texto</p>', 0), ('<svg><title>Tooltip</title></svg>', 1)]:
                p.write_text(frame(body), encoding='utf-8')
                proc = subprocess.run([sys.executable, str(Path(lc.__file__)), str(p), '--json'], capture_output=True, text=True)
                self.assertEqual(proc.returncode, status, proc.stderr)
                result = json.loads(proc.stdout)
                self.assertEqual(result['totals']['total'], sum(result['totals'][k] for k in lc.COUNTS))


if __name__ == '__main__':
    unittest.main()
