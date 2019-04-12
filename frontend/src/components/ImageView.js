import React from 'react';
import Zmage from 'react-zmage'

const imageViewStyle = {
    overflow: "auto",
    height: "550px",
    outline: "solid #F5F5F5"
}

const scrollStyle = {
    overflowY: "auto",
    height: "150px",
    marginBottom: "15px",
    backgroundColor: "#F5F5F5"
};

export default class ImageView extends React.Component {
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

export class ImageDescription extends React.Component {
    constructor(props) {
		super(props);
    }
    render() {
        return (
            <div>
                <h6>Gene/Drugs Details </h6>
                <p>{this.props.text} </p>
            </div>
        )
    }
}
