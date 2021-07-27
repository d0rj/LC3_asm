.ORIG 0x0200

; Programm:
ld r6, UserProgrammAddr
jmp r6

; Data:
UserProgrammAddr: .FILL	0x3000

.END