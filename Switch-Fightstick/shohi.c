#include "Joystick.h"

const uint32_t frame  = 10178;
const int report_step = 200000;

typedef enum {
  UP,
  DOWN,
  LEFT,
  RIGHT,
  H_UP,
  H_DOWN,
  H_LEFT,
  H_RIGHT,
  UPLEFT,     // UP + LEFT
  UPRIGHT,
  DOWNLEFT,
  DOWNRIGHT,
  HOLD_UP,    // Hold L Stick UP
  HOLD_DOWN,  // using duration = 0
  HOLD_LEFT,
  HOLD_RIGHT,
  HOLD_CLEAR, // clear Hold L Stick = center
  HOLD_CAM_L, // Hold R Stick Left
  HOLD_CAM_R, // Hold R Stick Right
  HOLD_CAM_C, // clear Hold R Stick = center
  X,
  Y,
  A,
  B,
  L,
  R,
  PLUS,
  HOME,
  LOOP_START,
  NOTHING
} Buttons_t;

typedef struct {
  Buttons_t button;
  uint16_t duration;
} command;

static const command step[] = {
  // Setup controller
  { B,          5 }, // 0
  { NOTHING,  250 },
  { B,          5 },
  { NOTHING,   50 },
  // ここまでコントローラーを認識させるおまじない

  // ゲームに戻る
  { NOTHING,    5 },
  { HOME,       2 },
  { NOTHING,   30 },
  { HOME,       2 },
  { NOTHING,   30 },

  // セーブをする
  { X,          5 },
	{ NOTHING,   30 }, // 10
  { R,          5 },
	{ NOTHING,   15 },
  { A,          5 },
	{ NOTHING,   30 },
  { A,          5 },
	{ NOTHING,  130 },

  // Start
  { HOME,       5 }, // Home
  { NOTHING,   15 },
  { DOWN,       2 },
  { NOTHING,    1 }, // 20
  { RIGHT,      2 },
  { NOTHING,    1 },
  { RIGHT,      2 },
  { NOTHING,    1 },
  { RIGHT,      2 },
  { NOTHING,    1 },
  { RIGHT,      2 },
  { NOTHING,    1 },
  { A,          2 }, // 設定選択
  { NOTHING,    5 }, // 30

  { DOWN,      80 },

  { A,          2 }, // 設定>本体 選択
  { NOTHING,    5 },

  { DOWN,       2 },
  { NOTHING,    1 },
  { DOWN,       2 },
  { NOTHING,    1 },
  { DOWN,       2 },
  { NOTHING,    1 },
  { DOWN,       2 }, // 40
  { NOTHING,    1 },
  { A,          2 }, // 日付と時刻選択
  { NOTHING,   10 },

  { DOWN,       2 },
  { NOTHING,    1 },
  { DOWN,       2 },
  { NOTHING,    1 },

  { A,          2 }, // 現在の日付と時刻
  { NOTHING,    5 },
  { RIGHT,      2 }, // 50
  { NOTHING,    1 },
  { RIGHT,      2 },
  { NOTHING,    1 },
  // 初期設定など1回だけ動かしたいコードはここまで

  // loop Start
  { LOOP_START, 0 },
  // これより下を無限ループ
  { H_UP,      1 }, // 日付を1つ進める
  { RIGHT,     1 },
  { H_RIGHT,   1 },
  { RIGHT,     1 },
  { A,         1 }, // OK
  { NOTHING,   4 }, // 60

  { A,         1 },
  { NOTHING,   4 },
  { LEFT,      1 },
  { H_LEFT,    1 },
  { LEFT,      1 },
};

// Main entry point.
int main(void) {
  // We'll start by performing hardware and peripheral setup.
  SetupHardware();
  // We'll then enable global interrupts for our use.
  GlobalInterruptEnable();
  // Once that's done, we'll enter an infinite loop.
  for (;;)
  {
    // We need to run our task to process and deliver data for our IN and OUT endpoints.
    HID_Task();
    // We also need to run the main USB management task.
    USB_USBTask();
  }
}

// Configures hardware and peripherals, such as the USB peripherals.
void SetupHardware(void) {
  // We need to disable watchdog if enabled by bootloader/fuses.
  MCUSR &= ~(1 << WDRF);
  wdt_disable();

  // We need to disable clock division before initializing the USB hardware.
  clock_prescale_set(clock_div_1);
  // We can then initialize our hardware and peripherals, including the USB stack.

  #ifdef ALERT_WHEN_DONE
  // Both PORTD and PORTB will be used for the optional LED flashing and buzzer.
  #warning LED and Buzzer functionality enabled. All pins on both PORTB and \
           PORTD will toggle when printing is done.
  DDRD  = 0xFF; //Teensy uses PORTD
  PORTD =  0x0;
                  //We'll just flash all pins on both ports since the UNO R3
  DDRB  = 0xFF; //uses PORTB. Micro can use either or, but both give us 2 LEDs
  PORTB =  0x0; //The ATmega328P on the UNO will be resetting, so unplug it?
  #endif
  // The USB stack should be initialized last.
  USB_Init();
}

// Fired to indicate that the device is enumerating.
void EVENT_USB_Device_Connect(void) {
  // We can indicate that we're enumerating here (via status LEDs, sound, etc.).
}

// Fired to indicate that the device is no longer connected to a host.
void EVENT_USB_Device_Disconnect(void) {
  // We can indicate that our device is not ready (via status LEDs, sound, etc.).
}

// Fired when the host set the current configuration of the USB device after enumeration.
void EVENT_USB_Device_ConfigurationChanged(void) {
  bool ConfigSuccess = true;

  // We setup the HID report endpoints.
  ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_OUT_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);
  ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_IN_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);

  // We can read ConfigSuccess to indicate a success or failure at this point.
}

// Process control requests sent to the device from the USB host.
void EVENT_USB_Device_ControlRequest(void) {
  // We can handle two control requests: a GetReport and a SetReport.

  // Not used here, it looks like we don't receive control request from the Switch.
}

// Process and deliver data from IN and OUT endpoints.
void HID_Task(void) {
  // If the device isn't connected and properly configured, we can't do anything here.
  if (USB_DeviceState != DEVICE_STATE_Configured)
    return;

  // We'll start with the OUT endpoint.
  Endpoint_SelectEndpoint(JOYSTICK_OUT_EPADDR);
  // We'll check to see if we received something on the OUT endpoint.
  if (Endpoint_IsOUTReceived())
  {
    // If we did, and the packet has data, we'll react to it.
    if (Endpoint_IsReadWriteAllowed())
    {
      // We'll create a place to store our data received from the host.
      USB_JoystickReport_Output_t JoystickOutputData;
      // We'll then take in that data, setting it up in our storage.
      while(Endpoint_Read_Stream_LE(&JoystickOutputData, sizeof(JoystickOutputData), NULL) != ENDPOINT_RWSTREAM_NoError);
      // At this point, we can react to this data.

      // However, since we're not doing anything with this data, we abandon it.
    }
    // Regardless of whether we reacted to the data, we acknowledge an OUT packet on this endpoint.
    Endpoint_ClearOUT();
  }

  // We'll then move on to the IN endpoint.
  Endpoint_SelectEndpoint(JOYSTICK_IN_EPADDR);
  // We first check to see if the host is ready to accept data.
  if (Endpoint_IsINReady())
  {
    // We'll create an empty report.
    USB_JoystickReport_Input_t JoystickInputData;
    // We'll then populate this report with what we want to send to the host.
    GetNextReport(&JoystickInputData);
    // Once populated, we can output this data to the host. We do this by first writing the data to the control stream.
    while(Endpoint_Write_Stream_LE(&JoystickInputData, sizeof(JoystickInputData), NULL) != ENDPOINT_RWSTREAM_NoError);
    // We then send an IN packet on this endpoint.
    Endpoint_ClearIN();
  }
}

int find_loop_start_step(void){
  for(int i=0;i<(int)(sizeof(step)/sizeof(step[0]))-1;i++){
    if(step[i].button==LOOP_START) return i;
  }
  return 0;
}

typedef enum {
  SYNC_CONTROLLER,
  BREATHE,
  PROCESS,
  DONE,
  CLEANUP
} State_t;
State_t state = SYNC_CONTROLLER;

#define ECHOES 2
int echoes = 0;
USB_JoystickReport_Input_t last_report;

int hold_LX = STICK_CENTER;
int hold_LY = STICK_CENTER;
int hold_RX = STICK_CENTER;
int bufindex = 0;
int duration_count = 0;
int loop_start_step = 0;
uint32_t loop_count = 0;
int complete_flag = false;
int day_count = 0;

void GetNextReport(USB_JoystickReport_Input_t* const ReportData) {
  // Prepare an empty report
  memset(ReportData, 0, sizeof(USB_JoystickReport_Input_t));
  ReportData->LX = STICK_CENTER;
  ReportData->LY = STICK_CENTER;
  ReportData->RX = STICK_CENTER;
  ReportData->RY = STICK_CENTER;
  ReportData->HAT = HAT_CENTER;

  //Hold stick
  ReportData->LX = hold_LX;
  ReportData->LY = hold_LY;
  ReportData->RX = hold_RX;

  // Repeat ECHOES times the last report
  if (echoes > 0)
  {
    memcpy(ReportData, &last_report, sizeof(USB_JoystickReport_Input_t));
    echoes--;
    return;
  }

  // States and moves management
  switch (state)
  {
    case SYNC_CONTROLLER:
			loop_start_step = find_loop_start_step();
			state = PROCESS;
      bufindex = 0;
      break;

    case PROCESS:
      switch (step[bufindex].button)
      {
        case UP:
          ReportData->LY = STICK_MIN;
          break;

        case LEFT:
          ReportData->LX = STICK_MIN;
          break;

        case DOWN:
          ReportData->LY = STICK_MAX;
          break;

        case RIGHT:
          ReportData->LX = STICK_MAX;
          break;

        case UPLEFT:
          ReportData->LY = STICK_MIN;
          ReportData->LX = STICK_MIN;
          break;

        case UPRIGHT:
          ReportData->LY = STICK_MIN;
          ReportData->LX = STICK_MAX;
          break;

        case DOWNLEFT:
          ReportData->LY = STICK_MAX;
          ReportData->LX = STICK_MIN;
          break;

        case DOWNRIGHT:
          ReportData->LY = STICK_MAX;
          ReportData->LX = STICK_MAX;
          break;

        case HOLD_UP:
          hold_LY = STICK_MIN;
          break;

        case HOLD_LEFT:
          hold_LX = STICK_MIN;
          break;

        case HOLD_DOWN:
          hold_LY = STICK_MAX;
          break;

        case HOLD_RIGHT:
          hold_LX = STICK_MAX;
          break;

        case HOLD_CLEAR:
          hold_LX = STICK_CENTER;
          hold_LY = STICK_CENTER;
          break;

        case HOLD_CAM_L:
          hold_RX = STICK_MIN;
          break;

        case HOLD_CAM_R:
          hold_RX = STICK_MAX;
          break;

        case HOLD_CAM_C:
          hold_RX = STICK_CENTER;
          break;

        case A:
          ReportData->Button |= SWITCH_A;
          break;

        case B:
          ReportData->Button |= SWITCH_B;
          break;

        case X:
          ReportData->Button |= SWITCH_X;
          break;

        case Y:
          ReportData->Button |= SWITCH_Y;
          break;

        case R:
          ReportData->Button |= SWITCH_R;
          break;

        case PLUS:
          ReportData->Button |= SWITCH_START;
          break;

        case HOME:
          ReportData->Button |= SWITCH_HOME;
          break;

        case H_UP:
          ReportData->HAT = HAT_TOP;
          break;

        case H_DOWN:
          ReportData->HAT = HAT_BOTTOM;
          break;

        case H_LEFT:
          ReportData->HAT = HAT_LEFT;
          break;

        case H_RIGHT:
          ReportData->HAT = HAT_RIGHT;
          break;

        default:
          break;
      }

      duration_count++;

      if (duration_count > step[bufindex].duration)
      {
        bufindex++;
        duration_count = 0;
        if(bufindex == 60){
          day_count++;
          if(day_count != 31){
            loop_count++;
            if(loop_count == frame){
              complete_flag = true;
              bufindex = 0;
            }
            else if(loop_count % report_step == 0){
              bufindex = 4;
            }
          }
          else{
            day_count = 0;
          }
        }
      }

      if(complete_flag && bufindex == 2){
        bufindex = 0;
      }
      if(bufindex == 3){ // ループ開始時のみ
        bufindex = 16;
      }

      if (bufindex > (int)( sizeof(step) / sizeof(step[0])) - 1)
      {
        bufindex = loop_start_step;
        duration_count = 0;
      }
      break;
    case CLEANUP:
			state = DONE;
			break;

		case DONE:
			return;
    }

  // Prepare to echo this report
  memcpy(&last_report, ReportData, sizeof(USB_JoystickReport_Input_t));
  echoes = ECHOES;
}
//d93c03549851f1b5
