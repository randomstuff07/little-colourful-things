import os
import flet as ft
import flet
import subprocess as sp

from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
from flet import (
    Row,
    Text,
)

matplotlib.use('svg')

# dummy init (remove once done testing)

def fetch_stats(ct, ec):
    global cats
    global err_cnt

    cats = ct
    err_cnt = ec
    
    ft.app(target=disp_stats)

def disp_stats(page: ft.Page):
    
    fig, ax = plt.subplots()
    
    ax.bar(cats, err_cnt, color='blue')
    # Adding labels and title
    ax.set_xlabel('Error type')
    ax.set_ylabel('Frequency')
    ax.set_title('Segregation error rates')
    ax.legend(title='error types')
    page.title = 'Stats - Little Colorful Things v1.0'
    page.add(
        Row(
            [ Text('Segregation error counts in current set: ')],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        MatplotlibChart(fig, expand=True),

        ft.DataTable(
            columns = [
                ft.DataColumn(ft.Text('Normal'), numeric=True),
                ft.DataColumn(ft.Text('CCO'), numeric=True),
                ft.DataColumn(ft.Text('MI NDJ'), numeric=True),
                ft.DataColumn(ft.Text('MI RS'), numeric=True),
                ft.DataColumn(ft.Text('MI PSSC'), numeric=True),
                ft.DataColumn(ft.Text('MII PSSC'), numeric=True),
                ft.DataColumn(ft.Text('Others'), numeric=True)
            ],
            rows = [
                ft.DataRow(
                    cells= [
                        ft.DataCell(ft.Text(err_cnt[0])),
                        ft.DataCell(ft.Text(err_cnt[1])),
                        ft.DataCell(ft.Text(err_cnt[2])),
                        ft.DataCell(ft.Text(err_cnt[3])),
                        ft.DataCell(ft.Text(err_cnt[4])),
                        ft.DataCell(ft.Text(err_cnt[5])),
                        ft.DataCell(ft.Text(err_cnt[6])),
                    ]
                )  
            ]
            
        )
    )

    
def get_file(page: Page):
    FILE_PATH = ''
    EXEC_FLAG = ''
    # Pick files dialog
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 40
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    img = ft.Image(
        src=os.path.join(os.getcwd(), 'logo.png'),
        width=175,
        height=175,
        fit=ft.ImageFit.CONTAIN,
    )
    path_notif = ft.Text()
    page.add(path_notif)
    txt =ft.TextField(label="For e.g.: 'D://Documents//....'")
    def save_file_btn(e):
        path = txt.value
        if os.path.exists(path):
            FILE_PATH = txt.value
            path_notif = ft.Text('File path saved!')
            page.update()
        else:
            path_notif = ft.Text('Couldn\'t find file path! Enter correct file path.')
            page.update()
    
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'Enter':
            save_file_btn()

    def open_readme(e):
        programName = "notepad.exe"
        fileName = "README.md"
        sp.Popen([programName, fileName])
        
    def get_exec_flag(flag):
        EXEC_FLAG = flag
    
    page.on_keyboard_event = on_keyboard

    page.title = 'Little Colorful Things v1.0'

    lbl1 = ft.Text('Enter File Path of Images (.png, .jpg files):')
    path_status = ft.Text()
    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()
        
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])
    
    page.add(
        Row(
        [img, ft.IconButton(
                icon= icons.QUESTION_MARK,
                icon_size=20,
                on_click = open_readme,
            )],
            spacing=350, alignment=ft.MainAxisAlignment.CENTER
       ),
        Row(),
        Row([lbl1]),
        Row(),
        Row(
            [txt, ElevatedButton(
                    'Save File Path', 
                    icon = icons.SAVE,
                    on_click=save_file_btn,
            ),
            ]
        ),
        Row([Text('Or choose a folder from This PC')]),
        Row([ElevatedButton(
                    "Open directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
            ]
        ), 
        Row(),
        Row(
            [Text('Choose contrast settings: ')]
        ), 
        Row(
            [
                ElevatedButton(
                    "High Contrast",
                    on_click=get_exec_flag('high'),
                ),
                ElevatedButton(
                    "Low Contrast",
                    on_click=get_exec_flag('low')
                ), 
            ]
        )
    )
    page.update()
    return FILE_PATH, EXEC_FLAG

flet.app(target=get_file)