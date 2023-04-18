import networkx as nx
import json

def create_digraph_with_attributes():
	"""
	Creates a directed graph with node and edge attributes.

	Returns:
	nx.DiGraph: The directed graph with node and edge attributes.
	"""
	digraph = nx.DiGraph()

	# Add nodes with attributes
	digraph.add_node('A', color='red')
	digraph.add_node('B', color='blue')

	# Add edges with attributes
	digraph.add_edge('A', 'B', command='command1')

	return digraph

def digraph_to_custom_json_format(digraph, graph_type = '', graph_label = '', graph_metadata=None):
	"""
	Converts a NetworkX DiGraph to the custom JSON format.

	Parameters:
	digraph (nx.DiGraph): The directed graph to convert.
	graph_type (str): The type of the graph.
	graph_label (str): The label of the graph.
	graph_metadata (dict): The metadata for the graph.

	Returns:
	str: The custom JSON format representation of the graph.
	"""
	if graph_metadata is None:
		graph_metadata = {}

	# Format nodes
	nodes = {}
	for node, attrs in digraph.nodes(data=True):
		nodes[str(node)] = {
			"label": f"node label({node})",
			"metadata": attrs
		}

	# Format edges
	edges = []
	for source, target, attrs in digraph.edges(data=True):
		edges.append({
			"source": str(source),
			"relation": attrs.get('command', 'edge relationship'),
			"target": str(target),
			"directed": True,
			"label": f"edge label",
			"metadata": {k: v for k, v in attrs.items() if k != 'command'}
		})

	# Create the JSON structure
	json_data = {
		"graphs": [
			{
				"directed": True,
				"type": graph_type,
				"label": graph_label,
				"metadata": graph_metadata,
				"nodes": nodes,
				"edges": edges
			}
		]
	}

	json_str = json.dumps(json_data, indent=2)
	with open('graph.json', 'w') as file:
		file.write(json_str)

def generate_html_with_d3js(json_filename, output_filename):
	with open(json_filename, 'r') as json_file:
		json_content = json_file.read()


	html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>D3.js Node Graph</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: sans-serif;
        }}
        .node {{
            stroke: #fff;
            stroke-width: 1.5px;
        }}
        .link {{
            stroke: #999;
            stroke-opacity: 0.6;
        }}
    </style>
</head>
<body>
    <div>
        <button onclick="changeGraph(0)">Graph 1</button>
        <button onclick="changeGraph(1)">Graph 2</button>
    </div>
    <svg id="graph"></svg>
    <script>
        const width = 800;
        const height = 600;
        const svg = d3.select("#graph")
            .attr("width", width)
            .attr("height", height);

        let graphs = [];

		const data = {json_content};

		graphs = data.graphs;
		changeGraph(0);


        function changeGraph(index) {{
            if (graphs.length === 0) {{
                return;
            }}

            svg.selectAll("*").remove();

            const graph = graphs[index];
            const nodes = Object.values(graph.nodes);
            
	    	const nodesArray = Object.entries(graph.nodes).map(([id, node]) => ({{
			id: id,
			label: node.label,
			metadata: node.metadata,
			x: width / 2 + Math.random() * 100 - 50,  // Random position around the center (x-axis)
        	y: height / 2 + Math.random() * 100 - 50 // Random position around the center (y-axis)
		}}));
	    
			const links = graph.edges.map(edge => ({{
			...edge,
			source: edge.source,
			target: edge.target
		}}));

            const simulation = d3.forceSimulation(nodesArray)
        		.force("link", d3.forceLink(links).id(d => d.id))
                .force("charge", d3.forceManyBody())
        		.force("center", d3.forceCenter(width / 2, height / 2));
				// .force("x", d3.forceX(width / 2))
				// .force("y", d3.forceX(height / 2));

            const link = svg.append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(links)
                .join("line")
                .attr("class", "link")
                .attr("stroke-width", 2);

            const node = svg.append("g")
                .attr("class", "nodes")
                .selectAll("circle")
                .data(nodesArray)
                .join("circle")
                .attr("class", "node")
                .attr("r", 5)
                .attr("fill", "blue")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            node.append("title")
                .text(d => d.label);

            simulation.on("tick", () => {{
                link.attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node.attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            }});

            function dragstarted(event, d) {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }}

            function dragged(event, d) {{
                d.fx = event.x;
                d.fy = event.y;
            }}

            function dragended(event, d) {{
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }}
        }}
    </script>
</body>
</html>"""

	with open(output_filename, 'w') as file:
		file.write(html_template)