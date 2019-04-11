import React from 'react';

const imageViewStyle = {
    overflow: "auto",
    height: "550px",
    outline: "solid #F5F5F5"
}

export default class ImageView extends React.Component {
	render() {
		return (
            <div className="container-fluid">
                <h6> Biomodel View </h6>
                <div style={imageViewStyle}>                
                    <img src={this.props.src}/>
                </div>
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
