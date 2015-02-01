def delay_block ():
	return """
        ; {delay}ms delay start.
        loop ({delay}) {{
            LDX #999 ;
{label}     NOP
            NOP
            NOP
            NOP
            NOP
            DBNE X, {label}
        }}
        ; {delay}ms delay end.
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
        LDAA {num_loops}
        STAA {sp}
{label} NOP
        """

def loop_post_block ():
	return """
        LDAA {sp}
        DBNE A, {label}
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