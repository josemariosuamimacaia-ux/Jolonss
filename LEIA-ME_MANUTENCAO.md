# MacTech: guia de manutenção

O produto está fechado. De agora em diante só se mexe nestes pontos.

## Onde mudar preços, limites e custos
Tudo no início do ficheiro `planos.py`:
- `PLANOS`: nome, preço por mês (Kz), mensagens de clientes por mês, e se inclui WhatsApp e ferramentas (stock, encomendas, faturas, departamentos).
- `CUSTO_FIXO_MENSAL_KZ`: servidor e base de dados no Render (estimativa tua).
- `CUSTO_IA_KZ_MIL_ENTRADA` e `CUSTO_IA_KZ_MIL_SAIDA`: custo estimado da IA por cada 1000 tokens. Ajusta quando vires a fatura real.
- `AVISO_PERCENTAGEM`: avisa quando a empresa chega a este % do limite (80).
- `HORAS_ATE_IA_RETOMAR`: se uma pessoa assumiu a conversa e ninguém responde, a IA volta ao fim destas horas (6).

## O que o dono faz no painel
Depois da chave aparecem dois botões:
- **Cadastrar empresas**: registar empresa (com pacote), lista de empresas, conversas, tickets, exportar.
- **Análise**: no mês, por empresa: pessoas, mensagens, respostas da IA, custo da IA, receita do pacote e lucro. No fim, o lucro total depois do custo fixo.

Por empresa: mudar o pacote, mudar o logótipo, **Arquivar** (desliga o bot e tira da análise, os dados ficam), **Restaurar** e **Eliminar para sempre** (só depois de arquivar e escrevendo o nome exato).

## Regras que o sistema aplica sozinho
- Quando o mês pago ou o teste acaba, o bot desliga.
- Contas antigas "ativas" sem data de fim ganham 30 dias uma só vez; depois só continuam com «Pagou: ativar/renovar».
- Ao passar o limite de mensagens do pacote, a IA para e o cliente é mandado contactar a empresa (ainda pode falar com uma pessoa).
- Pacote sem WhatsApp: o número não responde por WhatsApp. Pacote sem ferramentas: a IA não usa stock/encomendas.
- Contas sem pacote (as antigas) continuam sem limite.
- Conversa assumida por uma pessoa que ninguém responde durante 6 horas: a IA retoma.

## Tabelas novas (criadas sozinhas, sem tocar no models.py)
`planos_empresa` (pacote e arquivo), `uso_ia` (tokens por empresa e mês), `logos_empresa` (logótipos).
O backup em /api/backup inclui `planos_empresa` e `uso_ia`.

## Testes
`python testes_offline.py` deve acabar com TODOS OS TESTES PASSARAM antes de cada atualização.

## Google (Search Console)
- `/robots.txt`, `/sitemap.xml` e `/google4a5cd989738543d6.html` respondem sempre, mesmo quando a base de dados está a acordar. Antes, nessa altura o site devolvia erro 503 e a Google lia isso como "bloqueado".
- Páginas públicas (`/`, `/clientes`, `/empresas`) também respondem sem a base de dados. As áreas privadas (`/painel`, `/agente`, `/minha-empresa`, `/api/`) ficam fora do Google.
- Depois de publicar: abre `/robots.txt` no navegador (deve aparecer texto), e na Search Console usa «Testar URL publicado» e «Solicitar indexação». A Google pode demorar dias.

## Pagamentos por comprovativo (novo)
Fluxo: a empresa paga por transferência e envia o comprovativo (foto, captura ou PDF até 900 KB) -> cai uma notificação no painel do dono -> o dono vê o comprovativo e carrega em «Já pagou» -> a empresa fica ativa **31 dias** (constante `DIAS_POR_MES` em `planos.py`).
- **Registo:** o comprovativo é obrigatório; o número da transferência é opcional.
- **Renovação:** em «Minha empresa» há o cartão «Pagamento e renovação» (como pagar, estado do último comprovativo e envio de um novo).
- **Painel do dono, botão «Notificações»** (com o número de pendentes): mostra os comprovativos à espera (Ver comprovativo, Já pagou, Recusar com motivo) e as empresas cujo prazo acaba em 3 dias ou menos, ou já acabou, com o consumo do período, o texto de cobrança pronto a copiar e o botão «Enviar por WhatsApp» (só se o contacto for um telemóvel).
- **Segurança:** só PNG, JPG, WebP e PDF verdadeiros e pequenos; carregar duas vezes em «Já pagou» não soma duas vezes; se ativares à mão em «Pagou: ativar/renovar», os comprovativos à espera ficam tratados.
- **Espaço:** o ficheiro de cada comprovativo é apagado 90 dias depois de tratado (a linha com a data e o estado fica). O backup leva os dados dos comprovativos mas não os ficheiros.
- **Instruções de pagamento:** a variável `PAGAMENTO_INSTRUCOES` no Render (aparece no registo e em «Minha empresa»).
- Tabela nova (criada sozinha): `provas_pagamento`.

## Google e o Render gratuito
No plano gratuito do Render o serviço adormece após 15 minutos sem visitas e, enquanto dorme, o próprio Render responde ao `/robots.txt` com «proibido tudo», sem chegar ao código. Isso faz a Search Console mostrar «Bloqueada pelo ficheiro robots.txt». Para a Google conseguir ler: usa um plano pago do Render (o mais barato que não adormece) ou, no mínimo, abre o site antes de testar na Search Console.
