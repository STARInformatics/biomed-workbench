import React from 'react';
import SearchBar from './components/SearchBar.js'
import SBGNView from './components/SBGNView.js'
import ImageDescription from './components/ImageView.js'
import {MondoList, GeneList, BioModelList,MyLoader} from './components/ListItem.js'

import update from 'react-addons-update';
import './App.css';

import 'font-awesome/css/font-awesome.min.css';

const BASE_URL =  process.env.REACT_APP_BASE_URL || 'http://localhost:5000';
const API_PATH =  process.env.REACT_APP_API_PATH || '';
const SERVICE_URL  = BASE_URL + API_PATH;

const divStyle = {
    marginTop: "30px"
}

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			sbgn: '',
			imgSrc : null,
			searchText : '',
			mondoList: [
				{id: '1', name: 'No Search'}
			],
			list: [
				{id: 'MONDO:0010863', text: 'No Search',
					items: [
						{id: 'MONDO:0012919',text: 'tiny 3'},
						{id: 'MONDO:0012921',text: 'tiny 2'}
					]},
				{id: 'MONDO:0011168',text: 'No Search2'}

			],
			geneList: [
				{id:1, name:'mod0 - Gene Lookup', isLoading:false, items:[]},
				{id:2, name:'mod1e - Gene Interactions', isLoading:false, items:[]},
        {id:3, name:'mod1b1 - Phenotype Similarity',isLoading:false, items:[]},
			],

			biomodelList: [
				{pathway_id: 1, name: 'No Search'}
			],
			mondoisClickEnabled: false,
			geneisClickEnabled: false,
			bioisClickEnabled: false,

			mondoisLoading:false,
			bioisLoading:false,
			descriptionIsLoading:false,

			mondoSelected: '',
      description: {}
		};

		this.handleMondoSearch = this.handleMondoSearch.bind(this);
		this.handleTextChange = this.handleTextChange.bind(this);
		this.handleMondoClick = this.handleMondoClick.bind(this);
		this.handleGeneClick = this.handleGeneClick.bind(this);
		this.handleBiomodelClick = this.handleBiomodelClick.bind(this);
	}

	handleMondoSearch = () => {
		this.setState({mondoisLoading:true});
			fetch(SERVICE_URL.concat('/api/disease/').concat(this.state.searchText))
				.then(response => response.json())
				.then(data => {
					if (data === undefined || data.length === 0) {
						const newData = [
							{id: 1, name: 'No Result'}
						];
						this.setState({mondoList: newData, mondoisClickEnabled: false});
					} else {
						this.setState({mondoList: data, mondoisClickEnabled: true, mondoisLoading:false});
					}
			})
			.catch(error => {
				const data = [
					{id: 1, name: 'No Result'}
				];
				this.setState({mondoList: data, mondoisClickEnabled: false});
				});

	};


	handleTextChange(e) {
		this.setState({searchText : e.target.value});
	}

	handleMondoClick(mondoItem) {
		this.setState({geneisClickEnabled: true,
			descriptionIsLoading:true,
			geneList: update(this.state.geneList, { 0: {isLoading: {$set: true}},
																							1: {isLoading: {$set: true}},
																							2: {isLoading: {$set: true}}})
			});

		//Load mod0
		fetch(SERVICE_URL.concat('/api/workflow/mod0/').concat(mondoItem))
      .then(response => response.json())
      .then(data => {
        console.log("FINISH: mod0");
        if (data === undefined || data.length === 0) {
          data = [{hit_id: 1, hit_symbol: 'No Result'}];
        }
        this.setState({
					geneList: update(this.state.geneList, {0 : {items: {$set: data},
																											isLoading:{$set: false}}}),

				})})
			.catch(error=> {
				const data = [{hit_id: 1, hit_symbol: 'No Result'}];
				this.setState({
					geneList: update(this.state.geneList, {0 : {items: {$set: data},
																											isLoading:{$set: false}}}),
			})});


		//Load mod1e
    fetch(SERVICE_URL.concat('/api/workflow/mod1e/').concat(mondoItem))
      .then(response => response.json())
      .then(data => {
        console.log("FINISH: mod1e");
        if (data === undefined || data.length === 0) {
          data = [{hit_id: 1, hit_symbol: 'No Result'}];
        }
        this.setState({
					geneList: update(this.state.geneList, {1 : {items: {$set: data},
																											isLoading:{$set:false}}}),
        })
		})
		.catch(error=> {
			const data = [{hit_id: 1, hit_symbol: 'No Result'}];
			this.setState({
				geneList: update(this.state.geneList, {1 : {items: {$set: data},
																										isLoading:{$set:false}}}),
		})});

		//Load mod1b1
    fetch(SERVICE_URL.concat('/api/workflow/mod1b1/').concat(mondoItem))
      .then(response => response.json())
      .then(data => {
        console.log("FINISH: mod1b1");
        if (data === undefined || data.length === 0) {
          data = [{hit_id: 1, hit_symbol: 'No Result'}];
        }
        this.setState({
					geneList: update(this.state.geneList, {2 : {items: {$set: data},
																											isLoading:{$set:false}}}),
        })
    }).catch(error=> {
			const data = [{hit_id: 1, hit_symbol: 'No Result'}];
			this.setState({
				geneList: update(this.state.geneList, {2 : {items: {$set: data},
																										isLoading:{$set:false}}}),
		})});

		fetch(SERVICE_URL.concat('/api/get-ncats-data/').concat(mondoItem))
				.then(response => response.json())
				.then(data => {
					if (data !== undefined || data.length !== 0) {
							this.setState({description:data});
					}
					this.setState({descriptionIsLoading:false})
				})
				.catch(error => {
					this.setState({description:{concept:{category:'Not Found'}}});
			});

	}

  	handleGeneClick(geneItem) {
			this.setState({bioisLoading:true, descriptionIsLoading:true});

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
						this.setState({ biomodelList: data, bioisClickEnabled: true, bioisLoading:false });
					}
				});

			//Load gene description
			fetch(SERVICE_URL.concat('/api/get-ncats-data/').concat(geneItem))
			.then(response => response.json())
			.then(data => {
				if (data !== undefined || data.length !== 0) {
						this.setState({description:data});
				}
				this.setState({descriptionIsLoading:false})
			})
			.catch(error => {
				this.setState({description:{concept:{category:'Not Found'}}});
	});

  }

	handleBiomodelClick(index) {
		console.log(index);
		this.setState({imgSrc : SERVICE_URL.concat('/api/pathway-to-png/') + index});
		fetch(SERVICE_URL.concat('/api/pathway-to-sbgn/') + index)
		  .then(response => {
		    return response.text().then((text)=>{
		      // console.log(text);
		      this.setState({sbgn: text});
		    });
		  });
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



            <div style={divStyle}>
                <div className="container-fluid">
                    <SearchBar handleSearch={this.handleMondoSearch} handleTextChange={this.handleTextChange}/>

                    <div className="row">
                        <div className="col-sm-3">
													<MondoList
                            mondoList={this.state.mondoList}
														isClickEnabled={this.state.mondoisClickEnabled}
														isLoading={this.state.mondoisLoading}
                            onClick={this.handleMondoClick}/>
                          <GeneList
                            geneList={this.state.geneList}
														isClickEnabled={this.state.geneisClickEnabled}
														isLoading={this.state.geneisLoading}
                            onClick={this.handleGeneClick}/>
                          <BioModelList
                            biomodelList={this.state.biomodelList}
                						isClickEnabled={this.state.bioisClickEnabled}
                						isLoading={this.state.bioisLoading}
                            onClick={this.handleBiomodelClick}
                          />
                    		</div>

                    		<div className="col-sm-6">
                    			<SBGNView sbgn={this.state.sbgn}  />
                    		</div>

                    		<div className="col-sm-3">
													<MyLoader isLoading={this.state.descriptionIsLoading}>
                        		<ImageDescription text={this.state.description} />
													</MyLoader>
                    		</div>
                	</div>
                </div>

						</div>
        );
  }
}

export default App;
