import math
import obspython as obs
import pywinctl as pwc
import time

description = (
    "ZOOM AND FOLLOW"
   
)
source = ""
cWidth = ""
cHeight = ""
follow_on = False
seconds = 0.1


def populate_list_property_with_source_names(list_property):
    """
    Updates Zoom Source's available options.

    Checks a source against SOURCES to determine availability.
    """
    sources = obs.obs_enum_sources()
    if sources is not None:
        obs.obs_property_list_clear(list_property)
        obs.obs_property_list_add_string(list_property, "", "")
        for source in sources:
            source_type = obs.obs_source_get_id(source)
            # Filter out sources based on their type
            if source_type in ["window_capture", "game_capture", "monitor_capture"]:
                name_val = obs.obs_source_get_name(source)
                name = name_val + "||" + source_type
                obs.obs_property_list_add_string(list_property, name_val, name)
    obs.source_list_release(sources)


def script_properties():
    props = obs.obs_properties_create()
    source_property = obs.obs_properties_add_list(props, "source", "Source", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    populate_list_property_with_source_names(source_property)
    obs.obs_properties_add_button(props, "refresh_sources", "Refresh Sources", populate_list_property_with_source_names)
    obs.obs_properties_add_int(props, "width", "Canvas Width", 0, 9999, 1)
    obs.obs_properties_add_int(props, "height", "Canvas Height",0,9999,1)

    return props


def script_update(settings):
    # populate_list_property_with_source_names((obs.obs_properties_get(settings)))
    global source
    source = obs.obs_data_get_string(settings, "source")
    global cWidth
    cWidth = obs.obs_data_get_int(settings, "width")
    global cHeight
    cHeight = obs.obs_data_get_int(settings, "height")
    log(source)


def script_description():
    return description


def script_load(settings):
    zoomoff = obs.obs_hotkey_register_frontend("zoom_off", "Turn Zoom Off", zoom_off)
    zoomtwo = obs.obs_hotkey_register_frontend("zoom_two", "Zoom Two", zoom_two)
    zoomfour = obs.obs_hotkey_register_frontend("zoom_four", "Zoom Four", zoom_four)
    followtoggle = obs.obs_hotkey_register_frontend("follow_toggle", "Follow Toggle", follow_toggle)
    hotkey_save_array = obs.obs_data_get_array(settings, "ZOOM/FOLLOW")
    obs.obs_hotkey_load(zoomoff, hotkey_save_array)
    obs.obs_hotkey_load(zoomtwo, hotkey_save_array)
    obs.obs_hotkey_load(zoomfour, hotkey_save_array)
    obs.obs_hotkey_load(followtoggle, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)


def get_cursor_position():
    return pwc.getMousePos()
  

def log(message):
    print("[LOG INFO] " + str(message))


def zoom_off(pressed):
    if pressed:
        curX = get_width()
        curY = get_height()
        global cWidth
        global cHeight
        increase_zoom(curX, curY, cWidth, cHeight)
        set_x_and_y(0,0)


def zoom_two(pressed):
    if pressed:
        curX = get_width()
        curY = get_height()
        global cWidth
        global cHeight
        increase_zoom(curX, curY, cWidth/2, cHeight/2)


def zoom_four(pressed):
    if pressed:
        curX = get_width()
        curY = get_height()
        global cWidth
        global cHeight
        increase_zoom(curX, curY, cWidth/4, cHeight/4)


def get_selected_source():
    
    global source
    text = source.split('||')
    sourceName = text[0]
    return sourceName


def obs_set_crop_settings(width, height):
    sourceN = obs.obs_get_source_by_name(get_selected_source())
    crop = obs.obs_source_get_filter_by_name(sourceN, "MultiZoom")
    crop_settings = obs.obs_source_get_settings(crop)
    #log(obs.obs_data_get_json(crop_settings))
    obs.obs_data_set_int(crop_settings, "cx", width)
    obs.obs_data_set_int(crop_settings, "cy", height)
    obs.obs_data_set_bool(crop_settings, "relative", False)
    obs.obs_source_update(crop, crop_settings)


def get_height():
    sourceN = obs.obs_get_source_by_name(get_selected_source())
    crop = obs.obs_source_get_filter_by_name(sourceN, "MultiZoom")
    crop_settings = obs.obs_source_get_settings(crop)
    #log(obs.obs_data_get_json(crop_settings))
    curY = obs.obs_data_get_int(crop_settings, "cy")
    return curY

    
def get_width():
    sourceN = obs.obs_get_source_by_name(get_selected_source())
    crop = obs.obs_source_get_filter_by_name(sourceN, "MultiZoom")
    crop_settings = obs.obs_source_get_settings(crop)
    #log(obs.obs_data_get_json(crop_settings))
    curX = obs.obs_data_get_int(crop_settings, "cx")
    return curX


def increase_zoom(cx, cy, nx, ny):
    while cx != nx or cy != ny:
        if cx > nx:
            cx -= 10
            if cx < nx:
                cx = nx
        elif cx < nx:
            cx += 10
            if cx > nx:
                cx = nx

        if cy > ny:
            cy -= 6
            if cy < ny:
                cy = ny
        elif cy < ny:
            cy += 6
            if cy > ny:
                cy = ny
        obs_set_crop_settings(cx, cy)

        time.sleep(0.01)
    #log("Zoom Down")

   
def follow_toggle(pressed):
    if pressed:
        mouse = pwc.getMousePos()
        log(f"PosMouseX/{mouse.x} PosMouseY{mouse.y}")
        global follow_on
        if follow_on is True:
            follow_on = False
        else:
            follow_on = True
        log(follow_on)

def set_x_and_y(x,y):
    sourceName = obs.obs_get_source_by_name(get_selected_source())
    crop = obs.obs_source_get_filter_by_name(sourceName, "MultiZoom")
    crop_settings = obs.obs_source_get_settings(crop)
    #log(obs.obs_data_get_json(crop_settings))
    obs.obs_data_set_int(crop_settings, "top", y)
    obs.obs_data_set_int(crop_settings, "left", x)
    obs.obs_data_set_bool(crop_settings, "relative", False)
    obs.obs_source_update(crop, crop_settings) 
    


def script_tick(seconds):
    global follow_on
    if follow_on is True: 
        # Get mouse Pos          
        mouse = pwc.getMousePos()
        curX = get_width()
        curY = get_height()
        global cWidth
        global cHeight
        cx = mouse.x - curX if mouse.x > curX else mouse.x
        cy = mouse.y - curY if mouse.y > curY else mouse.y
       
        x = 0 if mouse.x < (curX/2) else cx + (curX/2) 
        x = cHeight if mouse.x > cWidth  else cx + (curX/2)
        
        y = 0 if mouse.y < (curY/2) else cy + (curY/2) 
        y = cHeight if mouse.y > cHeight  else cy + (curY/2)

        
        set_x_and_y(round_up(x),round_up(y))
        log(f"PosMouseX/{x} PosMouseY{y}")
        
        # Workout level of Zoom
        # adjust level of tracking
        # reset the settings
        
            

def round_up(n):
   
    return math.trunc(n)

