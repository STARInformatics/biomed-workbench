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
		<div>
			<div>
				<h3> Disease Index </h3>
				<ListItems items={mondoList} />
			</div>
			<div>
				<h3> Gene List </h3>
				<ListItems items={geneList} />
			</div>
			<div>
				<h3> Biomodel List </h3>
				<ListItems items={biomodelList} />
			</div>
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
	React.createElement(ListView, {mondoList: mondoList, geneList: geneList, biomodelList: biomodelList}, null),
	document.getElementById('list_container')
);

	
