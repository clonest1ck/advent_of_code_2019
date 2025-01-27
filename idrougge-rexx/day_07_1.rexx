/* Advent of code 2019, day 7, part 1 in ANSI REXX */
parse arg file
if file = '' then file = 'day7.txt'

/* Read input */
code = linein(file)
do codesize = 0 by 1 while code > ''
	parse var code rom.codesize ',' code
end

top = 0

do i = 00000 to 44444
	if verify(i, '01234') > 0 then iterate
	phases = right(i, 5, 0) /* Pad to 5 digits */
	if dup(phases) then iterate /* Skip if any phase occurs more than once */
	push 0 /* Push the initial input to queue */
	do n = 1 to 5
		phase = substr(phases, n, 1)
		push phase
		call copymem
		call calculate
	end
	pull answer
	top = max(top, answer)
end

say top
exit

dup: procedure
arg phases
do while phases > ''
	parse var phases # +1 phases
	if verify(#, phases) = 0 then return 1
end
return 0

/* Read opcode */
calculate:
pc = 0
do forever
	op = ram.pc

	parse value right(op, 5, 0) with mode.3 +1 mode.2 +1 mode.1 +1 op

	select
		when op = 1 then call add
		when op = 2 then call mul
		when op = 3 then call store
		when op = 4 then call load
		when op = 5 then call jnz
		when op = 6 then call jz
		when op = 7 then call clt
		when op = 8 then call cmp
		when op = 99 then return ram.0
		otherwise signal illegal
	end
end
return

add:
mode.3 = 1
parse value fetch(3) with src1 src2 dest .
ram.dest = src1 + src2
return

mul:
mode.3 = 1
parse value fetch(3) with src1 src2 dest .
ram.dest = src1 * src2
return

store:
mode.1 = 1
parse value fetch(1) with dest .
pull val
ram.dest = val
return

load:
parse value fetch(1) with src1 .
push src1
return

jnz:
parse value fetch(2) with val dest .
if val \= 0 then pc = dest
return

jz:
parse value fetch(2) with val dest .
if val = 0 then pc = dest
return

clt:
mode.3 = 1
parse value fetch(3) with src1 src2 dest .
ram.dest = src1 < src2
return

cmp:
mode.3 = 1
parse value fetch(3) with src1 src2 dest .
ram.dest = (src1 = src2)
return

fetch: procedure expose ram. mode. pc
out = ''
do # = 1 to arg(1)
	@ = pc + #
	if mode.# then do
		out = out ram.@		
	end
	else do
		ref = ram.@
		out = out ram.ref
	end
end
pc = pc + #
return out

copymem:
drop ram.
do p = 0 to codesize
	ram.p = rom.p
end
return

illegal:
say 'Illegal opcode:' op '@' pc
exit op