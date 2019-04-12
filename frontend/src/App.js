import React from 'react';

import SearchBar from './components/SearchBar.js'
import GraphView from './components/GraphView.js'
import ImageView, {ImageDescription} from './components/ImageView.js'
import {MondoList, GeneList, BioModelList} from './components/ListItem.js'

import {xml} from './components/demo.js'

import './App.css';

import 'font-awesome/css/font-awesome.min.css';

//let convert = require('sbgnml-to-cytoscape');
//let cyGraph = convert(xml);

//const BASE_URL =  process.env.REACT_APP_BASE_URL || 'http://localhost:5000';
//const API_PATH =  process.env.REACT_APP_API_PATH || '';
const BASE_URL =  'https://bkw.starinformatics.com';
const API_PATH =  '/service';
const SERVICE_URL  = BASE_URL + API_PATH;

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			sbgn: xml,
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
            geneDescription: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc quis varius ex.'
		};

		this.handleMondoSearch = this.handleMondoSearch.bind(this);
		this.handleTextChange = this.handleTextChange.bind(this);
		this.handleMondoClick = this.handleMondoClick.bind(this);
		this.handleGeneClick = this.handleGeneClick.bind(this);
		this.handlePathwayClick = this.handlePathwayClick.bind(this);
	}

	handleMondoSearch = () => {
		return fetch(SERVICE_URL.concat('/api/disease/').concat(this.state.searchText))
			.then(response => response.json())
			.then(data => {
				if (data === undefined || data.length === 0) {
					const newData = [
						{id: 1, name: 'No Result'}
					];
					this.setState({mondoList: newData, mondoisClickEnabled: false});
				} else {
					this.setState({mondoList: data, mondoisClickEnabled: true});
				}
			});
	};

	handleTextChange(e) {
		this.setState({searchText : e.target.value});
	}

	handleMondoClick(mondoItem) {
		fetch(SERVICE_URL.concat('/api/disease-to-gene/').concat(mondoItem))
			.then(response => response.json())
			.then(data => {
                if (data === undefined || data.length === 0) {
                    const newData = [
                        {gene_id: 1, gene_symbol: 'No Result'}
                    ];
                    this.setState({ geneListlList: newData, geneisClickEnabled: false });
                }
                else {
                    this.setState({ geneList: data, geneisClickEnabled: true });
                }
            });
	}

  handleGeneClick(geneItem) {
      fetch(SERVICE_URL.concat('/api/gene-to-pathway/').concat(geneItem).concat('?size=5'))
		.then(response => response.json())
		.then(data => {
            if (data === undefined || data.length === 0) {
                const newData = [
                    {pathway_id: 1, name: 'No Result'}
                ];
                this.setState({ biomodelList: newData, bioisClickEnabled: false });
            }
            else {
                this.setState({ biomodelList: data, bioisClickEnabled: true });
            }
        });
  }

	handlePathwayClick(index) {
		console.log(index);
		this.setState({imgSrc : SERVICE_URL.concat('/api/pathway-to-png/') + index});
		fetch(SERVICE_URL.concat('/api/pathway-to-sbgn/') + index)
		  .then(response => {
		    return response.text().then((text)=>{
		      console.log(text);
		      this.setState({sbgn: text});
		    });
		  });
	}

	render() {

	    console.log("Workbench Environmental Variables:");
	    console.log("\tBASE_URL:\t"+BASE_URL);
	    console.log("\tAPI_PATH:\t"+API_PATH);
	    console.log("\tSERVICE_URL:\t"+SERVICE_URL);

		return (
			<div className="container-fluid">
                <SearchBar handleSearch={this.handleMondoSearch} handleTextChange={this.handleTextChange}/>
                <div className="row">
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
                    <div className="col-sm-6">
                        <ImageView src={this.state.imgSrc} />
                    </div>
                    <div className="col-sm-3">
                        <ImageDescription text={this.state.geneDescription} />
                    </div>
										<GraphView sbgn={this.state.sbgn} />

                </div>
            </div>
		);
  }
}

export default App;
