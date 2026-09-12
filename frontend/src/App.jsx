import { useState } from "react";
import axios from "axios";
import "./App.css";


function App() {

  const [repoUrl, setRepoUrl] =
    useState("");

  const [repositoryId, setRepositoryId] =
    useState("");

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [sources, setSources] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");


  const ingestRepository =
    async () => {

      if (!repoUrl.trim()) {
        setMessage(
          "Enter a GitHub repository URL."
        );
        return;
      }

      try {

        setLoading(true);
        setMessage(
          "Analyzing repository..."
        );

        const response =
          await axios.post(
            "http://127.0.0.1:8000/ingest",
            {
              repo_url: repoUrl
            }
          );

        setRepositoryId(
          response.data.repository_id
        );

        setMessage(
          `Repository indexed successfully. ${response.data.files} files and ${response.data.chunks} chunks found.`
        );

      } catch (error) {

        console.error(error);

        setMessage(
          "Repository ingestion failed."
        );

      } finally {

        setLoading(false);

      }
    };


  const askQuestion =
    async () => {

      if (!repositoryId) {

        setMessage(
          "Analyze a repository first."
        );

        return;
      }

      if (!question.trim()) {

        setMessage(
          "Enter a question."
        );

        return;
      }

      try {

        setLoading(true);

        setAnswer("");

        const response =
          await axios.post(
            "http://127.0.0.1:8000/ask",
            {
              repository_id:
                repositoryId,

              question:
                question
            }
          );

        setAnswer(
          response.data.answer
        );

        setSources(
          response.data.sources || []
        );

      } catch (error) {

        console.error(error);

        setAnswer(
          "Unable to answer the question."
        );

      } finally {

        setLoading(false);

      }
    };


  return (

    <div className="app">

      <div className="container">

        <header>

          <div className="badge">
            AI CODE INTELLIGENCE
          </div>

          <h1>
            GitHub Codebase
            <span> Copilot</span>
          </h1>

          <p>
            Analyze GitHub repositories
            with Retrieval-Augmented
            Generation and semantic
            code search.
          </p>

        </header>


        <section className="card">

          <h2>
            Repository
          </h2>

          <div className="input-row">

            <input
              placeholder="https://github.com/user/repository"
              value={repoUrl}
              onChange={
                (e) =>
                  setRepoUrl(
                    e.target.value
                  )
              }
            />

            <button
              onClick={
                ingestRepository
              }
              disabled={loading}
            >
              Analyze
            </button>

          </div>

          {
            repositoryId && (

              <div className="repo-id">

                Repository ID:

                <code>
                  {repositoryId}
                </code>

              </div>

            )
          }

          {
            message && (

              <p className="message">
                {message}
              </p>

            )
          }

        </section>


        <section className="card">

          <h2>
            Ask the Codebase
          </h2>

          <textarea
            placeholder="What does this project do?"
            value={question}
            onChange={
              (e) =>
                setQuestion(
                  e.target.value
                )
            }
          />

          <button
            className="ask-button"
            onClick={
              askQuestion
            }
            disabled={loading}
          >

            {
              loading
                ? "Processing..."
                : "Ask Copilot"
            }

          </button>

        </section>


        {
          answer && (

            <section className="card">

              <h2>
                AI Answer
              </h2>

              <div className="answer">
                {answer}
              </div>

              {
                sources.length > 0 && (

                  <div className="sources">

                    <h3>
                      Sources
                    </h3>

                    {
                      sources.map(
                        (
                          source,
                          index
                        ) => (

                          <div
                            className="source"
                            key={index}
                          >

                            <strong>
                              {
                                source.file_path
                              }
                            </strong>

                            <span>

                              Lines{" "}

                              {
                                source.start_line
                              }

                              {" - "}

                              {
                                source.end_line
                              }

                            </span>

                          </div>

                        )
                      )
                    }

                  </div>

                )
              }

            </section>

          )
        }

      </div>

    </div>

  );
}


export default App;