'use strict';

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {clicked : false};
  }

  render() {
    if (this.state.clicked) {
      return "You've clicked me!";
    }

    return React.createElement(
      'button',
      { onClick: () => this.setState({ clicked: true }) },
      'Like'
    );
  }
}

const domContainer = document.querySelector('#button_container');
ReactDOM.render(React.createElement(LikeButton), domContainer);
