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
    <div style={{ fontFamily: "EB Garamond", margin: "0 auto" }}>

      <h1 style= {{ padding: "10px 20px", backgroundColor: "#dcd0ea", color: "white", fontSize: "15px", textAlign: "center", width: "100vw", margin: "0", boxSizing: "border-box" }}> Welcome! Please enter a piece of fiction and highlight the sentence you wish to be replaced. </h1>

      <div style = {{ marginLeft: "5%" }}>

        <h2>Creative Writing Assistant</h2>

        <div style={{ display: "flex", alignItems: "center", columnGap: "45px" }}>
          
          <textarea
            value={story}
            onChange={handleStoryChange}
            onMouseUp={handleHighlight}
            rows="10"
            cols="60"
            placeholder="Paste your story here..."
            style={{ padding: "10px", fontFamily: "EB Garamond", fontSize: "16px", width: "900px", height: "350px", resize: "none" }}
          />

          <div style = {{ display: "flex", flexDirection: "column", alignItems: "center" }}>

            <h1 style = {{ fontSize: "18px", fontWeight: "bold", textAlign: "center", maxWidth: "300px", color: "white", backgroundColor: "#dcd0ea", borderRadius: "5px", padding: "10px 30px" }}> Note from the Creators </h1>
            <h1 style={{ fontSize: "15px", fontWeight: "lighter", alignItems: "justify", maxWidth: "350px", border: "1px solid black", borderRadius: "5px", padding: "10px", boxSizing: "border-box" }}> Hello! We're glad you're here.  
            The three of us are currently students in COMPSCI 2790r, a class dedicated to AI-human interactions, 
            and we wish to utilize LLMs to augment the creative experience for writers. In particular, when 
            creative writers use LLMs in the editing process of their work, the LLM often becomes a black box, 
            and we aim to dispel any disconnect in the communication between LLM and user. Specifically, we are using 
            an OpenAI to structure a given explanation for the sentence replacement in terms that might resonate more with 
            creative writers. If you have any questions, please feel free to reach out to us at: helenblake@college.harvard.edu, 
            benchoi@college.harvard.edu, or jorontopratt@college.harvard.edu.</h1>

          </div>

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

        <div style = {{ maxWidth: "1100px" }}>

          {highlightedText && (
            <div style={{ marginTop: "20px" }}>
              <h3>Highlighted Sentence:</h3>
              <p style = {{ overflowWrap: "normal", fontFamily: "EB Garamond" }}>{highlightedText}</p>
            </div>
          )}

          {analysis && (
            <div style={{ marginTop: "20px" }}>
              <h3>Analysis:</h3>
              <p style={{ whiteSpace: "pre-wrap", overflowWrap: "normal", fontFamily: "EB Garamond" }}>{analysis}</p>
            </div>
          )}

          {rewrite && (
            <div style={{ marginTop: "20px" }}>
              <h3>Rewritten Version:</h3>
              <p style={{ whiteSpace: "pre-wrap", overflowWrap: "normal", fontFamily: "EB Garamond" }}>{rewrite}</p>
            </div>
          )}

        </div>
      </div>
      
    </div>
  );
}

export default App;
