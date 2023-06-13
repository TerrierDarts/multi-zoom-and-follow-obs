# Multi Level Zoom and Follow 

Script for OBS and Multi Level Zooms and Mouse Follow
Setting this up requires pywict1

Once added to OBS and you will need to add a `Crop/Pad` Filter to the source you want to zoom into called `MultiZoom`

## TO DO

- Add Following to track correctly
- Auto Turn off follow when zoom is turned off
- Turn on Follow if going from Off to On
- Make sure the when going from 2 > 4 or 4 > 2 if follow is off it zoooms correctly

Problems with the Follow

1 - I need to workout which screen is been captured, as the limits will be different on each screen,
2 - I need to correctly work out the limits depending on what zoom level is active
3 - (easy) If Zoom is off follow turns off so nothing moves and set x/y to 0
4 - if zoom is off and i zoom in or out i dont want it getting thrown off


## OBSRaw Hotkeys (WEBSOCKET 5)

### Zoom Off

```json
{
  "requestType": "TriggerHotkeyByName",
  "requestData": {
    "hotkeyName": "zoom_off"
  }
}
```

### Zoom 2x

```json
{
  "requestType": "TriggerHotkeyByName",
  "requestData": {
    "hotkeyName": "zoom_two"
  }
}
```

### Zoom 4x

```json
{
  "requestType": "TriggerHotkeyByName",
  "requestData": {
    "hotkeyName": "zoom_four"
  }
}
```

### Follow Toggle

```json
{
  "requestType": "TriggerHotkeyByName",
  "requestData": {
    "hotkeyName": "follow_toggle"
  }
}
```
