# imports
import machine
import math

#######################################
# Pin and constant definitions
#######################################
SEVEN_SEGMENT_START_PIN = 0
ANALOGUE_INPUT_PIN_POT = 26
ANALOGUE_INPUT_PIN_LDR = 27
ANALOGUE_INPUT_PIN_NTC = 28
BUTTON_PIN = 16
DISPLAY_COUNT = 4
MEASUREMENT_COUNT = 16
DECIMAL_PRECISION = 3
ADC_RANGE = float((math.pow(2, 16) - 1))

# HEX values for 7 segment display values
digit_list_hex = [
    0x40,  # 0
    0x79,  # 1
    0x24,  # 2
    0x30,  # 3
    0x19,  # 4
    0x12,  # 5
    0x02,  # 6
    0x78,  # 7
    0x00,  # 8
    0x10,  # 9
    0x08,  # A
    0x03,  # B
    0x46,  # C
    0x21,  # D
    0x06,  # E
    0x0E,  # F
    0x7F   # Empty
]

#######################################
# Global variables
#######################################
display_value = 0
segment_pins = []
display_select_pins = []
analogue_voltage_pin_pot = None
analogue_voltage_pin_ldr = None
analogue_voltage_pin_ntc = None
button_pin = None
current_display_index = DISPLAY_COUNT - 1  # to keep track of which digit is currently being displayed
display_timer = None
prev_analogue_voltage = -1
selected_sensor = 0  # 0: Potentiometer, 1: LDR, 2: NTC

#######################################
# Function definitions
#######################################

# Function to read the ADC pin and
# to convert the digital value to a voltage level in the 0-3.3V range
# This function updates the value of the display_value global variable
def read_analogue_voltage():
    global display_value, prev_disp_val, display_timer
    global prev_analogue_voltage, DECIMAL_PRECISION

    if selected_sensor == 0:
        pin = analogue_voltage_pin_pot
    elif selected_sensor == 1:
        pin = analogue_voltage_pin_ldr
    else:
        pin = analogue_voltage_pin_ntc

    # Take MEASUREMENT_COUNT measurements and average them
    total_value = 0
    for _ in range(MEASUREMENT_COUNT):
        total_value += pin.read_u16()
    average_value = total_value // MEASUREMENT_COUNT

    # Convert the average digital value to an analogue voltage value
    analogue_voltage = round((average_value / ADC_RANGE) * 3.3, DISPLAY_COUNT - 1)

    if analogue_voltage != prev_analogue_voltage:
        prev_analogue_voltage = analogue_voltage

        new_display_value = int(analogue_voltage * math.pow(10, DECIMAL_PRECISION))

        # Temperature Reading
        # When using the NTC, change the line below to
        # if selected_sensor == 2:
        if selected_sensor == 2:
            DECIMAL_PRECISION = 2
            temp = 0
            try:
                # Use the formula from
                # https://docs.wokwi.com/parts/wokwi-ntc-temperature-sensor
                temp = round(1 / (math.log(1 / (ADC_RANGE / average_value - 1)) / 3950 + 1.0 / 298.15) - 273.15, 1)
                print(f'temp: {temp} C')
            except:
                pass
            new_display_value = int(temp * math.pow(10, DECIMAL_PRECISION))

        max_val = math.pow(10, DISPLAY_COUNT) - 1
        if new_display_value > max_val:
            print(f'warn: {new_display_value} exceeds {max_val}, clipping')
            new_display_value = max_val

        if display_value != new_display_value:
            print(f'voltage: {analogue_voltage} mV')
            display_value = new_display_value

            disable_display_timer()
            current_display_index = DISPLAY_COUNT - 1
            display_digit(16, -1)
            enable_display_timer()

# Function to disable timer that triggers scanning 7 segment displays
def disable_display_timer():
    global display_timer
    display_timer.deinit()

# Function to enable timer that triggers scanning 7 segment displays
def enable_display_timer():
    global display_timer
    display_timer.init(period=4, mode=machine.Timer.PERIODIC, callback=scan_display)

# Function to handle scanning 7 segment displays
# Display the value stored in the display_value global variable
# on available 7-segment displays
def scan_display(timer_int):
    global current_display_index, display_value

    # Extract the digit corresponding to the current display index
    # Only display positive values
    digit = int((abs(display_value) // math.pow(10, current_display_index))) % 10

    # Display the digit,
    # enable the decimal point if the current digit index equals to the set decimal precision
    display_digit(digit, current_display_index,
                  current_display_index == DECIMAL_PRECISION and 0 != DECIMAL_PRECISION)

    # Move to the next display
    current_display_index = (current_display_index - 1)
    if current_display_index < 0:
        current_display_index = DISPLAY_COUNT - 1

# Function display the given value on the display with the specified index
# dp_enable specifies if the decimal point should be on or off
def display_digit(digit_value, digit_index, dp_enable=False):
    # Ensure the value is valid
    if digit_value < 0 or digit_value > len(digit_list_hex):
        return

    # Deselect all display select pins
    for pin in display_select_pins:
        pin.value(0)

    # Set the segments according to the digit value
    mask = digit_list_hex[digit_value]
    for i in range(7):  # 7 segments from A to G
        segment_pins[i].value((mask >> i) & 1)

    segment_pins[7].value(1 if not dp_enable else 0)

    # If digit_index is -1, activate all display select pins
    if digit_index == -1:
        for pin in display_select_pins:
            pin.value(1)
    # Otherwise, ensure the index is valid and activate the relevant display select pin
    elif 0 <= digit_index < DISPLAY_COUNT:
        display_select_pins[digit_index].value(1)

# Function to test available 7-segment displays
def display_value_test():
    global display_value

    disable_display_timer()
    current_display_index = 0

    for i in range(0, len(digit_list_hex)):
        display_digit(i, -1, i % 2 != 0)

    for i in range(0, len(digit_list_hex)):
        display_digit(i, DISPLAY_COUNT - 1 - (i % DISPLAY_COUNT), True)

    enable_display_timer()

# Function to handle the push button interrupt
def button_handler(pin):
    global selected_sensor
    if pin.value() == 0:  # Check if button is still pressed
        selected_sensor = (selected_sensor + 1) % 3  # Cycle through the sensors
        read_analogue_voltage()

# Function to setup GPIO/ADC pins, timers, and interrupts
def setup():
    global segment_pins, display_select_pins, analogue_voltage_pin_pot, analogue_voltage_pin_ldr, analogue_voltage_pin_ntc, button_pin, display_timer

    # Set up display select pins
    for i in range(SEVEN_SEGMENT_START_PIN + 8, SEVEN_SEGMENT_START_PIN + 8 + DISPLAY_COUNT):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.value(0)
        display_select_pins.append(pin)

    # Set up seven segment pins
    for i in range(SEVEN_SEGMENT_START_PIN, SEVEN_SEGMENT_START_PIN + 8):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.value(1)
        segment_pins.append(pin)

    analogue_voltage_pin_pot = machine.ADC(ANALOGUE_INPUT_PIN_POT)
    analogue_voltage_pin_ldr = machine.ADC(ANALOGUE_INPUT_PIN_LDR)
    analogue_voltage_pin_ntc = machine.ADC(ANALOGUE_INPUT_PIN_NTC)

    # Set up the push button pin
    button_pin = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)

    # Start the timer interrupt for scanning
    display_timer = machine.Timer()
    enable_display_timer()

if __name__ == '__main__':
    setup()
