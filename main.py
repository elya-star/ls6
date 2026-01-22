import flet as ft 
from db import main_db


def main(page: ft.Page):

    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=25)
    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task_text, task_d=task_text, completed=completed))

    def view_tasks(task_id, task_text, task_d, completed=None):
        task_field = ft.TextField(read_only=True, value=task_text, expand=True, label=f"Создано: {task_d}")

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))

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

        def delete_task(_):
            main_db.delete_task(task_id)
            task_list.controls.remove(row)
            page.update()

        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED)


        row = ft.Row([checkbox, task_field, edit_button, save_button, delete_button])
        return row 
    
    def toggle_task(task_id, is_completed):
        print(is_completed)
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()



    def add_task_db(_):
        if task_input.value:
            task_text = task_input.value
            new_task_id, date_now = main_db.add_task(task=task_text)
            print(f"Задача {task_text} успешно добавлена! Его ID - {new_task_id}")

            task_list.controls.append(view_tasks(task_id=new_task_id, task_text=task_text, task_d=date_now, completed=None))

            task_input.value = ""


    task_input = ft.TextField(label='Введите задание:', expand=True, on_submit=add_task_db)
    task_add_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task_db)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все задачи", on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted'), icon=ft.Icons.WATCH_LATER),
        ft.ElevatedButton('Готово', on_click=lambda e: set_filter('completed'), icon=ft.Icons.CHECK_BOX)
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    def delete_completed(_):
        main_db.delete_completed_tasks()
        load_tasks()

    clear_button = ft.ElevatedButton("Очистить выполненные", icon=ft.Icons.DELETE_SWEEP, on_click=delete_completed)
    input_row = ft.Row([task_input, task_add_button])

    column_buttons = ft.Column ([
        input_row,
        ft.Row([filter_buttons, clear_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ])
    page.add(column_buttons, task_list)
    load_tasks()

if __name__ == '__main__':
    main_db.init_db()
    ft.run(main)