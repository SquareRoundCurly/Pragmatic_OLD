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

graph = pragmatic.create_digraph_with_attributes()
pragmatic.digraph_to_custom_json_format(graph)
pragmatic.generate_html_with_d3js('graph.json', 'index.html')