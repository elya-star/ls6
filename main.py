import flet as ft 
from db import main_db


def main(page: ft.Page):

    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=25)

    def view_tasks(task_id, task_text):
        task_field = ft.TextField(read_only=True, value=task_text, expand=True)

        def enable_edit(_):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        def delete_task(e):
            tid = task_id[0] if isinstance(task_id, tuple) else task_id
            main_db.delete_task(tid)
            task_list.controls.remove(row)
            page.update()

        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED)

        row = ft.Row([task_field, edit_button, save_button, delete_button])
        return row 

    def add_task_db(_):
        if task_input.value:
            task_text = task_input.value
            new_task_id = main_db.add_task(task=task_text)
            print(f"Задача {task_text} успешно добавлена! Его ID - {new_task_id}")

            task_list.controls.append(view_tasks(task_id=new_task_id, task_text=task_text))

            task_input.value = ""


    task_input = ft.TextField(label='Введите задание:', expand=True, on_submit=add_task_db)
    task_add_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task_db)

    input_row = ft.Row([task_input, task_add_button])

    page.add(input_row, task_list)


if __name__ == '__main__':
    main_db.init_db()
    ft.run(main, view=ft.AppView.WEB_BROWSER)