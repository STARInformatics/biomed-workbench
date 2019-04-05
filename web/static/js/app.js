'use strict';

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {searchText : ''}
    this.handleClick = this.handleClick.bind(this);
    this.handleTextChange = this.handleTextChange.bind(this);
  }

  handleClick(e) {
    alert(this.state.searchText);
  }

  handleTextChange(e) {
    this.setState({searchText : e.target.value})
  }

  render() {
    return (
      <div className="topnav">
        <input
          type="text"
          onChange={this.handleTextChange}
          placeholder="Search.."
          id="search"
        />
        <button
          type="submit"
          onClick={this.handleClick}>
          <i className="fa fa-search"></i>
        </button>
      </div>
    );
  }
}

ReactDOM.render(
  <SearchBar/>,
  document.getElementById('root')
);
