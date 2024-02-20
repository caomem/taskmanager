# ⚠️ This Repository is Abandoned ⚠️

**Attention:** This repository is no longer actively maintained. We recommend using [Taskwarrior](https://taskwarrior.org/) for task management, as it provides a robust and feature-rich solution.

---

## Task Manager

The Task Manager is an simple application for managing daily tasks, allowing users to organize their activities efficiently.
The main goal of the project is to not need to think so much about what to do daily.

## Key Features:

- **Manage Tasks:** Users can add new tasks, view, edit, complete and cancel tasks.
- **Automate create daily ToDo list:** Specifying priority, time estimate and deadline of each task allows the application to suggest your next tasks to today. 
- **User Interface:** The Task Scheduler offers a command-line interface (CLI) and a web-based graphical user interface (GUI) for easy interaction.

## How to Use:

1. Clone the repository to your local environment.
```bash
git clone https://github.com/caomem/taskmanager
```
You already can use the command line interface. Try
```bash
./taskman --help
```
2. Install the required dependencies listed in the `requirements.txt` file using the command 
```bash 
make install
```
3. Start the Flask server by running the command `make run`.
4. Access the application through the web browser.

## Contribution:

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License:

This project is licensed under the [GNU General Public License v3.0](https://opensource.org/licenses/GPL-3.0).


