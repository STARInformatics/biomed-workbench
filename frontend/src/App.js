import React, { Component } from 'react';
import './App.css';
import './css/searchbar.css';
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
			return <li onClick={this.handleClick} className="list-group-item">{this.props.value}</li>;
		}
		else {
			return <li className="list-group-item">{this.props.value}</li>;
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
		<ul className="list-group">
			{listItems}
		</ul>
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
		enableClick: false
	}
    this.handleClick = this.handleClick.bind(this);
    this.handleTextChange = this.handleTextChange.bind(this);
  }

  handleClick(e) {
		fetch('http://127.0.0.1:5000/api/disease/'.concat(this.state.searchText).concat('?size=5'))
			.then(response => response.json())
			.then(data => this.setState({ mondoList: data, enableClick: true }));
	}

  handleTextChange(e) {
    this.setState({searchText : e.target.value})
  }

  render() {
    return (
      <div className="container">
        <input
          type="text"
		  className="form-control"
          onChange={this.handleTextChange}
          placeholder="Search.."
          id="search"
        />
        <button
          type="submit"
          onClick={this.handleClick}>
          <i className="fa fa-search"></i>
        </button>
		<div className="row">
			<div className="col-sm-4">
				<MondoList mondoList={this.state.mondoList} enableClick={this.state.enableClick} />
			</div>
			<div className="col-sm-4">
				<GeneList geneList={this.state.geneList} enableClick={this.state.enableClick} />
			</div>
			<div className="col-sm-4">
				<BioModelList biomodelList={this.state.biomodelList} enableClick={this.state.enableClick} />
			</div>
		</div>
      </div>
    );
  }
}

class App extends Component {
  render() {
    return (
		<SearchBar/>
    );
  }
}

export default App;
