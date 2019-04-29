import React from 'react';
import cytoscape from 'cytoscape';
import sbgnStylesheet from 'cytoscape-sbgn-stylesheet';
import convert from 'sbgnml-to-cytoscape';

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

    	// Generate zIndex value for each node, larger nodes get smaller values
    	// Nodes are set to be drawn in order of lowest to highest z-index value
    	for (var key in elements.nodes) {
    		var tempH = elements.nodes[key].data.bbox.h;
    		var tempW = elements.nodes[key].data.bbox.w;  
    		var product = 10000/(tempW*tempH)

    		elements.nodes[key].data.zIndex = Math.floor(product);
    	}

    	// Create Cytoscape instance
		this.cy = cytoscape({
    		container: document.getElementById('cy'),
    		boxSelectionEnabled: true,
    		elements: elements,
    		// autounselectify: true,
			style: sbgnStylesheet(cytoscape).selector('node').css({
				'width': 'data(width)',
    			'height': 'data(height)',
    			'background-opacity': 0,
    			'overlay-opacity': 0,
    			'z-index-compare': 'manual',
    			'z-index': 'data(zIndex)',
    			'font-size': 10,
    		}).selector('edge').css({
    			'curve-style': 'taxi',
    		}), 
    		layout: {
    			name: 'preset',
    		}
    	})
    	this.cy.on('mouseover', 'node', function(evt) {
    		var node = evt.target;
    		console.log( 'mouse on node' + node.data('label') );
    	})

    	// for (var i; i < elements.nodes.length; i++) {
    	// 	console.log(elements.nodes[i]);
    	// }
    	console.log(elements);
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

    	// Generate zIndex value for each node, larger nodes get smaller values
    	// Nodes are set to be drawn in order of lowest to highest z-index value
    	for (var key in elements.nodes) {
    		var tempH = elements.nodes[key].data.bbox.h;
    		var tempW = elements.nodes[key].data.bbox.w;  
    		var product = 10000/(tempW*tempH)

    		elements.nodes[key].data.zIndex = Math.floor(product);
    	}
    	
    	this.cy = cytoscape({
    		container: document.getElementById('cy'),
    		boxSelectionEnabled: true,
    		elements: elements,
    		// autounselectify: true,
			style: sbgnStylesheet(cytoscape).selector('node').css({
				'width': 'data(width)',
    			'height': 'data(height)',
    			'background-opacity': 0,
    			'overlay-opacity': 0,
    			'z-index-compare': 'manual',
    			'z-index': 'data(zIndex)',
    			'font-size': 10,
    		}).selector('edge').css({
    			'curve-style': 'taxi',
    		}), 
    		layout: {
    			name: 'preset',
    		}
    	})
    	this.cy.on('mouseover', 'node', function(evt) {
    		var node = evt.target;
    		console.log( 'mouse on node' + node.data('label') );
    	})
    	console.log(elements);
    }

    componentDidMount(){
        this.renderSBGNVizElement();
    }

    render(){
    	let cyStyle = {
    		height: '500px',
		    width: '650px',
		    margin: '20px 0px',
        	outline: "solid #F5F5F5"
        };

        return(
			<div>
				<h6>Biomodel View</h6>
				<div style={cyStyle} id="cy"/>
			</div>
        	
        	)
    }
}

export default SBGNView;

