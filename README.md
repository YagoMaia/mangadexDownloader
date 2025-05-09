# MangadexDownloader 
Mangadex Downloader é uma aplicação que consome a API do MangaDex para fazer o download de mangás de maneira eficiente e otimizada. Usando Celery, RabbitMQ e Redis, a aplicação permite baixar capítulos de mangás específicos utilizando múltiplas threads de forma eficiente, melhorando o desempenho do processo.

## Tecnologias
- Celery: Para gerenciamento de tarefas assíncronas e multithreading.
- RabbitMQ: Usado como broker para comunicação entre o Celery e as tarefas.
- Redis: Para cache e monitoramento do lançamento de novos capítulos.
- MangaDex API: API que fornece os dados sobre mangás e capítulos.

## Funcionalidades
- Download paralelo de mangás: Utiliza o Celery e RabbitMQ para dividir as tarefas de download em múltiplas threads, acelerando o processo de download dos capítulos.
- Monitoramento de lançamentos: A aplicação verifica periodicamente, usando tarefas agendadas, quando um novo capítulo de mangá da sua lista diária é lançado.
- Armazenamento rápido com Redis: A lista de mangás e informações de lançamento são armazenadas e acessadas rapidamente utilizando Redis.

## Como Funciona
- Consumindo MangaDex API: A aplicação consome a API do MangaDex para obter informações sobre mangás, capítulos e detalhes relacionados.
- Baixando capítulos: Através do Celery, as tarefas de download são distribuídas de maneira eficiente entre múltiplas threads, otimizando o tempo de download. O número máximo de threads é configurável.
- Monitoramento de atualizações: A aplicação possui tarefas agendadas no Celery para verificar se novos capítulos dos mangás estão sendo lançados, com um intervalo configurável.
- Uso de Redis: Toda a comunicação e cache (informações de mangás e atualizações) são gerenciados com Redis para garantir respostas rápidas e evitar sobrecarga no sistema.