import React from 'react';
import sbgnviz from 'sbgnviz'
import cytoscape from 'cytoscape';
import cysbgn from 'cytoscape-for-sbgn';
import sbgnStylesheet from 'cytoscape-sbgn-stylesheet';
import convert from 'sbgnml-to-cytoscape';
// import coseBilkent from 'cytoscape-cose-bilkent';
// import cola from 'cytoscape-cola';
// import filesaverjs from 'filesaverjs';
// import fcose from 'cytoscape-fcose';

// cytoscape.use( coseBilkent );
// cytoscape.use( cola );
// cytoscape.use( fcose);

class SBGNView extends React.Component{

	constructor(props){
        super(props);
        this.renderSBGNVizElement = this.renderSBGNVizElement.bind(this);
    }

    componentDidUpdate(prevProps, prevState) {
    	// Convert SBGN XML to JSON
    	var elements = convert(this.props.sbgn)
    	
    	// Extract x and y position values and add as a new position element for each Node object
    	for (var key in elements.nodes) {
    		var tempX = elements.nodes[key].data.bbox.x;
    		var tempY = elements.nodes[key].data.bbox.y;
    		var tempH = elements.nodes[key].data.bbox.h;
    		var tempW = elements.nodes[key].data.bbox.w;    		

    		var positionStr = '{"x": ' + tempX + ', "y": '+tempY+'}';
    		var positionObj = JSON.parse(positionStr);

    		elements.nodes[key].position = positionObj;
    		elements.nodes[key].data.height = tempH;
    		elements.nodes[key].data.width = tempW;
    	}

    	// for (var key in elements.nodes) {
    	// 	if (elements.nodes[key].class === "complex") elements.nodes[key].shape = "hexagon";
    	// 	if (elements.nodes[key].class === "compartment" || elements.nodes[key].class === "macromolecule") elements.nodes[key].shape = "round rectangle";
    	// 	if (elements.nodes[key].class === "subcompartment") elements.nodes[key].shape = "rectangle";
    	// 	if (elements.nodes[key].class === "simple chemical") 
    	// 		elements.nodes[key].shape = "ellipse";
    		
    	// }

    	// for (var key in elements.edges) {

    	// }

    	// Create Cytoscape instance
    	this.cy = cytoscape({
    		container: document.getElementById('cy'),
    		boxSelectionEnabled: true,
    		elements: elements,
    		style: sbgnStylesheet(cytoscape),

    		// style: cytoscape.stylesheet()
    		// 	.selector('node')
    		// 		.css({
    		// 			'width': 'data(width)',
    		// 			'height': 'data(height)',
    		// 			// 'shape': 'data(shape)'
    		// 		}),
    		
    		layout: {
    			name: 'preset',
    		}
    	})

    	// for (var i; i < elements.nodes.length; i++) {
    	// 	console.log(elements.nodes[i]);
    	// }
    	console.log(elements);
    	console.log(sbgnStylesheet(cytoscape));
    }

    renderSBGNVizElement(){
    	// Convert SBGN XML to JSON
		var elements = convert(this.props.sbgn)

    	// Extract x and y position values and add as a new position element for each Node object
    	for (var key in elements.nodes) {
    		var tempX = elements.nodes[key].data.bbox.x;
    		var tempY = elements.nodes[key].data.bbox.y;
			var tempH = elements.nodes[key].data.bbox.h;
    		var tempW = elements.nodes[key].data.bbox.w;   
    		
    		var positionStr = '{"x": ' + tempX + ', "y": '+tempY+'}';
    		var positionObj = JSON.parse(positionStr);

    		elements.nodes[key].position = positionObj;
    		elements.nodes[key].data.height = tempH;
    		elements.nodes[key].data.width = tempW;
    	}
    	
    	this.cy = cytoscape({
    		container: document.getElementById('cy'),
    		boxSelectionEnabled: true,
    		// autounselectify: true,
    		style: sbgnStylesheet(cytoscape),
    		elements: elements,
    		layout: {
    			name: 'preset',
    		}
    	})
    }

    componentDidMount(){
        this.renderSBGNVizElement();
    }

    render(){
    	let cyStyle = {
    		height: '500px',
		    width: '800px',
		    margin: '20px 0px',
        	outline: "solid #F5F5F5"
        };

        return(
        	<div style={cyStyle} id="cy"/>
        	)
    }
}

export default SBGNView;

