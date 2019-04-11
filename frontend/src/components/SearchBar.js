import React from 'react';

class SearchBar extends React.Component {
  render() {
    return (
		<form className="form-inline">
			<input
				type="search"
				className="form-control mr-sm-2"
				onChange={this.props.handleTextChange}
				placeholder="Search.."
				aria-label="Search"
				id="search"
			/>
			<button
				type="button"
				onClick={this.props.handleSearch}
				className="btn btn-outline-success my-2 my-sm-0">
				Search
			</button>
		</form>
    );
  }
}

export default SearchBar;
