# 🔢 Sorting Visualizer

Visualizador interativo de algoritmos de ordenação com interface gráfica em Python (Tkinter). Ideal para estudar e entender o comportamento de diferentes algoritmos de forma visual.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## 📸 Preview

> Interface com tema escuro, barras coloridas em tempo real e painel de estatísticas.

---

## ✨ Funcionalidades

- **5 algoritmos** implementados: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort e Quick Sort
- **Visualização em tempo real** com cores distintas para comparações, trocas e elementos já ordenados
- **Painel de estatísticas** com contador de comparações, trocas e tempo decorrido
- **Controles ajustáveis**: quantidade de elementos (10–150) e velocidade da animação
- **Tema dark** com estética terminal/retro
- **Thread separada** para a ordenação, mantendo a UI responsiva

---

## 🎨 Legenda de cores

| Cor | Significado |
|-----|-------------|
| 🔵 Ciano (`#00e5ff`) | Barra padrão |
| 🔴 Rosa (`#ff4081`) | Comparando dois elementos |
| 🟡 Amarelo (`#ffeb3b`) | Realizando uma troca |
| 🟢 Verde (`#69ff47`) | Elemento na posição correta |

---

## 🚀 Como executar

### Pré-requisitos

- Python 3.8 ou superior
- Tkinter (já incluído na instalação padrão do Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sorting-visualizer.git
cd sorting-visualizer

# Execute diretamente (sem dependências externas)
python main.py
```

> **Nota:** No Linux, caso o Tkinter não esteja instalado:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🧠 Algoritmos implementados

| Algoritmo | Melhor caso | Caso médio | Pior caso | Memória |
|-----------|-------------|------------|-----------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |

---

## 📂 Estrutura do projeto

```
sorting-visualizer/
├── main.py        # Código principal (algoritmos + interface)
├── algorithms.py  # algoritmos utilizados
├── app.py         # interface do aplicativo
├── config.py      # configurações básicas
├── README.md      # Documentação
└── .gitignore     # Arquivos ignorados pelo Git
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

- Adicionar novos algoritmos (Heap Sort, Shell Sort, Radix Sort...)
- Melhorar a interface
- Adicionar suporte a temas
- Traduzir para outros idiomas

Abra uma _issue_ ou envie um _pull request_.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [`LICENSE`](LICENSE) para mais detalhes.

---

Feito com 🚀 por [Mateus](https://github.com/xTeuszz)
