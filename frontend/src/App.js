import React, { Component } from 'react';
import './App.css';
import 'font-awesome/css/font-awesome.min.css';

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
			<h5> Disease Index </h5>
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
			<h5> Gene List </h5>
			{listItems}
		</div>
	);
}
function BioModelList(props) {
	const biomodelList = props.biomodelList;
	const isClickEnabled = props.isClickEnabled;
	const listItems = biomodelList.map((item) =>
		<ListItem key={item.id}
					value={item.name} isClickEnabled={isClickEnabled}/>					
	);
	return (
		<div className="container">
			<h5> Biomodel List </h5>
			{listItems}
		</div>
	);
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);    
  }

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
				type="submit"
				onClick={this.props.handleSearch}
				className="btn btn-outline-success my-2 my-sm-0">
				Search
			</button>
		</form>
    );
  }
}

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			searchText : '',
			mondoList: [
				{id: 1, name: 'No Result'}
			],
			geneList: [
				{gene_id: 1, gene_symbol: 'No Result'}
			],

			biomodelList: [
				{id: 1, name: 'No Result'}
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
        
	}
	handleMondoSearch(e) {
		fetch('http://127.0.0.1:5000/api/disease/'.concat(this.state.searchText).concat('?size=5'))
			.then(response => response.json())
			.then(data => this.setState({ mondoList: data, mondoisClickEnabled: true }));
	}
	handleTextChange(e) {
		this.setState({searchText : e.target.value});
	}
	
	handleMondoClick(mondoItem) {
		fetch('http://127.0.0.1:5000/api/disease-to-gene/'.concat(mondoItem).concat('?size=5'))
			.then(response => response.json())
			.then(data => this.setState({ geneList: data, geneisClickEnabled: true }));
	}
    handleGeneClick(geneItem) {
        fetch('http://127.0.0.1:5000/api/gene-to-pathway/'.concat(geneItem).concat('?size=5'))
			.then(response => response.json())
			.then(data => this.setState({ biomodelList: data, bioisClickEnabled: true }));
    }

	render() {
		return (
			<div className="container">
			<SearchBar handleSearch={this.handleMondoSearch} handleTextChange={this.handleTextChange}/>		
			<div className="row">
				<div className="col-sm-3">
					<MondoList 
						mondoList={this.state.mondoList} 
						isClickEnabled={this.state.mondoisClickEnabled}
						onClick={this.handleMondoClick}/>
				</div>
				<div className="col-sm-3">
					<GeneList 
                        geneList={this.state.geneList} 
                        isClickEnabled={this.state.geneisClickEnabled} 
                        onClick={this.handleGeneClick}/>
				</div>
				<div className="col-sm-3">
					<BioModelList biomodelList={this.state.biomodelList} isClickEnabled={this.state.bioisClickEnabled} />
				</div>
			</div>
		  </div>
		);
  }
}

export default App;
