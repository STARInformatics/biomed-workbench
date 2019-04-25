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
            name: 'cose',
            // padding: 30
        }
      })
    }

    renderCytoscapeElement(){
      var elements = convert(this.props.sbgn)
      this.cy = cytoscape({
          container: document.getElementById('cy'),
          boxSelectionEnabled: true,
          autounselectify: true,
					style: sbgnStylesheet(cytoscape),
          elements: elements,
          layout: {
              name: 'cose',
              // padding: 30
          }
      });
    }

    componentDidMount(){
        this.renderCytoscapeElement();
    }

    render(){
			let cyStyle = {
		    height: '1000px',
		    width: '500px',
		    margin: '20px 0px',
        outline: "solid #F5F5F5"
		  };


      return(
				<div>
		      <div style={cyStyle} id="cy"/>
		    </div>
      )
    }
}



export default GraphView;
