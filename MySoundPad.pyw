import time

import dearpygui.dearpygui as dpg
from inspect import stack
from os.path import dirname, abspath
# app
from pygame import mixer  # Playing sound
import soundfile as sf
import sounddevice as sd


class App:
    running = True
    drag_active = False
    w_size = width, height = 800, 485
    w_pos = x, y = 1920//2 - width//2, 1080//2 - height//2
    
    mixer.init()
    dir: str = dirname(
        abspath(stack()[0].filename)
    ).removesuffix('\\PyInstaller\\loader').removesuffix('\\_internal')
    f_name = f'{dir}\\Helldivers_2_Initial_Helldive_.mp3'
    
    _c2: mixer.Channel = Ellipsis
    sound_length: float = 0
    start_play: float = 0
    devise_id = -1
    devises = list()
    ids = None
    
    def __init__(self):
        """ Инициализация Dear PyGui """
        dpg.create_context()
        data, st = self.set_w_data()
        
        """ Загрузка SysFonts """
        with dpg.font_registry():
            arial_font_20 = dpg.add_font('C:\Windows\Fonts\ARIALN.TTF', 20)
            arial_font_27 = dpg.add_font('C:\Windows\Fonts\ARIALN.TTF', 27)
            arial_font_40 = dpg.add_font('C:\Windows\Fonts\ARIALN.TTF', 40)
            arial_font_75 = dpg.add_font('C:\Windows\Fonts\ARIALNB.TTF', 75)
        
        """ THEMES """
        with dpg.theme() as exit_button_style:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (230, 75, 50), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered,
                    (230//3, 75//3, 150//3), category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (70, 70, 70), category=dpg.mvThemeCat_Core)
        with dpg.theme() as minimise_button_style:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 175, 230), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, (100//3, 150//3, 150//3),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (70, 70, 70), category=dpg.mvThemeCat_Core)
        with dpg.theme() as comment_font_style:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (120, 120, 120), category=dpg.mvThemeCat_Core)
        
        """ Загрузка TEXTURES """
        with dpg.texture_registry():
            tb_width, tb_height, _, tb_data = dpg.load_image(f"{App.dir}/ico.png")
            dpg.add_static_texture(width=tb_width, height=tb_height, default_value=tb_data, tag="main_ico")
        
        """ ОБРАБОТКА НАЖАТИЙ """
        with dpg.handler_registry():
            dpg.add_mouse_drag_handler(callback=App.drag_handle)
            dpg.add_mouse_click_handler(callback=App.mouse_down_callback)
            dpg.add_mouse_release_handler(callback=App.mouse_release_callback)
        
        """ Create MAIN window """
        with dpg.window(
                tag="mainWindow"
        ) as main_win:
            """manu-bar"""
            with dpg.menu_bar(show=False):
                # ico
                dpg.add_image('main_ico')
                # file
                with dpg.menu(label='File'):
                    """ open mp3 """
                    dpg.add_button(label="Open", callback=lambda: dpg.show_item("fileDialog"))
                    # comment
                    dpg.add_text(default_value='open 1 sound file')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                    
                    dpg.add_separator()
                # devises
                with dpg.menu(label='Devise'):
                    """ VB list text """
                    dpg.add_button(label="VB-list", callback=lambda: dpg.show_item("SD_IX"))
                    # comment
                    dpg.add_text(default_value='all devise indexes')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                    
                    dpg.add_separator()
                    
                    """ id """
                    dpg.add_input_int(default_value=data['devise']['id'], tag='DV_I_I_I')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    # comment
                    dpg.add_text(default_value='current devise index')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                    
                    dpg.add_separator()
                    
                    """ name """
                    dpg.add_input_text(default_value=data['devise']['name'], tag='DV_SI')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    # comment
                    dpg.add_text(default_value='current devise name')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                    
                    dpg.add_separator()
                    
                    """ detecting """
                    dpg.add_button(label="detect devise", callback=lambda: App.detect_devise())
                    # comment
                    dpg.add_text(default_value='set devise from name (del id)')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                # minimise
                dpg.add_button(label='Mini', callback=App.minimise, pos=(App.width - 80, 0), width=40)
                dpg.bind_item_theme(dpg.last_item(), minimise_button_style)
                # exit
                dpg.add_button(label='Exit', callback=App.exit, pos=(App.width - 40, 0), width=40)
                dpg.bind_item_theme(dpg.last_item(), exit_button_style)
            
            """main group"""
            with dpg.group(horizontal=False, horizontal_spacing=50):
                # MAIN
                with dpg.group(horizontal=True):
                    dpg.add_text("My Sound Pad")
                    dpg.bind_item_font(dpg.last_item(), arial_font_75)
                    dpg.add_loading_indicator(tag='LI_PM', pos=(420, 34), style=-1, radius=4, show=False)
                
                dpg.add_spacer(height=15)
                dpg.add_separator()
                dpg.add_spacer(height=15)
                
                # FILE
                dpg.add_input_text(tag='SF_TI', readonly=True, default_value=App.f_name, width=-1)
                dpg.bind_item_font(dpg.last_item(), arial_font_27)
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value='selected file')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                    with dpg.group(horizontal=False):
                        dpg.add_text(default_value='               played file: -', tag='PB_PS')
                        dpg.bind_item_font(dpg.last_item(), arial_font_20)
                        dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                        dpg.add_progress_bar(
                            default_value=0, tag='PB_PM', width=-1, height=10
                        )
                
                dpg.add_spacer(height=20)
                dpg.add_separator()
                
                # CHECKBOXES
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label='play in headphones', tag='CBP_H', default_value=data['play']['headphones'])
                    dpg.bind_item_font(dpg.last_item(), arial_font_27)
                    dpg.add_checkbox(label='play in microphone', tag='CBP_M', default_value=data['play']['microphone'])
                    dpg.bind_item_font(dpg.last_item(), arial_font_27)
                dpg.add_text(default_value='set play channels')
                dpg.bind_item_font(dpg.last_item(), arial_font_20)
                dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                
                dpg.add_spacer(height=20)
                
                # VOLUME
                with dpg.group(horizontal=True):
                    dpg.add_drag_int(
                        tag='DIV', default_value=data['play']['volume'], callback=App.volume_callback,
                        width=-65
                    )
                    dpg.bind_item_font(dpg.last_item(), arial_font_27)
                    dpg.add_text(default_value='volume')
                    dpg.bind_item_font(dpg.last_item(), arial_font_20)
                    dpg.bind_item_theme(dpg.last_item(), comment_font_style)
                
                dpg.add_separator()
                dpg.add_spacer(height=20)
                dpg.add_separator()
                
                # BUTTONS
                with dpg.group(horizontal=True):
                    dpg.add_button(label='Play', tag='P_BTN', callback=App.play_action, width=App.width//2)
                    dpg.bind_item_font(dpg.last_item(), arial_font_40)
                    dpg.add_button(label='Stop', tag='S_BTN', callback=App.stop_action, width=-1)
                    dpg.bind_item_font(dpg.last_item(), arial_font_40)
        
        """ FILE MANAGER """
        with dpg.file_dialog(
                callback=App.file_dialog_callback,
                directory_selector=False, file_count=1,
                show=False, width=550, height=350,
                tag='fileDialog'
        ):
            dpg.add_file_extension("sounds (*.mp3){.mp3}")
            dpg.add_file_extension(".*")
        
        """ SOUND DEVISES """
        with dpg.window(
                width=350, height=350, no_title_bar=True, tag='SD_IX', show=False, pos=(540, 50), no_move=True
        ):
            dpg.add_text(default_value='All sound devises')
            text = ''
            for d in sd.query_devices():
                if d['max_output_channels'] != 0 and d['hostapi'] == 0:
                    text += f"{d['index']} - {d['name']}\n"
                    App.devises.append(d)
            dpg.add_input_text(default_value=text, multiline=True, width=-1, height=-50)
            with dpg.group(horizontal=True):
                dpg.add_button(label='ok', callback=lambda: dpg.hide_item('SD_IX'))
                dpg.add_button(label='debug - all devises', callback=lambda: dpg.show_item('DB_SD_IX'))
        
        """ DEBUG SOUND DEVISES """
        with dpg.window(
                width=570, height=350, no_title_bar=True, tag='DB_SD_IX', show=False, pos=(540, 50), no_move=True
        ):
            dpg.add_text(default_value='All devises on PC')
            dpg.add_input_text(default_value=sd.query_devices(), multiline=True, width=-1, height=-50)
            dpg.add_button(label='ok', callback=lambda: dpg.hide_item('DB_SD_IX'))
        
        """ ERROR """
        with dpg.window(
                width=570, modal=True, height=350, no_title_bar=True, tag='FLR', show=False, pos=(110, 60)
        ):
            dpg.add_text(default_value='ERRORS')
            dpg.add_input_text(default_value='', tag='FLR_TI', multiline=True, width=-1, height=-50)
            with dpg.group(horizontal=True):
                dpg.add_button(label='ok', callback=lambda: dpg.hide_item('FLR'))
                dpg.add_button(label='clear', callback=lambda: dpg.set_value('FLR_TI', ''))
        
        if st:
            with dpg.window(
                    width=App.width - 6, height=App.height - 7, tag='getting_started',
                    no_resize=True, modal=True, no_move=True, no_collapse=True
            ):
                with dpg.group(horizontal=True):
                    dpg.add_text('GETTING STARTING')
                    dpg.bind_item_font(dpg.last_item(), arial_font_75)
                    dpg.add_image('main_ico')
                dpg.add_input_text(
                    default_value='Hello. This My sound pad.\n'
                                  'That use this application you need set VirtualCable.\n'
                                  'In App dir Im copy my VB Cable.\n'
                                  '\n'
                                  'Im recommend copy this guid in txt file. You can delete config, to see this guid\n'
                                  'First steps:\n'
                                  '1) set VB;\n'
                                  '2) restart App;\n'
                                  '3) find him in `Devise/VB-list` on bar\n'
                                  '4) copy id, or name in field.\n'
                                  '5) click \"detect devise\"\n'
                                  'Congratulation, you set up app configs\n'
                                  '\n'
                                  'How Use:\n'
                                  '1) find your sound in `File/File`\n'
                                  '2) set configs\n'
                                  '3) select your Virtual Cable in Discord/Game/other app\n'
                                  '4) click play\n'
                                  '5) to stop click stop\n'
                                  '\n'
                                  'Tips: (REQUIREMENT TO READING)\n'
                                  '* use standard `sound` dir in main app patch\n'
                                  '* `volume` change ONLY headphone volume, not microphone\n'
                                  '* you can find new file, before ending current playing file.'
                                  '    Them name on `selected` and `played` file field be not equal\n'
                                  '* read tracback text, him can help fix this error in future\n'
                                  '* ids in `VB-list` not fuller, you can click on `debug - all devises` to see all\n'
                                  '\n'
                                  'GOOD USING. Thanks.\n',
                    multiline=True,
                    height=-1,
                    width=-1
                )
        
        dpg.bind_font(arial_font_20)
        """ START """
        dpg.create_viewport(
            title='My Sound Pad', width=App.width, height=App.height,
            decorated=False, x_pos=App.x, y_pos=App.y
        )
        dpg.set_primary_window(main_win, True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        
        if App.devise_id is None:
            App.detect_devise()
    
    @staticmethod
    def detect_devise():
        App.ids = set()
        dv_i_i_i = dpg.get_value('DV_I_I_I')
        
        if dv_i_i_i > 0:
            App.ids.add(dv_i_i_i)
            App.devise_id = dv_i_i_i
        else:
            dv_si = dpg.get_value('DV_SI')
            for i in App.devises:
                if dv_si in i['name']:
                    App.ids.add(i['index'])
            App.devise_id = min(App.ids)
        dpg.set_value('DV_I_I_I', App.devise_id)
    
    @staticmethod
    def show_err(err):
        text = (f'EROOR {type(err)}:\n'
                f'   {str(err)}\n'
                f'   current ids: {str(App.ids)}\n')
        text += 'Description: '
        match (err.args[-1], type(err)):
            case (-9998, _):
                text += 'not valid sound devise. Change id'
            case ('Error querying device -1', _):
                text += 'devise not detect. Find devises in Devise on bar'
            case (_, t):
                if t is FileNotFoundError:
                    text += 'File not found. Check ext or try create dir'
                else:
                    text += 'problem onto app'
        text += '\n\n'
        dpg.set_value('FLR_TI', dpg.get_value('FLR_TI') + text)
        dpg.show_item('FLR')
    
    @staticmethod
    def play_in_headphones(s2):
        c2 = Ellipsis
        try:
            c2 = mixer.Channel(1)
            c2.play(s2)
        except Exception as err:
            App.show_err(err)
        # working with all
        App._c2 = c2
    
    @staticmethod
    def play_in_microphone(f_name):
        try:
            data, fs = sf.read(f_name, dtype='float32')
            sd.play(data, fs, device=App.devise_id)
        except sd.PortAudioError as err:
            App.show_err(err)
    
    @staticmethod
    def play_action(_):
        try:
            s2 = mixer.Sound(App.f_name)
        except Exception as err:
            App.show_err(err)
            return
        App.sound_length = s2.get_length()
        App.start_play = time.time()
        App.play_in_headphones(s2) if dpg.get_value('CBP_H') else Ellipsis
        App.play_in_microphone(App.f_name) if dpg.get_value('CBP_M') else Ellipsis
        dpg.show_item('LI_PM')
        dpg.set_value('PB_PS', f'               played file: {App.f_name}')
    
    @staticmethod
    def stop_action(_):
        mixer.stop()
        sd.stop()
        dpg.hide_item('LI_PM')
        dpg.set_value('PB_PM', 0)
        App.sound_length = 0
        dpg.set_value('PB_PS', f'               played file: -')
    
    @staticmethod
    def volume_callback(_):
        if App._c2 is not Ellipsis:
            v = dpg.get_value('DIV')
            if v > 0:
                App._c2.set_volume(v/100)
    
    @classmethod
    def run(cls):
        """ MAIN-LOOP """
        while App.running:
            dpg.render_dearpygui_frame()
            if App.sound_length != 0:
                p = (time.time() - App.start_play)/App.sound_length
                if 0 < p < 1:
                    dpg.set_value('PB_PM', p)
                elif p >= 1:
                    dpg.hide_item('LI_PM')
                    dpg.set_value('PB_PM', 0)
                    App.sound_length = 0
                    dpg.set_value('PB_PS', f'               played file: -')
        
        dpg.destroy_context()
    
    @staticmethod
    def set_w_data():
        import json
        try:
            with open('config.json', 'r') as f:
                data = json.load(f)
            App.devise_id = data['devise']['id']
            return data, False
        except FileNotFoundError:
            return {
                "devise": {
                    "id": -1,
                    "name": ""
                },
                "play": {
                    "microphone": True,
                    "headphones": True,
                    "volume": 100
                }
            }, True
    
    @staticmethod
    def exit():
        import json
        with open('config.json', 'w') as f:
            data = {
                'devise': {
                    'id': App.devise_id,
                    'name': dpg.get_value('DV_SI'),
                },
                'play': {
                    'microphone': dpg.get_value('CBP_M'),
                    'headphones': dpg.get_value('CBP_H'),
                    'volume': dpg.get_value('DIV'),
                }
            }
            json.dump(data, f, indent=2)
        App.running = False
    
    @staticmethod
    def minimise():
        dpg.minimize_viewport()
    
    @staticmethod
    def mouse_down_callback(_):
        if dpg.get_mouse_pos()[1] <= 0 and dpg.is_item_hovered('mainWindow'):
            App.drag_active = not App.drag_active
    
    @staticmethod
    def mouse_release_callback(_):
        if App.drag_active:
            App.drag_active = not App.drag_active
    
    @staticmethod
    def drag_handle(_, data):
        if App.drag_active:
            dpg.set_viewport_width(dpg.get_viewport_width())
            dpg.set_viewport_height(dpg.get_viewport_height())
            p = dpg.get_viewport_pos()
            dpg.set_viewport_pos((p[0] + data[1], p[1] + data[2]))
    
    @staticmethod
    def file_dialog_callback(_, data):
        App.f_name = data['file_path_name']
        dpg.set_value('SF_TI', App.f_name)


if __name__ == '__main__':
    App().run()
