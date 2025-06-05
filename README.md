Trabalho LAA02

## 🏫 Organização de Horários de Aulas para Professores

Você está planejando a grade horária de um curso universitário e recebeu diversas propostas de aulas dos professores, com diferentes durações e temas. Seu desafio é organizar essas aulas ao longo da semana respeitando os horários da instituição e evitando sobreposição de horários para os professores.

### Contexto

A instituição divide o horário diário de aulas em dois períodos:

* **Turno da Manhã**: das 9h às 12h (antes do almoço).
* **Turno da Tarde**: das 13h às 17h (antes de encerrar o expediente).

Cada professor pode ter **mais de uma aula por dia**, mas **não pode estar em duas salas ao mesmo tempo**. A grade semanal é composta por **vários dias (tracks)**, e cada dia possui uma **sessão pela manhã e outra pela tarde**.

Não há necessidade de intervalos entre as aulas, e todos os professores são pontuais. O sistema deve organizar as aulas de forma que **todas as aulas sejam alocadas** e que cada **sessão respeite os limites de horário**.

### Regras

* Cada **sessão da manhã** deve iniciar às **09h00** e terminar **antes ou exatamente às 12h00**.
* Cada **sessão da tarde** deve iniciar às **13h00** e terminar **antes ou exatamente às 17h00**.
* As aulas têm sua **duração especificada em minutos** ou como **“relâmpago”** (5 minutos).
* Cada aula é associada a **um professor**. O professor **não pode ter mais de uma aula ao mesmo tempo**.
* Ao final da tarde, às **17h00**, ocorre uma **reunião de professores** obrigatória, que não pode ser sobreposta por nenhuma aula.

---

### 📄 Exemplo de Entrada (arquivo `aulas.txt`):

```
Introdução à IA - Prof. João 60min
Técnicas de Aprendizado Supervisionado - Prof. Ana 45min
Redes Neurais Convolucionais - Prof. João 30min
Ética na IA - Prof. Carla lightning
Linguagens de Programação Funcionais - Prof. Paulo 45min
História da Computação - Prof. Carla 30min
Banco de Dados NoSQL - Prof. Ana 60min
Lógica Computacional - Prof. Paulo 45min
Compiladores e Interpretadores - Prof. João 60min
Computação Quântica - Prof. Carla 45min
Algoritmos Avançados - Prof. Ana 60min
Programação Paralela - Prof. Paulo 30min
Pensamento Computacional - Prof. Carla 30min
```

---

### 🖥️ Exemplo de Saída Esperada:

```
📅 Segunda-feira:
09:00 Introdução à IA - Prof. João 60min  
10:00 Técnicas de Aprendizado Supervisionado - Prof. Ana 45min  
10:45 Redes Neurais Convolucionais - Prof. João 30min  
11:15 História da Computação - Prof. Carla 30min  
12:00 Intervalo para Almoço  

13:00 Compiladores e Interpretadores - Prof. João 60min  
14:00 Linguagens de Programação Funcionais - Prof. Paulo 45min  
14:45 Programação Paralela - Prof. Paulo 30min  
15:15 Pensamento Computacional - Prof. Carla 30min  
15:45 Ética na IA - Prof. Carla lightning  
16:00 Banco de Dados NoSQL - Prof. Ana 60min  
17:00 Reunião de Professores

📅 Terça-feira:
09:00 Algoritmos Avançados - Prof. Ana 60min  
10:00 Lógica Computacional - Prof. Paulo 45min  
10:45 Computação Quântica - Prof. Carla 45min  
12:00 Intervalo para Almoço  

13:00 (sem aulas disponíveis)  
17:00 Reunião de Professores
```

---

### ✅ Instruções

* Você deve produzir uma **solução programável** capaz de ler um arquivo `aulas.txt` e organizar automaticamente a grade de aulas respeitando as regras acima.
* O resultado da organização deverá ser impresso no console, seguindo o modelo acima.
* Professores **não podem ter conflitos de horário**.
* Sua solução deve ser **escalável** para funcionar com conjuntos maiores de aulas.

---

### 🧪 Avaliação

* Solução funcional, bem estruturada e com testes automatizados: **40 pontos**
* Solução funcional sem testes: **30 pontos**
* Solução incompleta mas com tentativa de organização: **10 pontos**
* Apenas entrega de código sem execução/testes: **5 pontos**

---
