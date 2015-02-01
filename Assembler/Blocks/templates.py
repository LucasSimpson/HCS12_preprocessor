
def delay_block ():
	return """
        ; Delay for {delay_human} ms
        LDX #{delay} 
{label} NOP
        NOP
        NOP
        NOP
        NOP
        DBNE X, {label}
        """

def long_delay_block ():
        return """
        ; Delay for {delay_human} ms
        LDX  #{outer_num} 
{label_1} NOP
        LDY  #{inner_num}
{label_2} NOP
        NOP
        NOP
        NOP
        NOP
        DBNE Y, {label_2}
        DBNE X, {label_1}
        LDX  #{offset}
{label_3} DBNE X, {label_4}
        NOP
        NOP
        NOP
        NOP
        JMP  {label_3}
{label_4} NOP
        ; End of delay.
        """

def start_block ():
	return """
        ; export symbols
            XDEF Entry, _Startup            ; export 'Entry' symbol
            ABSENTRY Entry        ; for absolute assembly: mark this as application entry point

        ; Include derivative-specific definitions 
        INCLUDE 'derivative.inc' 
        
ROMStart    EQU  {rom_start}  ; absolute address to place my code/constant data

        ; code section
            ORG   ROMStart


Entry:
_Startup:

            LDAA #$01      ; set the LSb (b0), clear all others (b7-b1)
            STAA DDRJ      ; configure uC's Data Direction Register for Port J

        header (Code start)
        """

def header_block ():
	return """
    ;***************************************
    ;* {header}
    ;***************************************
    """

def loop_pre_block ():
	return """
        ; Loop {num_loops_human} times.
        LDAA #{num_loops}
        STAA {sp}
{label} DECA
        STAA {sp}
        """

def loop_post_block ():
	return """
        LDAA {sp}
        BGT  {label}
        ; Loop end.
        """

def long_loop_block ():
	return """
	loop ({outer_num}) {{
		loop ({inner_num}) {{
			{inside_raw}
		}}
	}}
	loop ({offset}) {{
		{inside_raw}
	}}
	"""

def LED_block ():
        return """
        LDAA {state}
        STAA PTJ   ; Turn {state_human} LED
        """

def interrupt_block ():
        return """
        header (Interrupt Vectors)
        ORG   $FFFE
        DC.W  Entry           ; Reset Vector
        """

def loop_inf_pre_block ():
	return """
{label} NOP ; Infinite loop start.
	"""

def loop_inf_post_block ():
	return """
	JMP  {label}
	"""
