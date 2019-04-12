import React from 'react';

import SearchBar from './components/SearchBar.js'
import GraphView from './components/GraphView.js'
import ImageView, {ImageDescription} from './components/ImageView.js'
import ListItem, {MondoList, GeneList, BioModelList} from './components/ListItem.js'

import {elements, xml} from './components/demo.js'

import './App.css';

import 'font-awesome/css/font-awesome.min.css';

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
      fetch(SERVICE_URL.concat('/api/gene-to-pathway/').concat(geneItem).concat('?size=5'))
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

		fetch('http://127.0.0.1:5000/api/pathway-to-sbgn/' + index)
		  .then(response => {
		    return response.text().then((text)=>{
		      console.log(text);
		      this.setState({sbgn: text});
		    });
		  });
	}

	render() {
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
