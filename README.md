# Instruções para o Site Estático no Render

Este arquivo contém instruções sobre como usar o site estático hospedado no Render.

## Sobre esta versão

Esta versão do site foi adaptada para funcionar como um site estático no Render, o que significa:

1. Não há backend Python/Flask (diferente da versão original)
2. Os dados são armazenados localmente no navegador de cada usuário
3. Atualizações podem ser feitas através do painel de administração embutido

## Como usar o painel de administração

1. Clique no ícone de engrenagem (⚙️) no canto inferior direito da tela
2. Edite os dados JSON no formato:
   ```json
   {
     "timers": [
       {
         "fic_number": "12345",
         "model": "MODELO-A",
         "tag": "220",
         "start": "2023-05-22T10:30:00Z"
       },
       {
         "fic_number": "67890",
         "model": "MODELO-B",
         "tag": "220",
         "start": "2023-05-22T11:45:00Z"
       }
     ],
     "stopped": ["12345"]
   }
   ```
3. Clique em "Atualizar Dados"

## Limitações

- Os dados são salvos apenas no navegador local (localStorage)
- Cada usuário vê apenas os dados que foram inseridos naquele navegador específico
- Não há sincronização automática entre diferentes dispositivos

## Alternativas para sincronização

Se você precisar de sincronização entre dispositivos, considere:

1. Usar um serviço Web Service no Render (opção mais avançada)
2. Integrar com Google Sheets ou outra fonte de dados externa
3. Usar um banco de dados simples como Firebase

## Contato para suporte

Se precisar de ajuda ou quiser implementar uma versão mais avançada com sincronização, entre em contato.
