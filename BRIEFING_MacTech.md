# Briefing do projeto MacTech (para uma IA que vai trabalhar neste código)

Copia este texto inteiro para a outra IA e, no fim, escreve a tarefa concreta que queres.
Nunca lhe dês chaves de API nem o código de administração.

## 1. O que é o produto
MacTech é um site em Python (Flask) que vende **assistentes de atendimento com IA para empresas angolanas**. Cada empresa regista os seus produtos, preços, horários e contactos; os clientes dessa empresa fazem perguntas num chat web (ou no WhatsApp) e uma IA responde só com a informação da empresa. Quando a IA não sabe, ou o cliente pede uma pessoa, a conversa passa a um atendente humano.

Idioma de tudo: português de Angola. Moeda: Kwanza (AOA). Fuso: Luanda (UTC+1).

## 2. Quem usa
- **Cliente:** abre o site, escolhe a empresa numa lista e conversa. Não precisa de conta nem de código.
- **Empresa:** pode registar-se sozinha (lê os termos, vê os dados de pagamento, preenche o formulário). Fica *pendente* até o dono confirmar o pagamento.
- **Dono (único administrador):** entra em `/painel` com a chave de administração. Regista empresas abordadas por ele (teste de 1 dia), ativa empresas pendentes, suspende, vê estatísticas, conversas, perguntas sem resposta, contactos e exporta CSV.
- **Atendente (nível 4):** entra em `/agente` com chave própria, vê a fila do seu departamento, assume uma conversa, responde e devolve à IA.

O dono **não é programador**: trabalha só pelo telemóvel, edita ficheiros pelo site do GitHub e faz deploy no Render. Explica sempre passo a passo e não peças comandos de terminal.

## 3. Modelo de negócio
- Empresas abordadas pelo dono são registadas por ele e testam **1 dia** de graça.
- Empresas que se registam sozinhas leem os termos, fazem o **pagamento inicial** (transferência/meios angolanos como BFA e BAI, confirmação manual) e só depois ficam visíveis.
- Objetivo atual: **gastar zero** até as primeiras empresas pagarem; só então sobe o plano pago do Render.

## 4. Tecnologia e alojamento (tudo no plano grátis)
- Python 3, Flask, SQLAlchemy 2, gunicorn. Sem framework de front-end: HTML, CSS e JavaScript simples **embutidos em `assets.py`** (não há pasta static).
- Alojamento: **Render** (web service grátis, adormece após 15 min; mantido acordado por um monitor UptimeRobot a chamar `/saude`).
- Base de dados: **PostgreSQL no Neon** via variável `DATABASE_URL` (o SQLite local `mactech.db` só serve em desenvolvimento, porque o disco do Render apaga-se a cada deploy).
- IA: **Google Gemini** por HTTP direto (`requests`), chave gratuita do Google AI Studio. Modelo por defeito `gemini-3.1-flash-lite`, configurável em `AI_MODEL`. O limite gratuito é pequeno e é a principal causa de falhas.
- WhatsApp: API oficial da Meta (webhook `/webhook`), com número próprio por empresa ou um número partilhado que pergunta a que empresa o cliente quer falar.

## 5. Ficheiros
| Ficheiro | Função |
|---|---|
| `app.py` | rotas, multi-empresa, chat web, webhook do WhatsApp, passagem a humano, painel |
| `publico.py` | página inicial (3 botões), lista de empresas, registo de empresas, termos, pedidos de pagamento |
| `ia.py` | chamada ao Gemini: tentativas automáticas, regras da IA, ferramentas, streaming, mensagens de erro, diagnóstico |
| `config.py` | variáveis de ambiente (aceita `GEMINI_API_KEY`) e validação ao arrancar |
| `models.py` | tabelas: empresas, conversas, mensagens, departamentos, agentes, tickets, produtos, encomendas, pedidos |
| `assets.py` | todo o CSS, JS e HTML do chat, do painel e da página do agente |
| `chat_page.py` | página de chat de cada empresa (`/c/<slug>`) |
| `nivel4.py`, `ferramentas.py`, `segredos.py` | departamentos, atendentes, ferramentas da IA (stock, encomenda, fatura, transferência), ligação a ERP, cifra de tokens |
| `whatsapp.py` | assinatura HMAC e envio de mensagens |
| `verificar.py` | script que testa o site publicado |
| `requirements.txt`, `Procfile`, `render.yaml` | instalação e arranque no Render |
| `README.md`, `GUIA_RENDER.md`, `NIVEL4.md`, `INTEGRACAO.md` | documentação |

## 6. Funcionalidades já feitas
- Multi-empresa: cada empresa tem `slug`, texto de instruções (system prompt), estado (`pendente`, `teste`, `ativo`, `suspenso`) e conversas próprias.
- Chat web com texto a aparecer aos poucos, limites de pedidos por visitante e por sessão, mensagens até 1000 caracteres.
- A IA só usa a informação da empresa, responde curto, ignora tentativas de mudar as suas regras, diz que é uma IA, e pede nome e contacto quando não sabe (marcador interno `[[SEM_RESPOSTA]]`).
- Passagem a humano; devolução à IA; fila de atendentes por departamento.
- Ferramentas da IA: consultar stock, consultar encomenda (valida telefone/email), pedir fatura (não emite: quem emite é o ERP certificado), transferir para departamento, abrir ticket.
- Painel: empresas, estatísticas, conversas, perguntas sem resposta, contactos, CSV, botão "Testar sistema".
- Registo público de empresas com termos, pagamento e aprovação do dono; lista pública só com empresas aprovadas.
- Segurança: chave de administração com bloqueio após tentativas erradas, painel sem iframe, deduplicação de mensagens da Meta, honeypot e limite no registo público.

## 7. Variáveis de ambiente (Render)
`ADMIN_API_KEY` (chave do dono), `GEMINI_API_KEY`, `AI_MODEL` (opcional), `DATABASE_URL` (Neon), `PAGAMENTO_INSTRUCOES` (texto de pagamento), `TRUST_PROXY=1`, e as do WhatsApp (`WHATSAPP_VERIFY_TOKEN`, `HUB_PHONE_NUMBER_ID`, `HUB_ACCESS_TOKEN`, segredo da app Meta) só se usar WhatsApp.

## 8. Problemas conhecidos e riscos
- O limite gratuito do Gemini é pequeno e instável; quando falha, o cliente recebe a mensagem de erro/atendente humano. Ideia pendente: usar um segundo fornecedor gratuito (por exemplo Groq) como reserva e uma camada de FAQ que responde perguntas simples sem chamar a IA.
- Os modelos de IA mudam de nome e são desligados com frequência: confirmar sempre o nome atual na documentação oficial.
- O telemóvel renomeia ficheiros repetidos (`app-1.py`, `config (1).py`): o dono já teve o site a correr a versão antiga por isso.
- O registo público não foi testado ponta a ponta com PostgreSQL real (só com testes parciais).
- Os termos de uso são um modelo e precisam de revisão por um advogado.
- O limitador de pedidos é em memória (cada worker conta à parte).
- O pagamento é manual (sem gateway). Falta definir texto de pagamento e valor.

## 9. Regras para quem mexer no código
1. Mantém Python/Flask e a estrutura de ficheiros; não introduzas front-end com build (React, npm).
2. Mantém tudo gratuito: nada de serviços pagos sem avisar o dono.
3. Não mudes os nomes dos ficheiros nem das variáveis de ambiente sem avisar.
4. Entrega ficheiros completos, com os mesmos nomes, prontos a colar no GitHub (o dono não sabe aplicar diffs).
5. Mensagens ao utilizador em português de Angola, simples e curtas.
6. Não peças nem escrevas chaves de API, tokens ou o código do painel em lado nenhum.
7. Antes de dizer que algo funciona, testa; se não puderes testar, diz o que ficou por testar.

## 10. Tarefa
(Escreve aqui o que queres que a IA faça.)
