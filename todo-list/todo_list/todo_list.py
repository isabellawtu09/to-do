"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

class Task(rx.Base):
    name: str
    date: str
    notes: str
    status: str

class State(rx.State):
    # want website to be hosted on local storage
    tasks: list[Task] = []

    def add_item(self, form_data: dict):
        self.tasks.append(Task(**form_data))

    def delete_item(self, task_to_delete: Task):
        self.tasks = [task for task in self.tasks if task != task_to_delete]

    ## add edit button in actions


def _badge(icon: str, text: str, color_scheme: str):
    return rx.badge(
        rx.icon(icon, size=16),
        text,
        color_scheme=color_scheme,
        radius="full",
        variant="soft",
        size="3",
    )

def status_badge(status: str):
    badge_mapping = {
        "Completed": ("check", "Completed", "green"),
        "In Progress": ("loader", "In Progress", "yellow"),
        "Not Started": ("ban", "Not Started", "red"),
    }
    return _badge(*badge_mapping.get(status, ("loader", "In progress", "yellow")))



def show_item(task: Task):
    return rx.table.row(
        rx.table.cell(task.name),
        rx.table.cell(task.date),
        rx.table.cell(task.notes),
        rx.table.cell(
            rx.match(
                task.status,
                ("Completed", status_badge("Completed")),
                ("In Progress", status_badge("In Progress")),
                ("Not Started", status_badge("Not Started")),
                status_badge("Not Started"),
            )
        ),
        rx.table.cell(
            rx.button(
                "Delete",
                color_scheme="red",
                size="2",
                on_click=lambda: State.delete_item(task),
            )
        ),
    )

def add_item_form():
    return rx.form(
        rx.hstack(
            rx.input(placeholder="Task", name="name", required=True),
            rx.input(type="date", name="date", required=True),
            rx.input(placeholder="Notes", name="notes"),
            rx.select(
                ["Completed", "In Progress", "Not Started"],
                name="status",
                placeholder="Status",
                required=True,
            ),
            rx.button("Add", type="submit", color_scheme="green", size="2"),
        ),
        on_submit=State.add_item,
        reset_on_submit=True,
    )


def navbar():
    return rx.flex(
        rx.badge(
            rx.icon(tag="list-todo", size=28),
            rx.heading("Welcome to your To-Do List", size="6"),
            color_scheme="green",
            radius="large",
            align="center",
            variant="surface",
            padding="0.75rem",
        ),
        rx.spacer(),
        rx.hstack(
            rx.heading("Screen Mode : ", size = "2"),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
        padding_top="2em",
    )

def index():
    return rx.vstack(
        navbar(),
        add_item_form(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Date"),
                    rx.table.column_header_cell("Notes"),
                    rx.table.column_header_cell("Status"),
                    rx.table.column_header_cell("Actions"),
                ),
            ),
            rx.table.body(
                rx.foreach(State.tasks, show_item),
            ),
            width="100%",
        ),
    )

app = rx.App()
app.add_page(index)