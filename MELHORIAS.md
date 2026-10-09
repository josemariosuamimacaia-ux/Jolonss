# O que mudou nesta versão
- Empresas têm **validade do plano**: "Pagou: ativar/renovar +1 mês" soma 30 dias; quando acaba, o bot desliga sozinho e a empresa deixa de aparecer na lista. Empresas antigas "ativas" sem prazo continuam como estavam.
- Novo **portal da empresa** em `/minha-empresa` (botão "Já sou empresa: entrar"): cada empresa vê o estado, a validade, as estatísticas da semana, as conversas, as perguntas sem resposta e edita a informação do seu assistente sozinha. Só vê os seus dados.
- A empresa que se regista recebe a **chave de acesso** no fim do formulário (aparece uma vez). Para as empresas que tu registas, usa o botão "Gerar chave da empresa" no painel.
- API nova para o dono: `PUT /api/empresas/<id>/info` (editar nome e instruções) e `POST /api/empresas/<id>/chave`.
- Removido código morto (`PAGINA_INICIAL`) e comentário desatualizado.
- Colunas novas (`plano_ate`, `chave_hash`) são criadas sozinhas no arranque (não perdes dados).

# Versão 4 (2026-10-08-f-v4)
- **Áudios e imagens no WhatsApp:** o bot transcreve mensagens de voz e descreve fotos (comprovativos incluídos) com o Gemini, com a mesma chave. Se não conseguir, pede ao cliente que escreva.
- **Nunca confirma pagamentos:** diz que a equipa confirma. A confirmação continua a ser tua.
- **Cliente zangado passa a humano:** palavras claras de insatisfação (e pedidos de atendente) passam a conversa à equipa, se a empresa tiver equipa.
- **Lista tocável** na escolha de empresa do número partilhado (com plano B em texto se a Meta recusar).
- **Erros sem código técnico:** se algo falhar a meio, o cliente recebe sempre uma mensagem simpática.
- **IA de reserva (opcional):** se existir `GROQ_API_KEY`, o Groq responde quando o Gemini falha. Sem essa chave nada muda.
- **Base de dados mais robusta:** pg8000 (Python puro), aviso claro do que está mal e versão visível em `/saude`.

# Versão 5 (2026-10-08-g-v5), última antes de haver clientes
- **Cópia de segurança:** botão no painel ("Descarregar cópia de segurança") e endereço `/api/backup`. Guarda empresas, departamentos, produtos, encomendas e tickets em JSON, sem tokens nem chaves. Contém contactos de clientes, por isso guardar em local privado. A restauração é feita à mão (pede ajuda).
- **Voltar à lista de empresas** no número partilhado com frases claras: "mudar de empresa", "trocar de empresa", "outra empresa", "menu principal", "voltar ao menu". Palavras soltas como "menu" ou "cancelar" ficam de fora porque têm outro sentido numa loja.
- **Testes offline** em `testes_offline.py` (para quem desenvolver a seguir): `python testes_offline.py`.

