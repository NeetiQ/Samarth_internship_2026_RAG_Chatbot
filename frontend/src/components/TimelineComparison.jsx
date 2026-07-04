export default function TimelineComparison() {
  return (
    <div>

      {/* CASE TIMELINES */}

      <h3 className="timeline-title">
        📅 Case Progress Comparison
      </h3>

      <div className="dual-timeline">

        {/* CASE A */}

        <div className="timeline-column">

          <h4>Case A</h4>

          <div className="timeline-item">
            <span className="dot"></span>
            <div>
              <strong>Filed</strong>
              <p>12 Jan 2022</p>
            </div>
          </div>

          <div className="timeline-item">
            <span className="dot"></span>
            <div>
              <strong>First Hearing</strong>
              <p>05 Apr 2022</p>
            </div>
          </div>

          <div className="timeline-item">
            <span className="dot"></span>
            <div>
              <strong>Judgment</strong>
              <p>22 Aug 2022</p>
            </div>
          </div>

        </div>

        {/* CASE B */}

        <div className="timeline-column">

          <h4>Case B</h4>

          <div className="timeline-item">
            <span className="dot"></span>
            <div>
              <strong>Filed</strong>
              <p>18 Feb 2023</p>
            </div>
          </div>

          <div className="timeline-item">
            <span className="dot"></span>
            <div>
              <strong>First Hearing</strong>
              <p>10 Jun 2023</p>
            </div>
          </div>

          <div className="timeline-item">
            <span className="dot gold"></span>
            <div>
              <strong>Judgment</strong>
              <p>03 Dec 2023</p>
            </div>
          </div>

        </div>

      </div>

      {/* AI BREAKDOWN */}

      <h3 className="breakdown-title">
        🧠 AI Similarity Breakdown
      </h3>

      <div className="breakdown">

        <div className="breakdown-row">
          <span>Facts Match</span>
          <span>92%</span>
        </div>

        <div className="progress">
          <div style={{ width: "92%" }}></div>
        </div>

        <div className="breakdown-row">
          <span>Legal Sections</span>
          <span>88%</span>
        </div>

        <div className="progress">
          <div style={{ width: "88%" }}></div>
        </div>

        <div className="breakdown-row">
          <span>Precedents</span>
          <span>85%</span>
        </div>

        <div className="progress">
          <div style={{ width: "85%" }}></div>
        </div>

        <div className="breakdown-row">
          <span>Reasoning</span>
          <span>81%</span>
        </div>

        <div className="progress">
          <div style={{ width: "81%" }}></div>
        </div>

      </div>

    </div>
  );
}