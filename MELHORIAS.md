# O que mudou nesta versão
- Empresas têm **validade do plano**: "Pagou: ativar/renovar +1 mês" soma 30 dias; quando acaba, o bot desliga sozinho e a empresa deixa de aparecer na lista. Empresas antigas "ativas" sem prazo continuam como estavam.
- Novo **portal da empresa** em `/minha-empresa` (botão "Já sou empresa: entrar"): cada empresa vê o estado, a validade, as estatísticas da semana, as conversas, as perguntas sem resposta e edita a informação do seu assistente sozinha. Só vê os seus dados.
- A empresa que se regista recebe a **chave de acesso** no fim do formulário (aparece uma vez). Para as empresas que tu registas, usa o botão "Gerar chave da empresa" no painel.
- API nova para o dono: `PUT /api/empresas/<id>/info` (editar nome e instruções) e `POST /api/empresas/<id>/chave`.
- Removido código morto (`PAGINA_INICIAL`) e comentário desatualizado.
- Colunas novas (`plano_ate`, `chave_hash`) são criadas sozinhas no arranque (não perdes dados).
