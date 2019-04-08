import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import './css/searchbar.css';
import 'font-awesome/css/font-awesome.min.css';

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

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;
