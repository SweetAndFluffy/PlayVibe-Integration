## Limits

### Points

The points value is not limited in any way. It is given to the current mode, which converts it to a intensity setting for every vibrator the mode controls. 

### Intensity

The intensity is an integer value between 0 and 100. 

### Intervals

Intervals in the config are (in theory) limitless, but cannot overlap each other.

## API

### Get current amount of points GET `/points/`

Returns the current amount of pleasure points.

### Set current amount of points GET `/points/<points>`

Sets the current amount of points.

### Get the configuration of the vibrators GET `/config/`

Gets the current configuration string (JSON).

### Set the configuration string of the vibrators POST `/config/ data=JSON`

Sets the current configuration of the vibrators.
