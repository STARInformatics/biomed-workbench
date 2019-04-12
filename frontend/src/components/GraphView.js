import React from 'react';
import cytoscape from 'cytoscape';
import sbgnStylesheet from 'cytoscape-sbgn-stylesheet'

class GraphView extends React.Component{
    // https://stackoverflow.com/q/38626167
    constructor(props){
        super(props);
        this.renderCytoscapeElement = this.renderCytoscapeElement.bind(this);
    }

    renderCytoscapeElement(){
        this.cy = cytoscape({
            container: document.getElementById('cy'),
            boxSelectionEnabled: false,
            autounselectify: true,
						style: sbgnStylesheet(cytoscape),
            elements: this.props.elements,
            layout: {
                name: 'breadthfirst',
                directed: true,
                padding: 10
            }
        });
    }

    componentDidMount(){
        this.renderCytoscapeElement();
    }

    render(){
			let cyStyle = {
		    height: '1000px',
		    width: '1000px',
		    margin: '20px 0px'
		  };

      return(
				<div>
		      <div style={cyStyle} id="cy"/>
		    </div>
      )
    }
}

export default GraphView;
