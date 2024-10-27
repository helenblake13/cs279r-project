// src/App.js
import React, { useState } from "react";

function App() {
  const [story, setStory] = useState("");
  const [highlightedText, setHighlightedText] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [rewrite, setRewrite] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Handle story text input change
  const handleStoryChange = (e) => {
    setStory(e.target.value);
  };

  // Capture highlighted text
  const handleHighlight = () => {
    const selectedText = window.getSelection().toString();
    setHighlightedText(selectedText);
  };

  // Handle form submission to analyze highlighted text
  const handleSubmit = async () => {
    if (highlightedText) {
      setIsLoading(true);
      try {
        const response = await fetch("http://localhost:5001/api/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            story: story,
            highlighted: highlightedText,
          }),
        });

        const data = await response.json();
        if (response.ok) {
          setAnalysis(data.analysis);
          setRewrite(data.rewrite);
        } else {
          alert("Error: " + data.error);
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server");
      } finally {
        setIsLoading(false);
      }
    } else {
      alert("Please highlight a sentence!");
    }
  };

  return (
    <div style={{ padding: "20px", borderRadius: "5px", maxWidth: "800px", fontFamily: "EB Garamond", margin: "0 auto" }}>

      <h1 style= {{ padding: "10px 20px", backgroundColor: "#dcd0ea", color: "white", fontSize: "15px" }}> helen todo banner dedicated to what this project entails </h1>

      <h2>Creative Writing Assistant</h2>

      <div style={{ display: "flex", alignItems: "center", columnGap: "100px" }}>
        
        <textarea
          value={story}
          onChange={handleStoryChange}
          onMouseUp={handleHighlight}
          rows="10"
          cols="60"
          placeholder="Paste your story here..."
          style={{ padding: "10px", fontFamily: "EB Garamond", fontSize: "16px", width: "100%" }}
        />

        <h1 style={{ fontSize: "20px" }}>helen todo how to use the tool etc etc testing testing</h1>

      </div>

      <br />
      <button
        onClick={handleSubmit}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          fontFamily: "EB Garamond",
          fontSize: "16px",
          backgroundColor: "#dcd0ea",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: isLoading ? "not-allowed" : "pointer",
          opacity: isLoading ? 0.7 : 1,
        }}
        disabled={isLoading}
      >
        {isLoading ? "Processing..." : "Analyze Highlighted Text"}
      </button>

      {highlightedText && (
        <div style={{ marginTop: "20px" }}>
          <h3>Highlighted Sentence:</h3>
          <p>{highlightedText}</p>
        </div>
      )}

      {analysis && (
        <div style={{ marginTop: "20px" }}>
          <h3>Analysis:</h3>
          <p style={{ whiteSpace: "pre-wrap", fontFamily: "EB Garamond" }}>{analysis}</p>
        </div>
      )}

      {rewrite && (
        <div style={{ marginTop: "20px" }}>
          <h3>Rewritten Version:</h3>
          <p style={{ whiteSpace: "pre-wrap", fontFamily: "EB Garamond" }}>{rewrite}</p>
        </div>
      )}
    </div>
  );
}

export default App;
