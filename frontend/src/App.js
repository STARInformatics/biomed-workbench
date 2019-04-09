import React, { Component } from 'react';
import './App.css';
import 'font-awesome/css/font-awesome.min.css';

class ListItem extends React.Component {
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}
	handleClick(e) {
		alert('You just choose '.concat(this.props.value));
	}
	render() {
		if (this.props.enableClick === true) {
			return <a href="#" onClick={this.handleClick} className="list-group-item list-group-item-action">
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

function ListItems(props) {
	const items = props.items;
	const enableClick = props.enableClick;
	const listItems = items.map((item) =>
		<ListItem key={item.id}
					value={item.name} enableClick={enableClick}/>					
	);
	return (
		<div className="list-group">
			{listItems}
		</div>
	);
}

function MondoList(props) {
	const mondoList = props.mondoList;
	const enableClick = props.enableClick;
	return (
		<div className="container">
			<h5> Disease Index </h5>
			<ListItems items={mondoList} enableClick={enableClick}/>
		</div>
	);
}

function GeneList(props) {
	const geneList = props.geneList;
	const enableClick = props.enableClick;
	return (
		<div className="container">
			<h5> Gene List </h5>
			<ListItems items={geneList} enableClick={enableClick}/>
		</div>
	);
}
function BioModelList(props) {
	const biomodelList = props.biomodelList;
	const enableClick = props.enableClick;
	return (
		<div className="container">
			<h5> Biomodel List </h5>
			<ListItems items={biomodelList} enableClick={enableClick}/>
		</div>
	);
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);    
  }

  render() {
    return (
		<form class="form-inline">
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
				{id: 1, name: 'No Result'}
			],

			biomodelList: [
				{id: 1, name: 'No Result'}
			],
			mondoEnableClick: false,
			geneEnableClick: false,
			bioEnableClick: false
			
		}
		this.handleSearch = this.handleSearch.bind(this);
		this.handleTextChange = this.handleTextChange.bind(this);
	}
	handleSearch(e) {
		fetch('http://127.0.0.1:5000/api/disease/'.concat(this.state.searchText).concat('?size=5'))
			.then(response => response.json())
			.then(data => this.setState({ mondoList: data, mondoEnableClick: true }));
	}
	handleTextChange(e) {
		this.setState({searchText : e.target.value});
	}
	render() {
		return (
			<div className="container">
			<SearchBar handleSearch={this.handleSearch} handleTextChange={this.handleTextChange}/>		
			<div className="row">
				<div className="col-sm-3">
					<MondoList mondoList={this.state.mondoList} enableClick={this.state.mondoEnableClick} />
				</div>
				<div className="col-sm-3">
					<GeneList geneList={this.state.geneList} enableClick={this.state.geneEnableClick} />
				</div>
				<div className="col-sm-3">
					<BioModelList biomodelList={this.state.biomodelList} enableClick={this.state.bioEnableClick} />
				</div>
			</div>
		  </div>
		);
  }
}

export default App;
