import React, { useState } from 'react';
import './App.css';

import client from "./client";
import { COLOR_QUERY, CREATE_COLOR_MUTATION, CHANGE_COLOR_CODE, Color, CreateColorVariables, DeleteColorVariables, DELETE_COLOR_MUTATION } from "./graphql"

function App() {
  const [color, setColor] = React.useState<Color | null>(null);
  const [inputColor, setInputColor] = useState("");
  const [inputColorCode, setInputColorCode] = useState([0, 0, 0]);

  const fetchColor = () => {
    client.query<Color[]>({ query: COLOR_QUERY }).then((result) => {
      console.log(result.data);
    })
  }

  const setInputs = (e: React.FormEvent<HTMLFormElement>) => {
    const target = e.target as typeof e.target & {
      color: { value: string };
      colorCode: { value: string };
    };
    setInputColor(target.color.value);
    setInputColorCode(target.colorCode?.value.split(",").map((v) => parseInt(v, 10)));
  }
  const CreateNewColor = (e: React.FormEvent<HTMLFormElement>) => {

    e.preventDefault();
    const target = e.target as typeof e.target & {
      color: { value: string };
      colorCode: { value: string };
    };
    const color = target.color.value;
    const colorCode = target.colorCode.value.split(",").map((v) => parseInt(v, 10));
    // setInputs(e);
    const [r, g, b] = colorCode;

    console.log("in onsubmit");

    client.mutate<boolean, CreateColorVariables>({
      mutation: CREATE_COLOR_MUTATION,
      variables: { input: { color: color, colorCode: [r, g, b] } },
    }).then((result) => {
      console.log(result);
    });
  }

  const ChangeColorCode = (e: React.FormEvent<HTMLFormElement>) => {

    e.preventDefault();
    // setInputs(e);
    const target = e.target as typeof e.target & {
      color: { value: string };
      colorCode: { value: string };
    };
    const color = target.color.value;
    const colorCode = target.colorCode.value.split(",").map((v) => parseInt(v, 10));
    const [r, g, b] = colorCode;
    console.log("in change color code");

    client.mutate<boolean, CreateColorVariables>({
      mutation: CHANGE_COLOR_CODE,
      variables: { input: { color: color, colorCode: [r, g, b] } },
    }).then((result) => {
      console.log(result);
    });
  }

  const DeleteColor = (e: React.FormEvent<HTMLFormElement>) => {

    e.preventDefault();
    // setInputs(e);
    const target = e.target as typeof e.target & {
      color: { value: string };
      
    };
    const color = target.color.value;
    
    console.log("in delete color code");

    client.mutate<boolean, DeleteColorVariables>({
      mutation: DELETE_COLOR_MUTATION,
      variables: { input: { color: color} },
    }).then((result) => {
      console.log(result);
    });
  }

  return (
    <div className="App">
      <header>
        <button onClick={fetchColor}>Fetch all colors</button>
        <p>Create new color</p>
        <form onSubmit={CreateNewColor}>
          <label>Color</label>
          <input name="color" type="text" />
          <label>Color Code</label>
          <input name='colorCode' type='text' />
          <button type='submit'>Submit</button>
        </form>
        <p>Update colorCode</p>
        <form onSubmit={ChangeColorCode}>
          <label>Color</label>
          <input name="color" type="text" />
          <label>Color Code</label>
          <input name='colorCode' type='text' />
          <button type='submit'>Submit</button>
        </form>
        <p>Delete Color</p>
        <form onSubmit={DeleteColor}>
          <label>Color</label>
          <input name="color" type="text" />
          <button type='submit'>Submit</button>
        </form>
      </header>
    </div>
  );
}

export default App;