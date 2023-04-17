import pragmatic

config = {
	'debug': {
		'debug_symbols': '-g',
		'optimize': '-O0',
		'defines': '-DDEBUG'
	},
	'release': {
		'optimize': '-O2',
		'defines': '-DNDEBUG'
	}
}

pragmatic.add_command('compile', 'clang {debug_symbols} {optimize} {defines} {input} -o {output}', config)

pragmatic.add_rule('Main.cpp', 'Main.o', 'compile')

print(pragmatic.commands)
print(pragmatic.rules)