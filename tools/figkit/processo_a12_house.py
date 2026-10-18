"""Aula 12 instruments: the P1 2025/2 regress chain and the art. 129 outcome."""
from pathlib import Path
import figkit

PAGE = 'courses/processo-civil-i/aula-12.html'

def thread_panel():
    """Map the parties in Sérgio Mattos's P1 2025/2 question 2 onto successive claims."""
    o = figkit.t(48,42,'P1 · 2025/2 · Q2 · SÉRGIO MATTOS',size=13,fill='var(--ink-2)',weight=700)
    o += figkit.line(48,58,952,58,tone='ink',w=1.4)
    o += figkit.t(66,108,'VIÚVA',size=12,fill='var(--ink-2)',weight=700)
    o += figkit.t(66,137,'ação de reparação',size=12,fill='var(--ink)')
    o += figkit.t(66,156,'demanda principal',size=10,fill='var(--ink-2)')
    o += figkit.line(236,128,365,128,tone='ink',w=2)
    o += figkit.t(300,111,'contra',size=10,fill='var(--ink-2)',anchor='middle')
    o += figkit.t(382,108,'MOTORISTA',size=12,fill='var(--ink)',weight=700)
    o += figkit.t(382,137,'denuncia a locadora',size=12,fill='var(--ink)',weight=700)
    o += figkit.line(558,128,680,128,tone='ink',w=2)
    o += figkit.t(620,111,'regresso 1',size=10,fill='var(--ink)',anchor='middle',weight=700)
    o += figkit.t(696,108,'LOCADORA',size=12,fill='var(--ink)',weight=700)
    o += figkit.t(680,137,'denuncia a seguradora',size=12,fill='var(--ink)',weight=700)
    o += figkit.line(866,128,925,128,tone='dif',w=2)
    o += figkit.t(895,111,'regresso 2',size=10,fill='var(--ink)',anchor='middle',weight=700)
    o += figkit.t(925,166,'SEGURADORA',size=12,fill='var(--ink)',anchor='end',weight=700)
    o += figkit.line(696,185,925,185,tone='dif',w=1.3,dash='4 4')
    o += figkit.t(810,212,'um único regresso sucessivo',size=11,fill='var(--ink)',anchor='middle',weight=700)
    o += figkit.line(48,240,952,240,tone='muted',w=1)
    o += figkit.t(48,273,'O MOTORISTA DENUNCIA A LOCADORA',size=11,fill='var(--ink)',weight=700)
    o += figkit.t(48,296,'A locadora aparece como denunciada e pode, por sua vez, denunciar a seguradora.',size=12,fill='var(--ink)')
    o += figkit.t(48,347,'O LIMITE',size=11,fill='var(--conc)',weight=700)
    o += figkit.t(48,370,'A seguradora não pode promover nova denunciação sucessiva; eventual regresso posterior segue por ação autônoma.',size=12,fill='var(--ink)')
    return figkit.svg('24 20 952 380',o,cls='fig',ident='pci-a12-thread',label='Questão 2 da P1 de 2025/2: motorista denuncia locadora, que promove a única denunciação sucessiva contra a seguradora')

def result_panel():
    """Apply the principal-claim outcome to the driver/rental-company exam claim."""
    o = figkit.t(48,38,'P1 · 2025/2 · Q2 · MOTORISTA / LOCADORA',size=12,fill='var(--ink-2)',weight=700)
    o += figkit.line(48,55,952,55,tone='ink',w=1.4)
    o += figkit.t(500,95,'DEMANDA DA VIÚVA CONTRA O MOTORISTA',size=12,fill='var(--ink)',anchor='middle',weight=700)
    o += figkit.line(500,108,500,145,tone='ink',w=1.8)
    o += figkit.line(240,145,760,145,tone='ink',w=1.8)
    o += figkit.line(240,145,240,190,tone='conc',w=1.8)
    o += figkit.line(760,145,760,190,tone='dif',w=1.8)
    o += figkit.t(240,220,'MOTORISTA VENCIDO',size=12,fill='var(--ink)',anchor='middle',weight=700)
    o += figkit.t(240,251,'juiz julga o regresso',size=12,fill='var(--ink)',anchor='middle')
    o += figkit.t(240,272,'contra a locadora',size=12,fill='var(--ink)',anchor='middle')
    o += figkit.t(760,220,'MOTORISTA VENCEDOR',size=12,fill='var(--ink)',anchor='middle',weight=700)
    o += figkit.t(760,251,'pedido contra a locadora',size=12,fill='var(--ink)',anchor='middle')
    o += figkit.t(760,272,'fica sem exame',size=12,fill='var(--ink)',anchor='middle')
    o += figkit.line(100,315,900,315,tone='muted',w=1)
    o += figkit.t(500,348,'A CONDIÇÃO É O RESULTADO DO PEDIDO DA VIÚVA CONTRA O MOTORISTA',size=11,fill='var(--ink-2)',anchor='middle',weight=700)
    return figkit.svg('24 18 952 355',o,cls='fig',ident='pci-a12-result',label='Na questão 2 da P1 de 2025/2, a derrota do motorista leva ao julgamento do regresso contra a locadora; sua vitória deixa o pedido regressivo sem exame')

def panels():
    figkit.WARN.clear()
    return [thread_panel(), result_panel()]

def install():
    import inject
    return inject.inject(PAGE, {s.split('id="',1)[1].split('"',1)[0]:s for s in panels()})

if __name__ == '__main__':
    print(f'{install()} Aula 12 figures installed')
    print('\n'.join(figkit.WARN) or 'no text warnings')
