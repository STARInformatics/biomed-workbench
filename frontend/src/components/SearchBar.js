import React from 'react';

const searchBarStyle = {
    marginTop: "20px",
    marginLeft: "25px",
    marginLeft: "15px",
    marginBottom: "20px",
}

class SearchBar extends React.Component {
  handleKeyPress = event => {
    if (event.key === 'Enter') {
      this.props.handleSearch();
    }
  };

  render() {
    return (
        <div style={searchBarStyle}>
            <form className="form-inline">
                <input
                    type="search"
                    className="form-control mr-sm-2"
                    onChange={this.props.handleTextChange}
                    placeholder="Search.."
                    aria-label="Search"
                    id="search"
                    onKeyPress={this.handleKeyPress}
                />
                <button
                    type="button"
                    onClick={this.props.handleSearch}
                    className="btn btn-outline-success my-2 my-sm-0">
                    Search
                </button>
            </form>
        </div>
    );
  }
}

export default SearchBar;
