import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(__file__))
from marks_lint import check

def run(html):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f: f.write('<body>' + html + '</body>')
    try: return {r for _, r, _ in check(f.name)}
    finally: os.unlink(f.name)

class T(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(run('<section class="chapter"><p>A <span class="held">carecem de efeitos</span> e <span class="limit">não cria direito</span>.</p><p><span class="mark">Frase.</span></p></section>'), set())
    def test_two_held(self):
        self.assertIn('held-per-paragraph', run('<p><span class="held">a</span> e <span class="held">b</span></p>'))
    def test_too_long(self):
        self.assertIn('limit-too-long', run('<p><span class="limit">um dois três quatro cinco seis sete oito nove</span></p>'))
    def test_two_marks_one_chapter(self):
        self.assertIn('mark-per-chapter', run('<section class="chapter"></section><p><span class="mark">a</span></p><p><span class="mark">b</span></p>'))
    def test_term_needs_def(self):
        self.assertIn('term-no-def', run('<p><span class="term">x</span></p>'))
    def test_plain_bold(self):
        self.assertIn('plain-bold', run('<p>veja <strong>isto</strong></p>'))
    def test_bold_ok_in_eixo_and_deck(self):
        self.assertEqual(run('<p class="deck">x <strong class="conc">y</strong></p><p class="eixo"><b>Eixo</b>z</p>'), set())
    def test_inline_colour(self):
        self.assertIn('inline-colour', run('<p><span style="color:red">x</span></p>'))
if __name__ == '__main__': unittest.main()
