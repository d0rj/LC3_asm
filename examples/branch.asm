.orig 0x3000

lea r0, Yes
ADD	r5,	r1,	r2
brz PrintYes

PrintNo: 
    lea r0, No
    PUTS

PrintYes: 
    lea r0, Yes
    PUTS

HALT

No: .STRINGZ	"N"
Yes: .STRINGZ	"Y"

.end
