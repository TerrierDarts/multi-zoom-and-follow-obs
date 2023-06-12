import math
import obspython as obs
import pywinctl as pwc
import time


description = (
    "ZOOM AND FOLLOW"
   
)

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

  


    return props

def script_update(settings):
    populate_list_property_with_source_names((obs.obs_properties_get(settings)))

def script_description():
    return description

def script_load(settings):
    zoomoff = obs.obs_hotkey_register_frontend("zoom_off", "Turn Zoom Off", zoom_off)
    zoomtwo = obs.obs_hotkey_register_frontend("zoom_two", "Zoom Two", zoom_two)
    zoomfour = obs.obs_hotkey_register_frontend("zoom_four", "Zoom Four", zoom_four)
    followtoggle = obs.obs_hotkey_register_frontend("follow_toggle", "Follow Toggle",follow_toggle)
    hotkey_save_array = obs.obs_data_get_array(settings,"ZOOM/FOLLOW")
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
        increase_zoom(curX,curY,1920,1080)

def zoom_two(pressed):
    if pressed:
        curX = get_width()
        curY = get_height()
        log(f"zoom2 {curX} {curY}")
        increase_zoom(curX,curY,960,540)

def zoom_four(pressed):
    if pressed:
        curX = get_width()
        curY = get_height()
        increase_zoom(curX,curY,480,270)

def get_selected_source():
    #source_name = obs.obs_data_get_string(obs.obs_frontend_get_current_scene())
    #source = obs.obs_get_source_by_name(source_name)
    return "Monitor View"

def obs_set_crop_settings(width,height):
    source = obs.obs_get_source_by_name(get_selected_source())
    crop = obs.obs_source_get_filter_by_name(source, "MultiZoom")
    crop_settings = obs.obs_source_get_settings(crop)
    log(obs.obs_data_get_json(crop_settings))
    obs.obs_data_set_int(crop_settings, "cx", width)
    obs.obs_data_set_int(crop_settings, "cy", height)
    obs.obs_data_set_int(crop_settings, "top", 0)
    obs.obs_data_set_int(crop_settings, "left", 0)
    obs.obs_data_set_bool(crop_settings, "relative", False)
    obs.obs_source_update(crop, crop_settings)
      
   


def get_height():
    source = obs.obs_get_source_by_name(get_selected_source())
    crop = obs.obs_source_get_filter_by_name(source, "MultiZoom")
    crop_settings = obs.obs_source_get_settings(crop)
    log(obs.obs_data_get_json(crop_settings))
    curY = obs.obs_data_get_int(crop_settings, "cy")
    return curY

    
def get_width():
    source = obs.obs_get_source_by_name(get_selected_source())
    crop = obs.obs_source_get_filter_by_name(source, "MultiZoom")
    crop_settings = obs.obs_source_get_settings(crop)
    log(obs.obs_data_get_json(crop_settings))
    curX = obs.obs_data_get_int(crop_settings, "cx")
    return curX


def increase_zoom(cx, cy, nx, ny):
    while cx != nx or cy != ny:
        if cx > nx:
            cx -= 10
        elif cx < nx:
            cx += 10

        if cy > ny :
            cy -= 10
        elif cy < ny:
            cy += 10
        obs_set_crop_settings(cx,cy)
        print(f"Current X: {cx} Current Y: {cy}")

        time.sleep(0.005)  # 10ms delay
    log("Zoom Down")


   
def follow_toggle(pressed):
    if pressed:
        mouse = pwc.getMousePos()
        log(f"PosMouseX/{mouse.x} PosMouseY{mouse.y}")
        #Get mouse Pos
        # Workout level of Zoom
        # adjust level of tracking
        # reset the settings
        source = obs.obs_get_source_by_name(get_selected_source())
        crop = obs.obs_source_get_filter_by_name(source, "MultiZoom")
        crop_settings = obs.obs_source_get_settings(crop)
        log(obs.obs_data_get_json(crop_settings))
    
        curX = obs.obs_data_get_int(crop_settings,"cx")
        curY = obs.obs_data_get_int(crop_settings,"cy")
        log(f"MouseX{curX} MouseY{curY}")

        mouseX = 1920 if mouse.x > 1920 else mouse.x
        mouseY = 1080 if mouse.x > 1080 else mouse.x

        
        newX = round_up(mouseX -(curX/2))
        newY = round_up(mouseY -(curY/2))
        log(f"NewMouseX{mouseX}/ {newX} NewMouseY {mouseY}/{newY}")

        obs.obs_data_set_int(crop_settings, "top", newY)
        obs.obs_data_set_int(crop_settings, "left", newX)
        obs.obs_data_set_bool(crop_settings, "relative",False)
    
        obs.obs_source_update(crop,crop_settings)
        
        obs.obs_data_release(crop_settings)
        obs.obs_source_release(source)
        obs.obs_source_release(crop)

def round_up(n):
   
    return math.trunc(n)

