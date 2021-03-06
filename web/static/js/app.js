function ListItem(props) {
	return <li className="list-group-item">{props.value}</li>;
}

function ListItems(props) {
	const items = props.items;
	const listItems = items.map((item) =>
		<ListItem key={item.id}
					value={item.name} />					
	);
	return (
		<ul className="list-group">
			{listItems}
		</ul>
	);
}

function MondoList(props) {
	const mondoList = props.mondoList;
	return (
		<div className="container">
			<h5> Disease Index </h5>
			<ListItems items={mondoList} />
		</div>
	);
}

function GeneList(props) {
	const geneList = props.geneList;
	return (
		<div className="container">
			<h5> Gene List </h5>
			<ListItems items={geneList} />
		</div>
	);
}
function BioModelList(props) {
	const biomodelList = props.biomodelList;
	return (
		<div className="container">
			<h5> Biomodel List </h5>
			<ListItems items={biomodelList} />
		</div>
	);
}

const BASE_URL =  'https://bkw.starinformatics.com';  //process.env.REACT_APP_BASE_URL || 'http://localhost:5000';
const API_PATH =  '/service';  //process.env.REACT_APP_API_PATH || '';
const SERVICE_URL  = BASE_URL + API_PATH;

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
		searchText : '',
		mondoList: [
				{id: 1, name: 'cancer'},
				{id: 2, name: 'diabetes'}
			],
			geneList: [
				{id: 1, name: 'geneA'},
				{id: 2, name: 'geneB'},
				{id: 3, name: 'geneC'}
			],

			biomodelList: [
				{id: 1, name: 'biomodelA'},
				{id: 2, name: 'biomodelB'},
				{id: 3, name: 'biomodelC'},
				{id: 4, name: 'biomodelD'}
			]
		}
    this.handleClick = this.handleClick.bind(this);
    this.handleTextChange = this.handleTextChange.bind(this);
  }

	handleClick(e) {
		fetch(SERVICE_URL.concat('/api/disease/').concat(this.state.searchText).concat('?size=5'))
			.then(response => response.json())
			.then(data => this.setState({ mondoList: data }));				
	}
	
			

  handleTextChange(e) {
    this.setState({searchText : e.target.value})
  }

  render() {
    return (
      <div className="container">
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
		<div className="row">
			<div className="col-sm-4">
				<MondoList mondoList={this.state.mondoList} />
			</div>
			<div className="col-sm-4">
				<GeneList geneList={this.state.geneList} />
			</div>
			<div className="col-sm-4">
				<BioModelList biomodelList={this.state.biomodelList} />
			</div>
		</div>
      </div>
    );
  }
}

class App extends React.Component {
	constructor(props) {
		super(props);
	}
	render() {
		return(
			<div className="app">
				<SearchBar/>				
			</div>
	
		)
	}
}


ReactDOM.render(
  <App />,
  document.getElementById('root')
);
