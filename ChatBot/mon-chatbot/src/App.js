import React, { useState } from "react";
import axios from "axios";

import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (input.trim() !== "") {
      const userMessage = { text: input, user: "me" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      const userInput = input;
      setInput("");

      try {
        const response = await axios.post("http://127.0.0.1:5000/predict", {
          text: userInput,
        });
        const botMessage = { text: response.data.reply, user: "bot" };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error("Erreur lors de la communication avec le backend", error);
        const errorMessage = {
          text: "Erreur lors de la communication avec le serveur.",
          user: "bot",
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  return (
    <div className="App">
      <div className="container">
        <div className="left-panel">
          <h1>
            مرحبا بكم في الجامعة الدولية بالدار البيضاء، هل لديك أي أسئلة؟
          </h1>
        </div>
        <div className="right-panel">
          <div className="chatbox">
            <div className="messages">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.user}`}>
                  {msg.text}
                </div>
              ))}
            </div>
            <div className="input-area">
              <button onClick={handleSend}>
                <span class="icon-send"></span>
              </button>
              <input
                type="text"
                value={input}
                onChange={handleInputChange}
                placeholder="........اكتب سؤالك"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
