import numpy as np
import PIL
import os
import flet
import json
from centerfinder import *
from seq_finder import *
from preprocess import *
from pizzacutter import *
from stats import *

import flet as ft
import subprocess as sp

from flet import (
    ElevatedButton,
    FilePickerResultEvent,
    Row,
    Text,
    icons,
)

import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import matplotlib

matplotlib.use('svg')
def get_main_window(page):   # gets the file path from the ui.

    title_text = ft.Text()
    page.title = 'Little Colourful Things v1.0'
    lbl = ft.Text()
    hclbl = 'High Contrast'
    lclbl = 'Low Contrast'
    # Pick files dialog
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 40
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    img = ft.Image(
        src=os.path.join(os.getcwd(), 'logo.png'),
        width=175,
        height=175,
        fit=ft.ImageFit.CONTAIN,
    )

    def open_readme(e):
        programName = "notepad.exe"
        fileName = "README.md"
        os.chdir('..')
        sp.Popen([programName, fileName])
        os.chdir('app_files')

    def hc_btn_click(e):        #event handler for (high contrast) button click 
        lbl.value = f'Processing settings: {hclbl}'
        hcbtn.bgcolor = 'GREEN'
        lcbtn.bgcolor = 'INDIGO'
        page.update()
    
    def lc_btn_click(e):        #event handler for (low contrast) button click 
        lbl.value = f'Processing settings: {lclbl}'
        hcbtn.bgcolor = 'INDIGO'
        lcbtn.bgcolor = 'GREEN'
        page.update()

    def close_dlg(e):           #event handler for closing the dialog box
        dlg.open = False
        ec, ct = classifier()
        disp_stats(ct, ec)
        page.update()

    def get_directory_result(e: FilePickerResultEvent):     #event handler for the FilePicker class in flet. 
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()
    
    def chkdir(e):                           # this function checks if the file path is correct or not and add_progress_bar. 
        dlg.open = True
        print(directory_path.value)
        if os.path.exists(directory_path.value):
            
            if hcbtn.bgcolor == 'GREEN' and lcbtn.bgcolor == 'INDIGO':
                write_config_settings(directory_path.value, 'high')
                # return directory_path.value, 'high'
            elif hcbtn.bgcolor == 'INDIGO' and lcbtn.bgcolor == 'GREEN':
                write_config_settings(directory_path.value, 'low')
                # return directory_path.value, 'low'
            add_progress_bar()
            dlg.title = ft.Text('Success!')
            dlg.content = ft.Text('Processing Started!')
        else:
            err_dlg.visible = True
            page.update()

    dlg = ft.AlertDialog(
            title = title_text,
            actions=[
                ft.TextButton('OK', on_click = (close_dlg)), 
            ]
        )    
    err_dlg = ft.AlertDialog(
        title= Text('Error in File path')
    )
    def write_config_settings(path, cont_set):      # writes the config settings given by the user to config.json file
        config = {
            'Path' : path, 
            'Contrast Settings': cont_set
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)

    def add_progress_bar():                         # progress bar for not leaving the user hanging when the program tries to compute 
        # activate the progress bar 
        pb.visible = True
        pbtext.visible = True

    def disp_stats(cats, err_cnt):   # display stats function 
    
        page.controls.clear()
        
        fig, ax = plt.subplots()
        
        ax.bar(cats, err_cnt, color='blue')
        # Adding labels and title
        ax.set_xlabel('Error type')
        ax.set_ylabel('Frequency')
        ax.set_title('Segregation error rates')
        page.title = 'Stats - Little Colorful Things v1.0'
        page.add(
            Row(
                [ Text('Segregation error counts in current set: ')],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            MatplotlibChart(fig, expand=True),

            #adding all details to the chart for displaying the stats 

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

    directory_path = ft.Text()
    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
    page.overlay.append(get_directory_dialog)
    page.dialog = dlg
    
    hcbtn = ElevatedButton('High Contrast', on_click=hc_btn_click, bgcolor='INDIGO')
    lcbtn = ElevatedButton('Low Contrast', on_click=lc_btn_click, bgcolor='INDIGO')
    
    startbtn = ElevatedButton("Start Processing",on_click = chkdir)
    pb = ft.ProgressBar(width=400, color='amber')
    pbtext = Text('Processing the images...')
    pb.visible = False
    pbtext.visible = False
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
        
        Row([Text('Choose a folder from This PC')]),
        
        Row([ElevatedButton(
                    "Open directory",
                    icon = icons.FOLDER_OPEN,
                    on_click = lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
            ]
        ), 
        
        Row([Text('Chosen directory: '), directory_path]),
        
        Row(
            [Text('Choose contrast settings: ')]
        ), 
        
        Row(
            [lcbtn, hcbtn]
        ),
        
        Row(
            [lbl]
        ),
        
        Row(
            [startbtn], alignment=ft.MainAxisAlignment.END
        ),
        Row(
                [pbtext]
            ),
        ft.Column([pb]),
    )
    
    page.update()

def classifier():                   # Main function that executes all the processing functions. 
    cats = []
    err_cnt = np.zeros(7)
    raw_images = []
    with open('config.json', 'r') as f:
        config = json.load(f)

    IMG_SAVE_PATH_TEST = config['Path']
    CONT_SET = config['Contrast Settings']

    print('got file path: ', IMG_SAVE_PATH_TEST)        #check if file path was passed correctly

    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    for image_name in os.listdir(IMG_SAVE_PATH_TEST):
        
        if any(image_name.lower().endswith(ext) for ext in image_extensions):
            raw_images.append(cv2.imread(os.path.join(IMG_SAVE_PATH_TEST, image_name), cv2.IMREAD_UNCHANGED))
    
    print(len(raw_images))
    for img in raw_images:

        if CONT_SET == 'high':                          #preprocess function call
            edges = preprocess_image_high_cont(img)
        else:
            edges = preprocess_image_low_cont(img)

        masks = generate_mask(edges, init_mask_gen)     # mask generator (SAM implementation)
        
        # show_mask(img, masks)                         
        
        cell_array, cluster_array = separate_clusters(masks, img)

        temp = process_cluster(cluster_array)       

        cell_array += temp                              #adding all cells to a cell_array
        
        cats_temp, err_cnt_temp = stats(cell_array)
        
        cats = cats_temp                                #categories of error types
        
        err_cnt += err_cnt_temp                         #error count is cumulatively stored in err_cnt

    print(err_cnt, cats)
    return err_cnt, cats

flet.app(target=get_main_window)                # method call for get_main_window









