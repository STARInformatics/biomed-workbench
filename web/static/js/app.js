'use strict';

function ListItem(props) {
	return <li>{props.value}</li>;
}

function ListItems(props) {
	const items = props.items;
	const listItems = items.map((item) =>
		<ListItem key={item.id}
					value={item.name} />					
	);
	return (
		<ul>
			{listItems}
		</ul>
	);
}

function ListView(props) {
	const mondoList = props.mondoList;
	const geneList = props.geneList;
	const biomodelList = props.biomodelList;
	return (
		<div className="ListView">
			<div className="MondoList">
				<h3> Disease Index </h3>
				<ListItems items={mondoList} />
			</div>
			<div className="GeneList">
				<h3> Gene List </h3>
				<ListItems items={geneList} />
			</div>
			<div className="BiomodelList">
				<h3> Biomodel List </h3>
				<ListItems items={biomodelList} />
			</div>
		</div>
	);
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {searchText : ''}
    this.handleClick = this.handleClick.bind(this);
    this.handleTextChange = this.handleTextChange.bind(this);
  }

  handleClick(e) {
    alert(this.state.searchText);
  }

  handleTextChange(e) {
    this.setState({searchText : e.target.value})
  }

  render() {
    return (
      <div className="topnav">
        <input
          type="text"
          onChange={this.handleTextChange}
          placeholder="Search.."
          id="search"
        />
        <button
          type="submit"
          onClick={this.handleClick}>
          <i className="fa fa-search"></i>
        </button>
      </div>
    );
  }
}

function App(props) {
	const mondoList = props.mondoList;
	const geneList = props.geneList;
	const biomodelList = props.biomodelList;
	return(
		<div className="app">
			<SearchBar/>
			<ListView mondoList={mondoList} geneList={geneList} biomodelList={biomodelList} />
		</div>
	);
}

const mondoList = [
	{id: 1, name: 'cancer'},
	{id: 2, name: 'diabetes'}
];

const geneList = [
	{id: 1, name: 'geneA'},
	{id: 2, name: 'geneB'},
	{id: 3, name: 'geneC'}
];

const biomodelList = [
	{id: 1, name: 'biomodelA'},
	{id: 2, name: 'biomodelB'},
	{id: 3, name: 'biomodelC'},
	{id: 4, name: 'biomodelD'}
];


ReactDOM.render(
  <App mondoList={mondoList} geneList={geneList} biomodelList={biomodelList} />,
  document.getElementById('root')
);
