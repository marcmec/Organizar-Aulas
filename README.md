# Organizador de Horários de Aulas

Este projeto organiza automaticamente uma grade de aulas para professores universitários a partir de um arquivo de texto, respeitando os horários da instituição e evitando conflitos.

## Como Executar

1.  **Pré-requisitos**: Certifique-se de ter o Python 3 instalado.

2.  **Preparar o Arquivo de Aulas**: Verifique se o arquivo `aulas.txt` está na mesma pasta e contém a lista de aulas no formato especificado:
    `Nome da Matéria - Prof. Nome Professor Duração` (ex: `Introdução à IA - Prof. João 60min` ou `Ética na IA - Prof. Carla lightning`).

3.  **Executar o Programa Principal**:
    Abra um terminal na pasta do projeto e execute o seguinte comando:
    ```sh
    python main.py
    ```
    A grade horária organizada será impressa no console.

## Como Executar os Testes

Para garantir que a lógica do programa está funcionando corretamente, você pode rodar os testes automatizados.

1.  **Executar os Testes**:
    No terminal, execute o comando:
    ```sh
    python test_scheduler.py
    ```
    Se todos os testes passarem, você verá uma mensagem indicando o sucesso.