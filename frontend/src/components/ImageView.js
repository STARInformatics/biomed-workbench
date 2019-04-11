import React from 'react';

class ImageView extends React.Component {
	render() {
		return (
			<div>
			<img src={this.props.src}/>
			</div>
		)
	}
}

export default ImageView;
