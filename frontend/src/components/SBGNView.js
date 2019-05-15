import React from 'react';
import {Button, Dropdown, DropdownToggle, DropdownMenu, DropdownItem} from 'reactstrap';
import cytoscape from 'cytoscape';
import sbgnStylesheet from 'cytoscape-sbgn-stylesheet';
import convert from 'sbgnml-to-cytoscape';

import anywherePanning from 'cytoscape-anywhere-panning';

import coseBilkent from 'cytoscape-cose-bilkent';
import cola from 'cytoscape-cola';
import dagre from 'cytoscape-dagre';

const layoutOptionsDict = {
  'Cola 5' : {
    name: 'cola',
    maxSimulationTime: 100,
    flow: 'DAG',
    nodeSpacing: function(node){
      return 5 * (node._private.edges.length + 1);
    },
  },
  'Cola 10' : {
    name: 'cola',
    maxSimulationTime: 100,
    flow: 'DAG',
    nodeSpacing: function(node){
      return 10 * (node._private.edges.length + 1);
    },
  },
  'Cola 20' : {
    name: 'cola',
    maxSimulationTime: 100,
    flow: 'DAG',
    nodeSpacing: function(node){
      return 20 * (node._private.edges.length + 1);
    },
  },
  'Preset' : {
    name : 'preset'
  },
  'Dagre' : {
    name : 'dagre',
    edgeSep : 10,
  },
  'Cose-Bilkent' : {
    name: 'cose-bilkent',
    randomize: false,
  },
  'Cose-Bilkent Randomized' : {
    name: 'cose-bilkent',
    randomize: true,
  },
};

class SBGNView extends React.Component {

  constructor(props) {
    super(props);
    this.renderSBGNVizElement = this.renderSBGNVizElement.bind(this);
    this.toggleDropdown = this.toggleDropdown.bind(this);
    this.chooseLayout = this.chooseLayout.bind(this);
    this.state = {
      isDropdownOpen : false,
      layout : Object.keys(layoutOptionsDict)[0],
      isPanning : true,
    }

    cytoscape.use(anywherePanning);

		cytoscape.use(coseBilkent);
    cytoscape.use(cola);
    cytoscape.use(dagre);
  }

  toggleDropdown() {
    this.setState(prevState => ({
      isDropdownOpen : !prevState.isDropdownOpen,
    }));
  }

  chooseLayout(layoutName) {
    if (layoutName != this.state.layout) {
      this.setState({layout : layoutName});
    }
  }

  componentDidUpdate(prevProps, prevState) {
    var redraw =
      (prevProps.sbgn === this.props.sbgn) &&
      (prevState.layout === this.state.layout) &&
      (prevState.isPanning) === (this.state.isPanning);

    if (!redraw) {
      this.renderSBGNVizElement();
    }
  }

  renderSBGNVizElement() {
    // Convert SBGN XML to JSON
    var elements = convert(this.props.sbgn)

    // Extract x and y position values and add as a new position element for each Node object
    for (var key in elements.nodes) {
      var X = elements.nodes[key].data.bbox.x;
      var Y = elements.nodes[key].data.bbox.y;
      var H = elements.nodes[key].data.bbox.h;
      var W = elements.nodes[key].data.bbox.w;

      var positionStr = '{"x": ' + X + ', "y": ' + Y + '}';
      var positionObj = JSON.parse(positionStr);

      elements.nodes[key].position = positionObj;
      elements.nodes[key].data.height = H;
      elements.nodes[key].data.width = W;
    }

    // Generate zIndex value for each node, larger nodes get smaller values
    // Nodes are set to be drawn in order of lowest to highest z-index value
    for (var key in elements.nodes) {
      var tempH = elements.nodes[key].data.bbox.h;
      var tempW = elements.nodes[key].data.bbox.w;
      var product = 10000 / (tempW * tempH)

      elements.nodes[key].data.zIndex = Math.floor(product);
			elements.nodes[key].parent = 'compartmentVertex_5460_17'
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
      }).selector('edge:selected')
        .css({
          'width': 5,
          'line-color': 'orange',
      }).selector('node:selected')
        .css({
          'border-color' : 'orange',
      }),
      layout: layoutOptionsDict[this.state.layout],
    })

    this.cy.on('mouseover', 'node', function(evt) {
      var node = evt.target;
      console.log('mouse on node' + node.data('label'));
    })

    const isPanning = this.state.isPanning
    this.cy.autoungrabify(isPanning);
    this.cy.anywherePanning(function() {
      return isPanning;
    });

    console.log(elements);
  }

  componentDidMount() {
    this.renderSBGNVizElement();
  }

  render() {
    let cyStyle = {
      height: '500px',
      width: '650px',
      margin: '20px 0px',
      outline: "solid #F5F5F5",
      align : 'top',
    };

    let layoutDropdownItems = Object.keys(layoutOptionsDict).map((layoutName) => (
      <DropdownItem
        onClick={() => this.chooseLayout(layoutName)}>
          {layoutName}
      </DropdownItem>
    ));

    return (
      <div>
        <div style={{'display':'flex'}}>
          <Dropdown isOpen={this.state.isDropdownOpen} toggle={this.toggleDropdown}>
            <DropdownToggle caret>{'Layout: ' + this.state.layout}</DropdownToggle>
            <DropdownMenu>
              {layoutDropdownItems}
            </DropdownMenu>
          </Dropdown>
          <Button
            onClick={() => this.setState({isPanning : !this.state.isPanning})}>
            {'Panning: ' + this.state.isPanning}
          </Button>
        </div>
        <div style={cyStyle} id="cy"/>
      </div>
    );
  }
}

export default SBGNView;
