import React from 'react';
import cytoscape from 'cytoscape';
import sbgnStylesheet from 'cytoscape-sbgn-stylesheet'
import convert from 'sbgnml-to-cytoscape'

class GraphView extends React.Component{
    // https://stackoverflow.com/q/38626167
    constructor(props){
        super(props);
        this.renderCytoscapeElement = this.renderCytoscapeElement.bind(this);
    }

    componentDidUpdate(prevProps, prevState) {
      var elements = convert(this.props.sbgn)
      this.cy.json({
        elements : elements,
        layout: {
            name: 'breadthfirst',
            directed: true,
            padding: 10
        }
      })
    }

    renderCytoscapeElement(){
      var elements = convert(this.props.sbgn)
      this.cy = cytoscape({
          container: document.getElementById('cy'),
          boxSelectionEnabled: false,
          autounselectify: true,
					style: sbgnStylesheet(cytoscape),
          elements: elements,
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
