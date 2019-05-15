import React from "react";
import ReactDOM from "react-dom";
import { Form, FormGroup, FormControl, InputGroup, Button } from "react-bootstrap";

const searchBarStyle = {
    marginTop: "20px",
    marginLeft: "25px",
    marginLeft: "15px",
    marginBottom: "20px",
}

class SearchBar extends React.Component {

  constructor(props) {
    super(props);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  handleKeyPress(event) {
    if (event.key == 'Enter') {
      this.props.handleSearch();
      return true;
    } else {
      return false;
    }
  };

  render() {
    return (
        <Form inline onSubmit={e => { e.preventDefault(); }} style={searchBarStyle}>
        <FormGroup>
          <InputGroup>
            <FormControl
              placeholder="Disease keywords ..."
              type="input"
              onKeyPress={event => {
                if (event.key === "Enter") {
                  this.props.handleSearch();
                }
              }}
            />
          </InputGroup>
          <button
              type="button"
              onClick={this.props.handleSearch}
              className="btn btn-outline-success my-2 my-sm-0">
              Search
          </button>
        </FormGroup>
        </Form>
    );
  }
}

export default SearchBar;
