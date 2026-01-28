# SHELL

A robust, POSIX-compliant shell implementation built in Python, developed as part of the [CodeCrafters Build Your Own Shell](https://app.codecrafters.io/courses/shell/overview) challenge.

## Features

This shell provides a rich set of features for command-line interaction:

- **Command Execution**: Run any external interactive or non-interactive programs found in your `$PATH`.
- **Built-in Commands**:
  - `cd`: Change directory (supports relative paths, absolute paths, `~`, `.`, and `..`).
  - `pwd`: Print working directory.
  - `echo`: Display text to standard output.
  - `type`: Identify if a command is a builtin or an external executable.
  - `exit`: Exit the shell.
  - `history`: View and manage command history.
- **Quoting & Escaping**:
  - Single Quotes (`'...'`): Preserve the literal value of each character within the quotes.
  - Double Quotes (`"..."`): Preserve the literal value of characters, but allow backslash escaping for `"` and `\`.
  - Backslash (`\`): Escape special characters.
- **I/O Redirection**:
  - Standard Output: `>` (overwrite), `>>` (append).
  - Standard Error: `2>` (overwrite), `2>>` (append).
- **Pipes**: Chaining commands using `|` (e.g., `ls | grep .py`).
- **History Management**:
  - Persistent history using `HISTFILE`.
  - Commands to read/write history (`history -r`, `history -w`, `history -a`).
- **Autocompletion**: Tab completion for commands and file paths.

## Installation

No external dependencies are required. The shell relies on Python's standard library components like `subprocess`, `os`, `sys`, and `readline`.

Clone the repository:

```bash
git clone https://github.com/wajdiJomaa/SHELL.git
cd SHELL
```

## Usage

Run the shell using the following command from the project root:

```bash
python3 -m app.main
```

Once running, you can use it just like any other shell:

```bash
$ echo "Hello, World!"
Hello, World!

$ pwd
/home/user/SHELL

$ ls -la | grep .py
...
```

## Project Structure

- **`app/main.py`**: The entry point of the application, initializing the REPL loop and history.
- **`app/scanner/`**: Tokenizes raw input strings.
- **`app/parser/`**: Parses tokens into an Abstract Syntax Tree (AST).
- **`app/executor/`**: Executes the AST, handling builtins, piping, and redirections.
- **`app/history.py`**: Manages session history and file persistence.
- **`app/completer/`**: Handles tab completion logic.

## Credits

Based on the ["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview) from CodeCrafters.
