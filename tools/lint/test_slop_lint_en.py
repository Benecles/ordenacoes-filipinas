#!/usr/bin/env python3
"""Tests for the English rule tables (CEO, 16/10). Each hard rule: one sentence that must fire, one near-miss that
must not. Plus language detection, rate rules, and a holdout on human English the limits were not tuned on."""
import glob, os, random, re, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slop_rules_en as en
from slop_lint import lint, detect

HIT_MISS = {
    'puffery': ("The turn plays a crucial role in the backstage.", "The turn flips the page over."),
    'significance-gerund': ("We shipped six blocks, highlighting the importance of sources.", "We shipped six blocks, each cut from the book."),
    'formulaic-metatext': ("It's worth noting that the crawl came back clean.", "The crawl came back clean."),
    'vague-attribution': ("Experts say figures help memory.", "Mayer's 2009 study found figures help recall."),
    'reader-address': ("You might be wondering why the page is blue.", "The page is blue because it is the back."),
    'AI-calque': ("We delve into the tapestry of Constitucional I.", "We read Constitucional I page by page."),
    'teaser-hook': ("Here's the thing. The page was grey.", "The page was grey. Here's the crop."),
    'self-labeling': ("This is where it gets interesting.", "This is where the rod ends."),
    'hedge-stack': ("It may potentially help.", "It may help, because the scan is faint."),
    'false-concession': ("While it may seem small, it is actually the biggest change.", "It is the biggest change: 34 pages."),
    'staged-objection': ("Some might say the blog is too long.", "You said the blog was hard to find."),
    'reader-steer-question': ("Why does this matter? Because the exam asks it.", "The exam asks it every year."),
    'circular-because': ("We redrew it because it needed to be redrawn.", "We redrew it because the shield had gone black."),
    'tool-artifact': ("As of my last update, the site had 427 pages.", "On 16 October the site had 427 pages."),
    'placeholder': ("The PR is [insert number].", "The PR is #310."),
    'chat-scaffolding': ("I hope this helps with the swap.", "This unblocks the swap."),
    'ai-self-reference': ("As an AI, I read the page.", "I read the page."),
    'ritual-conclusion': ("Ultimately, the blog is pinned.", "The blog is pinned on the backstage home."),
    'challenges-future': ("Only time will tell if Codex finishes.", "Codex has 11 pages left."),
    'evaluative-tail': ("The scale stays level, which is exactly the point.", "The scale stays level."),
    'count-announce': ("Here are three lessons from the night.", "The night taught me to look at pages."),
    'analogy-coach': ("Think of it like a filing cabinet.", "It files every ruling by date."),
    'where-it-lives': ("This is where the linter comes in.", "The linter checks it."),
    'invented-label': ("I fixed what I call the grey problem.", "I fixed the grey pages."),
    'stakes-inflation': ("The turn changes everything.", "The turn works on every page."),
    'rhetorical-triad': ("It shipped. Quick. Clean. Done.", "It shipped quick and clean."),
    'offer-closer': ("Want me to redraw the rod?", "I'll redraw the rod next."),
    'stock-metaphor': ("So airplane mode got tested where it lives.", "So airplane mode was tested on a phone in a car."),
    'personified-thing': ("The books speak on Constitucional I.", "The books are quoted on Constitucional I."),
    'manner-tag-en': ("The pages were redrawn, one lesson at a time.", "The pages were redrawn in 23 PRs."),
}


def lint_text(text, name='t.md'):
    d = tempfile.mkdtemp(); p = os.path.join(d, name)
    with open(p, 'w') as fh: fh.write(text)
    return lint(p, None, 'en')


class HardRules(unittest.TestCase):
    def test_every_hard_rule_has_a_case(self):
        self.assertEqual(set(HIT_MISS), set(en.HARD))

    def test_hits_and_near_misses(self):
        for rule, (hit, miss) in HIT_MISS.items():
            pat = en.HARD[rule][0]
            with self.subTest(rule=rule):
                self.assertTrue(re.search(pat, hit, re.I | re.M), f'{rule} missed: {hit}')
                self.assertFalse(re.search(pat, miss, re.I | re.M), f'{rule} false alarm: {miss}')


class RateRules(unittest.TestCase):
    FILL = ' '.join(['The page has a figure of the rod and a list of the lessons.'] * 30)

    def rate(self, rule, sentence, n=6):
        res = lint_text(self.FILL + ' ' + ' '.join([sentence] * n))
        return res['density'].get(rule, {})

    def test_house_tics_fire(self):
        for rule, s in [('rather-than', 'The page turns rather than toggles.'),
                        ('contrast-tail', 'OCR runs locally, never in the cloud.'),
                        ('authenticity-intensifier', 'It is a real blueprint now.'),
                        ('with-no', 'It shipped with no figure.'),
                        ('em-dash-density', 'The rod — the CF/88 — is drawn.'),
                        ('negated-inference', 'A count is not enough here.')]:
            with self.subTest(rule=rule):
                self.assertTrue(self.rate(rule, s).get('over_limit'), rule)

    def test_contrast_tail_keeps_copula(self):
        self.assertFalse(re.search(en.RATE['contrast-tail'][0], 'It shipped, not is.', re.I))

    def test_terms_are_masked(self):
        res = lint_text(self.FILL + ' The landscape orientation keeps fundamental rights visible.' * 3)
        self.assertNotIn('ai-vocab-en', res['density'])


class Language(unittest.TestCase):
    def test_detect(self):
        d = tempfile.mkdtemp()
        a = os.path.join(d, 'a.html'); open(a, 'w').write('<html lang="en"><body>x</body></html>')
        b = os.path.join(d, 'b.html'); open(b, 'w').write('<html lang="pt-BR"><body>x</body></html>')
        self.assertEqual(detect(a, ''), 'en'); self.assertEqual(detect(b, ''), 'pt')
        self.assertEqual(detect('c.md', 'The page and the rod that you drew with the house'), 'en')
        self.assertEqual(detect('c.md', 'A norma não produz efeitos para que uma lei'), 'pt')


class Holdout(unittest.TestCase):
    """No tell rule may alarm on more than 12% of held-out human English (the limits were tuned on a 400-doc sample)."""
    def test_holdout(self):
        here = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'work', 'slop-bench', 'en', 'corpus', 'human-legal')
        docs = sorted(glob.glob(os.path.join(here, '*.txt')))
        if len(docs) < 800: self.skipTest('English corpus absent (build_corpus.py)')
        random.seed(16); tuned = set(random.sample(docs, 400))
        held = random.Random(99).sample([d for d in docs if d not in tuned], 300)
        alarms = {}
        for p in held:
            r = lint(p, None, 'en')
            for f in r['findings']:
                if f['band'] == 'tell' and (f['severity'] == 'hard' or f.get('over_limit')):
                    alarms.setdefault(f['rule'], set()).add(p)
        worst = {k: round(100 * len(v) / len(held), 1) for k, v in alarms.items()}
        self.assertFalse({k: v for k, v in worst.items() if v > 12}, worst)


if __name__ == '__main__':
    unittest.main()
