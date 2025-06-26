# 💰 Gestor de Gastos

Aplicativo de controle financeiro pessoal desenvolvido em **Python** com **Tkinter** e banco de dados **SQLite**.  
Permite gerenciar seus gastos, organizando-os por data, valor, descrição e número de parcelas. Ideal para quem quer acompanhar suas despesas mensais de forma simples e visual.

![Tela Principal](docs/screenshot_gastos.png) <!-- Substitua com sua imagem -->

---

## ✨ Funcionalidades

- 📌 **Adicionar gastos** com valor, data, descrição e opção de parcelamento.
- 📊 **Consultar todos os gastos** com visualização em tabela e totalizador automático.
- 🧾 **Editar ou excluir** gastos já registrados.
- 🗂️ **Gerenciar múltiplas contas** (arquivos `.db`) diretamente pela interface:
  - Criar, trocar e excluir contas.
- 🔁 **Atualização automática** de parcelas com base na data atual.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [tkcalendar](https://github.com/j4321/tkcalendar) `pip install tkcalendar`

---

## 🖥️ Instalação e Uso

### Pré-requisitos

- Python 3 instalado
- Biblioteca `tkcalendar` (instale com o comando abaixo):

```bash
pip install tkcalendar
