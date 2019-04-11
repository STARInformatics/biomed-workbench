import React, { Component } from 'react';

import GraphView from './components/GraphView.js'
import SearchBar from './components/SearchBar.js'
import ImageView from './components/ImageView.js'
import ListItem, {MondoList, GeneList, BioModelList} from './components/ListItem.js'
import sbgnStylesheet from 'cytoscape-sbgn-stylesheet'
import cytoscape from 'cytoscape';

import ReactDOM from 'react-dom';
import CytoscapeComponent from 'react-cytoscapejs';

import {elements, xml} from './components/demo.js'

import './App.css';

import 'font-awesome/css/font-awesome.min.css';

let convert = require('sbgnml-to-cytoscape');
let cyGraph = convert(xml);

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			imgSrc : null,
			searchText : '',
			mondoList: [
				{id: 1, name: 'No Search'}
			],
			geneList: [
				{gene_id: 1, gene_symbol: 'No Search'}
			],

			biomodelList: [
				{pathway_id: 1, name: 'No Search'}
			],
			mondoisClickEnabled: false,
			geneisClickEnabled: false,
			bioisClickEnabled: false,
			mondoSelected: '',
		}

		this.handleMondoSearch = this.handleMondoSearch.bind(this);
		this.handleTextChange = this.handleTextChange.bind(this);
		this.handleMondoClick = this.handleMondoClick.bind(this);
		this.handleGeneClick = this.handleGeneClick.bind(this);
		this.handlePathwayClick = this.handlePathwayClick.bind(this);
	}

	handleMondoSearch(e) {
		fetch('http://127.0.0.1:5000/api/disease/'.concat(this.state.searchText))
			.then(response => response.json())
			.then(data => {
                if (data.length ===0 || data === undefined) {
                    const newData = [
                        {id: 1, name: 'No Result'}
                    ]
                    this.setState({ mondoList: newData, mondoisClickEnabled: false });
                }
                else {
                    this.setState({ mondoList: data, mondoisClickEnabled: true });
                }
            });
	}

	handleTextChange(e) {
		this.setState({searchText : e.target.value});
	}

	handleMondoClick(mondoItem) {
		fetch('http://127.0.0.1:5000/api/disease-to-gene/'.concat(mondoItem))
			.then(response => response.json())
			.then(data => {
                if (data.length ===0 || data === undefined) {
                    const newData = [
                        {gene_id: 1, gene_symbol: 'No Result'}
                    ]
                    this.setState({ geneListlList: newData, geneisClickEnabled: false });
                }
                else {
                    this.setState({ geneList: data, geneisClickEnabled: true });
                }
            });
	}

  handleGeneClick(geneItem) {
      fetch('http://127.0.0.1:5000/api/gene-to-pathway/'.concat(geneItem).concat('?size=5'))
		.then(response => response.json())
		.then(data => {
            if (data.length ===0 || data === undefined) {
                const newData = [
                    {pathway_id: 1, name: 'No Result'}
                ]
                this.setState({ biomodelList: newData, bioisClickEnabled: false });
            }
            else {
                this.setState({ biomodelList: data, bioisClickEnabled: true });
            }
        });
  }

	handlePathwayClick(index) {
		console.log(index)
		this.setState({imgSrc : "http://localhost:5000/api/pathway-to-png/" + index})
	}

	render() {
		return (
			<div className="container">
        <SearchBar handleSearch={this.handleMondoSearch} handleTextChange={this.handleTextChange}/>
        <div className="col-sm-3">
          <MondoList
              mondoList={this.state.mondoList}
              isClickEnabled={this.state.mondoisClickEnabled}
              onClick={this.handleMondoClick}/>
          <GeneList
              geneList={this.state.geneList}
              isClickEnabled={this.state.geneisClickEnabled}
              onClick={this.handleGeneClick}/>
          <BioModelList
              biomodelList={this.state.biomodelList}
              isClickEnabled={this.state.bioisClickEnabled}
              onClick={this.handlePathwayClick}
          />
        </div>
        <ImageView src={this.state.imgSrc} />
				<CytoscapeComponent
					elements={elements}
					cy={cy => this.cy = cy}
					// stylesheet={sbgnStylesheet(cytoscape)}
					style={ { width: '600px', height: '600px' } }
				/>
	    </div>
		);
  }
}

const obj = sbgnStylesheet(cytoscape)

for(var propt in obj){
    console.log(propt + ': ' + obj[propt].selector);
}

console.log(sbgnStylesheet(cytoscape));
console.log([
    {
      selector: 'node',
      style: {
        width: 20,
        height: 20,
        shape: 'rectangle'
      }
    },
    {
      selector: 'edge',
      style: {
        width: 15
      }
    }
  ]);

export default App;
