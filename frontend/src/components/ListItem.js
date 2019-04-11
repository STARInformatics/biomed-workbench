import React from 'react';

const scrollStyle = {
    overflowY: "auto",
    height: "150px",
    marginBottom: "15px",
    backgroundColor: "#F5F5F5"
};

export default class ListItem extends React.Component {
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



export function MondoList(props) {
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
			<div style={scrollStyle}>
                {listItems}
            </div>
		</div>
	);
}

export function GeneList(props) {
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
            <div style={scrollStyle}>
                {listItems}
            </div>
		</div>
	);
}
export function BioModelList(props) {
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
            <div style={scrollStyle}>
                {listItems}
            </div>
		</div>
	);
}
