# MacTech (site estático, grátis e sem espera)

Este site é só a "montra" da MacTech. O bot continua no outro serviço (jolonss.onrender.com).
Como é estático, o Render serve os ficheiros sempre, sem adormecer. É por isso que a Google o consegue ler.

## Publicar
1. Cria um repositório novo no GitHub e envia o conteúdo desta pasta (as pastas `public` e o `render.yaml`).
2. No Render: New > Static Site > escolhe esse repositório.
3. Build Command: deixa vazio. Publish Directory: `public`.
4. Quando o Render der o endereço do site (algo como https://mactech-site-xxxx.onrender.com), abre-o e confirma que aparece a página.

## Pôr na Google
1. Search Console: Adicionar propriedade > Prefixo do URL > cola o endereço novo.
2. Verificação por ficheiro HTML: o ficheiro `google4a5cd989738543d6.html` já está em `public`.
3. Inspeção de URLs: cola o endereço novo > Solicitar indexação.
A Google pode demorar alguns dias.

## Mudar os links do bot
Se o endereço do bot mudar, troca `https://jolonss.onrender.com` em `public/index.html`.
