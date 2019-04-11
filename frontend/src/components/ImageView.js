import React from 'react';

export default class ImageView extends React.Component {
	render() {
		return (
			<div>
                <img src={this.props.src}/>
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
