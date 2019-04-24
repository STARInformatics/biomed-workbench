import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import LoadingOverlay from 'react-loading-overlay';
import Loader from 'react-loader-spinner';

export function MyLoader(props) {
	return (
		<LoadingOverlay
			active={props.isLoading}
			spinner={<Loader  type="ThreeDots" color="#2BAD60" height="30" width="30" />}
		>
			{props.children}
		</LoadingOverlay>
	)
}


const scrollStyle = {
    overflowY: "auto",
    height: "180px",
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
		return <button
					className="list-group-item list-group-item-action"
					onClick={this.handleClick}>
						{this.props.value}
				</button>;
		
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
	if(isClickEnabled=== true) {
		return (
			<div className="container">
				<h6> Disease Index </h6>
				<MyLoader isLoading={props.isLoading}>
					<div style={scrollStyle}>						
							{listItems}						
					</div>
				</MyLoader> 
			</div>
		);
	} else {
		return(
			<div className="container">
				<h6> Disease List </h6>
				<MyLoader isLoading={props.isLoading}>
					<div style={scrollStyle}>						
							<button className="list-group-item list-group-item-action disabled">
								No Search
							</button>						
					</div>
				</MyLoader>
			</div>
		);
	}
}

export class AccordionList extends React.Component {

	render() {
		const listItems = this.props.geneList.map((item) =>
			<ListItem
				key={item.gene_symbol}
				index={item.gene_id}
				value={item.gene_symbol}
				isClickEnabled={this.props.isClickEnabled}
				onClick={this.props.onClick}/>
		);
				
		return (
			<Card>
				<Card.Header>
					<Accordion.Toggle as={Button} variant="link" eventKey={this.props.index}>
						{this.props.value}
					</Accordion.Toggle>
				</Card.Header>
				<Accordion.Collapse eventKey={this.props.index}>
					<Card.Body>{listItems}</Card.Body>
				</Accordion.Collapse>
			</Card>			
		);
	}
	
	
} 

export function GeneList(props) {
	const geneList = props.geneList;
	const isClickEnabled = props.isClickEnabled;
	const accordionItems = geneList.map((item) =>
		<AccordionList
			key={item.id}
			index={item.id}
			value={item.name}
			geneList={item.items}
			isClickEnabled={isClickEnabled}
			onClick={props.onClick}/>
	);
	if(isClickEnabled=== true) {
		return(
			<div className="container">
				<h6> Gene List </h6>
				<div style={scrollStyle}>
					<MyLoader isLoading={props.isLoading}>
						<Accordion>
							{accordionItems}
						</Accordion>
					</MyLoader>
				</div>
			</div>
		);
		
	} else {
		return(
			<div className="container">
				<h6> Gene List </h6>
				<div style={scrollStyle}>
					<MyLoader isLoading={props.isLoading}>
						<button className="list-group-item list-group-item-action disabled">
							No Search
						</button>
					</MyLoader>
				</div>
			</div>
		);

	}

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
	if(isClickEnabled=== true) {
		return (
			<div className="container">
				<h6> Biomodel List </h6>
				<MyLoader isLoading={props.isLoading}>
					<div style={scrollStyle}>						
							{listItems}									
					</div>
				</MyLoader>  >

			</div>
		);
	} else {
		return(
			<div className="container">
				<h6> Biomodel List </h6>
				<MyLoader isLoading={props.isLoading}>
					<div style={scrollStyle}>						
							<button className="list-group-item list-group-item-action disabled">
								No Search
							</button>
					</div>
				</MyLoader>
			</div>
		);
	}
}
