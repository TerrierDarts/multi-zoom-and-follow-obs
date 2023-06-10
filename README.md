# Multi Level Zoom and Follow 
Script for OBS and Multi Level Zooms and Mouse Follow
Setting this up requires pywict1

Once added to OBS and you will need to add a `Crop/Pad` Filter to the source you want to zoom into called `MultiZoom`

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

