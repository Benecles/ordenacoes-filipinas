"""Table-driven behavioral coverage for the Portuguese slop linter."""
import os
import json
import subprocess
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.dirname(__file__))
from slop_lint import HARD, RATE, lint, text_of

# Varied, deliberately neutral filler makes every RATE fixture eligible without
# accidentally repeating a rule trigger. 56 short sentences exceed all gates.
FILLER = " ".join(
    f"{start} consta no processo e orienta a leitura dos autos."
    for start in ["A norma", "O juízo", "A parte", "O pedido", "A prova", "O prazo", "A decisão"] * 8
)

RATE_CASES = {
    "contrast-tail": (
        "A regra vale para o autor, não para o réu. O efeito é de preclusão, nunca de nulidade. " + FILLER,
        "A regra vale para o autor. O efeito é de preclusão. " + FILLER,
    ),
    "manner-tag": (
        "O juiz lê os autos, folha por folha. A prova é examinada, cuidadosamente. " + FILLER,
        "O juiz lê os autos. A prova é examinada. " + FILLER,
    ),
    "ai-vocab-pt": (
        "O mecanismo é crucial e fundamental. A garantia é essencial e robusta. O panorama é abrangente e notável. " + FILLER,
        "O mecanismo fixa o prazo. A garantia protege o réu. O sistema cobre três instâncias. " + FILLER,
    ),
    "negative-parallelism": (
        "A medida não é definitiva. O ato não é nulo. A regra não é geral. O prazo não é fatal. " + FILLER,
        "A medida é provisória. O ato é anulável. A regra é especial. O prazo é dilatório. " + FILLER,
    ),
    "negated-inference": (
        "A declaração não prova a solução. O plano não basta. A ordem não substitui a política. " + FILLER,
        "A declaração registra o problema. O plano fixa metas. A ordem distribui deveres. " + FILLER,
    ),
    "gap-talk": (
        "O excerto não informa a data. A decisão não indica o meio. Sem esse dado, não cabe supor a confissão. " + FILLER,
        "A decisão fixa a data em 15 de janeiro. O autor junta a impugnação. O juiz examina a confissão. " + FILLER,
    ),
    "stacked-questions": (
        "Quem decide o plano? Quem paga a conta? A Corte responde em seguida. Quem fiscaliza a execução? Quem presta contas? " + FILLER,
        "A Corte decide quem fiscaliza a execução e quem presta contas. " + FILLER,
    ),
    "transition-opener": (
        "Além disso, a norma fixa o prazo.\nAdemais, o juízo examina a prova.\nContudo, a parte recorre.\nNo entanto, o pedido segue.\n" + FILLER,
        "A norma fixa o prazo.\nO juízo examina a prova.\nA parte recorre.\n" + FILLER,
    ),
    "uniform-paragraphs": (
        "\n".join(["A norma fixa o prazo e o juízo examina a prova com cuidado antes de decidir o pedido da parte, que recorre quando entende que a decisão viola a lei aplicável ao caso concreto, e o tribunal revê o mérito em seguida com base nos autos e nas provas juntadas pela parte."] * 10) + "\n" + FILLER,
        "\n".join(["A norma fixa o prazo.", "O juízo examina a prova com cuidado antes de decidir o pedido da parte, que recorre quando entende que a decisão viola a lei aplicável ao caso concreto, e o tribunal revê o mérito em seguida com base nos autos e nas provas juntadas pela parte, ouvindo o Ministério Público e as demais partes interessadas antes de proferir o acórdão final.", "A parte recorre.", "O tribunal decide em seguida com base nos autos e nas provas juntadas pela parte, que recorre quando entende que a decisão viola a lei."]) + "\n" + FILLER,
    ),
    "staged-reveal": (
        "A regra define o alcance. O ponto central é este: a decisão limita o pedido. "
        "A norma organiza o exame. A consequência é esta: o juiz verifica o prazo. " + FILLER,
        "A lei fixa o prazo aplicável ao pedido. O juiz examina os documentos juntados. " + FILLER,
    ),
    "denial-restatement": (
        "A medida não elimina o dever, mas desloca o momento do cumprimento. "
        "O ato não extingue o direito, mas altera o modo de exercício. " + FILLER,
        "A medida preserva o dever e define outro momento para o cumprimento. "
        "O ato mantém o direito e disciplina seu exercício. " + FILLER,
    ),
    "rather-than": (
        "A parte age em vez de aguardar. O juízo decide ao invés de suspender. " + FILLER,
        "A parte aguarda a intimação. O juízo suspende o feito. " + FILLER,
    ),
    "triad-density": (
        "A lei exige registro, publicação e comunicação. A norma prevê prazo, forma e recurso. "
        "O pedido exige identificação, assinatura e protocolo. " + FILLER,
        "A lei exige registro e publicação. A norma prevê prazo e recurso. " + FILLER,
    ),
    "stance-adverb": (
        "A medida é meramente formal. O ato foi simplesmente comunicado. " + FILLER,
        "A medida tem forma definida. O ato foi comunicado às partes. " + FILLER,
    ),
    "negation-chain": (
        "O pedido foi feito sem prazo, sem assinatura, sem comprovante. "
        "O ato ocorreu sem aviso, sem registro, sem justificativa. " + FILLER,
        "O pedido foi feito com prazo, assinatura e comprovante. "
        "O ato ocorreu após aviso e registro. " + FILLER,
    ),
    "same-opener-run": (
        "Norma define o prazo. Norma indica a forma. Norma delimita o efeito. "
        "A sentença foi juntada aos autos. "
        "Norma define outro prazo. Norma indica outra forma. Norma delimita outro efeito. " + FILLER,
        "A lei define o prazo. O juízo indica a forma. A parte delimita o pedido. " + FILLER,
    ),
    "semicolon-correction": (
        "A norma fixa o prazo; mas a decisão altera a contagem. "
        "O ato reconhece o pedido; na verdade, limita seu alcance. " + FILLER,
        "A norma fixa o prazo e o juízo conta os dias úteis. "
        "O ato reconhece o pedido e a decisão delimita seu alcance. " + FILLER,
    ),
    "colon-appositive": (
        "O requisito é: prova documental suficiente. A competência consiste em: julgamento do recurso. " + FILLER,
        "O requisito exige prova documental suficiente. A competência permite julgar o recurso. " + FILLER,
    ),
    "nominalisation-pileup": (
        "A implementação da verificação da execução cabe ao órgão. "
        "A realização da análise da aplicação depende do relator. " + FILLER,
        "O órgão implementa a verificação da execução. O relator analisa a aplicação. " + FILLER,
    ),
}

HARD_CASES = {
    "tool-artifact": ("Veja a fonte citeturn0search1 sobre o caso.", "Veja a fonte sobre o caso."),
    "placeholder": ("O prazo é de [inserir prazo] dias.", "O prazo é de quinze dias."),
    "chat-scaffolding": ("Espero que isso ajude na revisão.", "A revisão cobre as Aulas 02 a 09."),
    "ai-self-reference": ("Como modelo de linguagem, resumo a decisão.", "O resumo da decisão segue abaixo."),
    "ritual-conclusion": ("Em suma, a Corte manteve o prazo.", "A Corte manteve o prazo."),
    "challenges-future": ("Apesar dos desafios, o sistema avançou.", "O sistema reduziu a fila em 30% em 2019."),
    "evaluative-tail": ("A Corte manteve o prazo, o que demonstra rigor.", "A Corte manteve o prazo de quinze dias."),
    "count-announce": ("Há três razões para isso. A primeira é o prazo.", "A primeira razão é o prazo."),
    "analogy-coach": ("Pense no controle difuso como uma rede de vigias.", "No controle difuso, qualquer juiz afasta a lei no caso."),
    "where-it-lives": ("É aí que mora o problema da execução.", "O problema está na execução."),
    "invented-label": ("A Corte caiu no paradoxo da supervisão.", "A Corte supervisionou o cumprimento por cinco anos."),
    "stakes-inflation": ("A decisão muda tudo no direito penal.", "A decisão fixou o prazo prescricional."),
    "teaser-hook": ("O resultado? A Corte manteve a decisão.", "A Corte manteve a decisão."),
    "self-labeling": ("Esse é o ponto central da decisão.", "A decisão fixa o prazo."),
    "hedge-stack": ("A regra pode potencialmente afastar o prazo.", "A regra pode afastar o prazo."),
    "false-concession": ("Embora a reforma tenha avançado, a execução continua um desafio.", "A reforma criou o fundo em 2015; a execução caiu 40% em 2016."),
    "staged-objection": ("Alguém poderia objetar que a anistia encerrou o caso.", "Eros Grau sustentou que a anistia integrou a transição."),
    "reader-steer-question": ("O que isso significa? A Corte manteve o prazo.", "A Corte manteve o prazo."),
    "circular-because": ("A Corte interveio porque havia necessidade de intervenção.", "A Corte interveio porque as autoridades descumpriram a T-153."),
    "puffery": ("A regra desempenha papel fundamental no sistema.", "A regra define o prazo do recurso."),
    "significance-gerund": ("A regra foi aplicada, evidenciando a importância do tema.", "A regra foi aplicada ao caso concreto."),
    "formulaic-metatext": ("Vale destacar que o prazo começou ontem.", "O prazo começou ontem."),
    "vague-attribution": ("Muitos autores afirmam que o prazo é curto.", "O prazo é de quinze dias."),
    "reader-address": ("Perceba que o prazo termina hoje.", "O prazo termina hoje."),
    "AI-calque": ("A decisão oferece abordagem robusta para navegar pelo cenário atual.", "A decisão organiza o exame dos fatos."),
    "backstage": ("Os slides apresentam o tema nesta leitura.", "O tema aparece no primeiro capítulo."),
    "rhetorical-triad": ("A regra protege forma, prazo e, sobretudo, segurança.", "A regra protege forma, prazo e segurança."),
}


def run_text(text, budget=None):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as f:
        f.write(text)
        path = f.name
    try:
        return lint(path, budget)
    finally:
        os.unlink(path)


class LinterRulesTest(unittest.TestCase):
    def test_rule_inventory_has_examples(self):
        self.assertEqual(set(HARD), set(HARD_CASES))
        self.assertEqual(set(RATE) - {"paren-scarcity"}, set(RATE_CASES))

    def test_hard_rules_positive_and_negative(self):
        for rule, (positive, negative) in HARD_CASES.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, {f["rule"] for f in run_text(positive)["findings"]})
                self.assertNotIn(rule, {f["rule"] for f in run_text(negative)["findings"]})

    def test_rate_rules_positive_and_negative(self):
        for rule, (positive, negative) in RATE_CASES.items():
            with self.subTest(rule=rule):
                result = run_text(positive)
                self.assertGreaterEqual(result["words"], 250)
                self.assertGreaterEqual(result["sentences"], 5)
                self.assertGreaterEqual(sum(f["rule"] == rule for f in result["findings"]), 2)
                self.assertNotIn(rule, {f["rule"] for f in run_text(negative)["findings"]})

    def test_paren_scarcity_absence_signal(self):
        no_parens = run_text(FILLER)
        with_parens = run_text("Esta regra (com explicação útil) orienta a leitura. " + FILLER)
        self.assertGreaterEqual(no_parens["words"], 250)
        self.assertGreaterEqual(no_parens["sentences"], 5)
        self.assertIn("paren-scarcity", {f["rule"] for f in no_parens["findings"]})
        self.assertNotIn("paren-scarcity", {f["rule"] for f in with_parens["findings"]})

    def test_d9_hard_and_rate_patterns_match_natural_examples(self):
        rhetorical = run_text("A lei prevê três requisitos e, sobretudo, organiza seu exame.")["findings"]
        self.assertIn("rhetorical-triad", {f["rule"] for f in rhetorical})


    def test_minimum_gates_and_explicit_failure_budget(self):
        one_hit = "A medida não elimina o dever, mas desloca o cumprimento. " + FILLER
        two_short = "A medida não elimina o dever, mas desloca o cumprimento. " * 2
        two_few_sentences = ("A medida não elimina o dever, mas desloca o cumprimento, "
                             "e a norma define o prazo. " * 2)
        self.assertNotIn("denial-restatement", {f["rule"] for f in run_text(one_hit)["findings"]})
        self.assertNotIn("denial-restatement", {f["rule"] for f in run_text(two_short)["findings"]})
        self.assertNotIn("denial-restatement", {f["rule"] for f in run_text(two_few_sentences)["findings"]})
        review = run_text(FILLER, budget=0)
        self.assertGreater(review["finding_count"], 0)
        self.assertEqual(review["status"], "FAIL")

    def test_json_cli_includes_density_summary(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as f:
            f.write("A medida não elimina o dever, mas desloca o cumprimento. "
                    "O ato não extingue o direito, mas altera o modo de exercício. " + FILLER)
            path=f.name
        try:
            result=subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "slop_lint.py"), path, "--json"],
                                  check=True, capture_output=True, text=True)
            data=json.loads(result.stdout)["files"][0]
            self.assertIn("denial-restatement", data["density"])
            self.assertIn("per_1000", data["density"]["denial-restatement"])
            self.assertEqual(data["status"], "PASS")
        finally:
            os.unlink(path)

    def test_false_positive_contexts_remain_flagged_for_review(self):
        # These are intentional legal constructions; lint findings are prompts.
        legal = run_text("A regra não reduz o dano, mas desloca o ônus. O ato não extingue o direito, mas muda seu exercício. " + FILLER)
        statutory = run_text("A lei exige registro, publicação e comunicação. "
                             "A norma exige prazo, forma e recurso. " + FILLER)
        enumerated = run_text("O pedido requer identificação, assinatura e protocolo. "
                              "O procedimento exige presença, declaração e assinatura. " + FILLER)
        self.assertIn("denial-restatement", {f["rule"] for f in legal["findings"]})
        self.assertIn("triad-density", {f["rule"] for f in statutory["findings"]})
        self.assertIn("triad-density", {f["rule"] for f in enumerated["findings"]})


if __name__ == "__main__":
    unittest.main()


# 06/10 adversarial false-positive set (adewale discipline): legitimate legal prose that must raise no HARD *tell*.
ADVERSARIAL = [
    "A resposta tardia não forma contrato, mas vale como nova proposta.",
    "O art. 5º, LV, assegura o contraditório, a ampla defesa e os recursos a ela inerentes.",
    "Imagine que um Estado edite lei retroativa: o juiz deve afastá-la no caso concreto.",
    "O STF, por seis votos a cinco, manteve a interpretação da Lei 6.683/1979.",
    "A Corte declarou o estado de coisas inconstitucional e fixou prazos para as autoridades.",
    "Como dispõe o art. 421 do Código Civil, a liberdade contratual será exercida nos limites da função social.",
    "O relator, Eros Grau, sustentou que a anistia integrou a transição.",
    "A sentença não anulou o referendo; o efeito prático, porém, foi liberar a candidatura.",
]

class AdversarialTest(unittest.TestCase):
    def test_legal_prose_raises_no_hard_tell(self):
        from slop_lint import STYLE
        for sentence in ADVERSARIAL:
            with self.subTest(sentence=sentence):
                hard = {f["rule"] for f in run_text(sentence)["findings"] if f.get("severity") == "hard" and f["rule"] not in STYLE}
                self.assertEqual(hard, set())

    def test_holdout_human_false_alarms_when_corpus_present(self):
        bench = os.path.join(os.path.dirname(__file__), "..", "..", "work", "slop-bench")
        sys.path.insert(0, bench)
        try:
            import backtest
            docs = backtest.human_docs("holdout")
        except Exception:
            docs = []
        if len(docs) < 50:
            self.skipTest("human holdout corpus not on this machine (git-ignored chapters)")
        from slop_lint import STYLE
        counts = {}
        for _, text in docs:
            fired = {f["rule"] for f in run_text(text)["findings"] if (f.get("severity") == "hard" or f.get("over_limit")) and f["rule"] not in STYLE}
            for rule in fired: counts[rule] = counts.get(rule, 0) + 1
        worst = {r: n / len(docs) for r, n in counts.items() if n / len(docs) > 0.12}
        self.assertEqual(worst, {}, "tell rules alarming on >12% of held-out human doctrine")


class TackedOnTailTest(unittest.TestCase):
    """D11 (chairman 09/10): the construction, not a phrase list."""
    PAD = " O juiz recebeu a petição inicial e mandou citar o réu no prazo legal." * 40

    def rules(self, text):
        return [f["rule"] for f in run_text(text + self.PAD)["findings"]]

    def test_contrast_tail_fires(self):
        text = "A regra vale para o autor, não para o réu. O efeito é de preclusão, nunca de nulidade."
        self.assertEqual(self.rules(text).count("contrast-tail"), 2)

    def test_manner_tag_fires_on_unlisted_shapes(self):
        text = "O juiz lê os autos, folha por folha. A prova é examinada, cuidadosamente."
        self.assertEqual(self.rules(text).count("manner-tag"), 2)

    def test_informative_endings_stay_quiet(self):
        text = "O prazo conta em dobro, respectivamente. A parte não foi citada. O réu contestou com base no art. 335."
        rules = self.rules(text)
        self.assertNotIn("manner-tag", rules)
        self.assertNotIn("contrast-tail", rules)


class VerbatimTextTest(unittest.TestCase):
    """25/10: exam stems, options, case strips and source blocks are quoted text; the lint must not ask to reshape them."""
    def test_quoted_elements_leave_the_linted_text(self):
        page = ('<html lang="pt"><body><div class="prosa"><p>A parte cita o réu.</p></div>'
                '<section class="bank-question"><p class="pergunta">3. Assinale a correta:\na) Cachoeirinha, exclusivamente.</p>'
                '<details><summary>Gabarito comentado</summary><p>A resposta é a, pelo foro do domicílio.</p></details></section>'
                '<div class="bet"><p class="bet-q">Florinda pede a nulidade.</p><div class="bet-opts"><button>a) Alvorada, exclusivamente.</button></div>'
                '<div class="bet-reveal"><p>A alternativa a é correta.</p></div></div>'
                '<div class="exam"><p>7. Acerca da prova, assinale:</p></div><span class="exam-id">Prova 2015</span>'
                '<blockquote><p>Citado, o réu não contestou.</p></blockquote><aside class="fonte dec"><p>STJ, REsp 1.</p></aside></body></html>')
        with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as f:
            f.write(page)
        try:
            text = text_of(f.name)
        finally:
            os.unlink(f.name)
        for ours in ("A parte cita o réu", "pelo foro do domicílio", "A alternativa a é correta", "Prova 2015"):
            self.assertIn(ours, text)
        for quoted in ("exclusivamente", "Florinda", "Acerca da prova", "não contestou", "REsp"):
            self.assertNotIn(quoted, text)
