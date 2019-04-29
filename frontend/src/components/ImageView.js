import React from 'react';
import Zmage from 'react-zmage'
import { isEmptyStatement } from '@babel/types';

const imageViewStyle = {
    overflow: "auto",
    height: "550px",
    outline: "solid #F5F5F5"
}

const scrollStyle = {
    overflowY: "auto",
    height: "150px"
};

export class ImageView extends React.Component {
	render() {
		return (
            <div className="container-fluid">
                <h6> Biomodel View </h6>
                <div style={imageViewStyle}>
                    <Zmage src={this.props.src}/>
                </div>
                <div style={scrollStyle}/>
            </div>
		)
	}
}

export default function ImageDescription() {
    if (isEmpty(props.text)){
        return (
            <div>
                <h6>Gene/Drugs Details </h6>
                <p>No Search </p>
            </div>
        );
    } else if (props.text.concept.category[0]==="disease"){
        return (
            <div>
                <h6>Disease Details </h6>
                <p>Name: {props.text.concept.name}</p>
                <p>ID: {props.text.concept.id}</p>
                <p>Definition: {props.text.concept.definition}</p>
            </div>
        );
    } else if (props.text.concept.category[1]==="gene") {
        return (
            <div>
                <h6>Gene Details </h6>
                <p>Name: {props.text.concept.name}</p>
                <p>ID: {props.text.concept.id}</p>
                <p>Chromosome: {props.text.concept.chromosome}</p>
                <p>Location: {props.text.concept.location}</p>
                <p>gene_faminly: {props.text.concept.gene_faminly[0]}</p>
            </div>
        );
    }

}

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}
