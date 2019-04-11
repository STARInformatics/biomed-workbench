import React, { Component } from 'react';
import './App.css';
import 'font-awesome/css/font-awesome.min.css';

class ImageView extends React.Component {
	render() {
		return (
			<div>
			<img src={this.props.src}/>
			</div>
		)
	}
}

class ListItem extends React.Component {
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}

	handleClick() {
		this.props.onClick(this.props.index);
	}


	render() {
		if (this.props.isClickEnabled === true) {
		return <a href="#"
					className="list-group-item list-group-item-action"
					onClick={this.handleClick}>
						{this.props.value}
				</a>;
		}
		else {
			return <a href="#" className="list-group-item list-group-item-action disabled">
					{this.props.value}
				</a>;
		}
	}
}

function MondoList(props) {
	const mondoList = props.mondoList;
	const isClickEnabled = props.isClickEnabled;
	const listItems = mondoList.map((item) =>
		<ListItem
			key={item.id}
			index={item.id}
			value={item.name}
			isClickEnabled={isClickEnabled}
			onClick={props.onClick}/>
	);
	return (
		<div className="container">
			<h6> Disease Index </h6>
			{listItems}
		</div>
	);
}

function GeneList(props) {
	const geneList = props.geneList;
	const isClickEnabled = props.isClickEnabled;
	const listItems = geneList.map((item) =>
		<ListItem
            key={item.gene_symbol}
            index={item.gene_id}
			value={item.gene_symbol}
            onClick={props.onClick}
            isClickEnabled={isClickEnabled}/>
	);
	return (
		<div className="container">
			<h6> Gene List </h6>
			{listItems}
		</div>
	);
}
function BioModelList(props) {
	const biomodelList = props.biomodelList;
	const isClickEnabled = props.isClickEnabled;
	const listItems = biomodelList.map((item) =>
		<ListItem key={item.name}
			index={item.pathway_id}
			value={item.name}
			onClick={props.onClick}
			isClickEnabled={isClickEnabled}
		/>
	);
	return (
		<div className="container">
			<h6> Biomodel List </h6>
			{listItems}
		</div>
	);
}

class SearchBar extends React.Component {
  render() {
    return (
		<form className="form-inline">
			<input
				type="search"
				className="form-control mr-sm-2"
				onChange={this.props.handleTextChange}
				placeholder="Search.."
				aria-label="Search"
				id="search"
			/>
			<button
				type="button"
				onClick={this.props.handleSearch}
				className="btn btn-outline-success my-2 my-sm-0">
				Search
			</button>
		</form>
    );
  }
}

const BASE_URL = process.env.REACT_APP_BASE_URL || 'http://localhost:5000';
const API_PATH = process.env.REACT_APP_API_PATH || '';
const SERVICE_URL  = BASE_URL + API_PATH;

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
		fetch(SERVICE_URL.concat('/api/disease/').concat(this.state.searchText).concat('?size=5'))
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
		fetch(SERVICE_URL.concat('/api/disease-to-gene/').concat(mondoItem).concat('?size=5'))
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
		this.setState({imgSrc : process.env.PUBLIC_URL+"/api/pathway-to-png/" + index})
	}

	render() {
		return (
			<div className="container">
			<ImageView src={this.state.imgSrc} />
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
		  </div>
		);
  }
}

export default App;
