; Tutorial.asm
;
; Created: 10/7/2019 8:53:56 PM
; Description: Tutorial teaches how to use assembly
; to make the LEDs on the board flash.
; Application code:

LDI R16,0xFF ;R16 = 0xFF
LDI R17, 0
OUT DDRD, R16 ; PD set to output
SBI DDRE, 5 ; PE5 set to output
CBI DDRE, 6 ; PE6 set to input
SBI PORTE, 6 ; enable pullup on PE6
OUT DDRA, R17 ; PA set to input mode
OUT PORTA, R16 ; enable pullup on PA
MAIN: 
	

	S1:	
		SBIC PINA, 0 ; button is pushed / connected to ground
		RJMP S2
		CBI PORTD, 0 ; turns on LED1
		RJMP MAIN

	S1_OFF:
		SBI PORTD, 0 ; turns LED back off
	
	S2:
		SBIC PINA, 1 ; button is pushed / connected to ground
		RJMP S3
		CBI PORTD, 1 ; turns on LED1
		RJMP MAIN

	S2_OFF:
		SBI PORTD, 1 ; turns LED back off

	S3:
		SBIC PINA, 2 ; button is pushed / connected to ground
		RJMP S4
		CBI PORTD, 2 ; turns on LED1
		RJMP MAIN

	S3_OFF:
		SBI PORTD, 2 ; turns LED back off

	S4:
		SBIC PINA, 3 ; button is pushed / connected to ground
		RJMP S5
		CBI PORTD, 3 ; turns on LED1
		RJMP MAIN

	S4_OFF:
		SBI PORTD, 3 ; turns LED back off

	S5:
		SBIC PINE, 6 ; button is pushed / connected to ground
		RJMP S6
		CBI PORTE, 5 ; turns on LED1
		RJMP MAIN

	S5_OFF:
		SBI PORTE, 5 ; turns LED back off
	S6:
		SBIC PINA, 4 ; button is pushed / connected to ground
		RJMP S7
		CBI PORTD, 4 ; turns on LED1
		RJMP MAIN

	S6_OFF:
		SBI PORTD, 4 ; turns LED back off


	S7:
		SBIC PINA, 5 ; button is pushed / connected to ground
		RJMP S8
		CBI PORTD, 5 ; turns on LED1
		RJMP MAIN

	S7_OFF:
		SBI PORTD, 5 ; turns LED back off


	S8:
		SBIC PINA, 6 ; button is pushed / connected to ground
		RJMP S9
		CBI PORTD, 6 ; turns on LED1
		RJMP MAIN

	S8_OFF:
		SBI PORTD, 6 ; turns LED back off

	S9:
		SBIC PINA, 7 ; button is pushed / connected to ground
		RJMP S9_OFF
		CBI PORTD, 7 ; turns on LED1
		RJMP MAIN

	S9_OFF:
		SBI PORTD, 7 ; turns LED back off

	OUT PORTD, R17
	CBI PORTE, 5
	CALL Delay ; call a delay after the LEDs are turned on
	OUT PORTD, R16 ; turn off all LEDS
	SBI PORTE, 5
	CALL Delay ; call a delay after the LEDs are turned on
	RJMP MAIN


Delay: ; delay used in order to make LEDs flash
	LDI R22, 25
LOOP1:
	LDI R21, 255
LOOP2:
	LDI R19, 255
LOOP3:	
	DEC R19
	BRNE LOOP3
	DEC R21
	BRNE LOOP2
	DEC R22
	BRNE LOOP1
	RET