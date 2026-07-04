export default function ComparisonTable() {
  return (
    <div className="comparison-matrix">

      <div className="matrix-header">
        <div>Attribute</div>
        <div>Case A</div>
        <div>Case B</div>
      </div>

      <div className="matrix-row">
        <div>Court</div>
        <div>Supreme Court</div>
        <div>Supreme Court</div>
      </div>

      <div className="matrix-row">
        <div>Year</div>
        <div>2022</div>
        <div>2023</div>
      </div>

      <div className="matrix-row">
        <div>Judge</div>
        <div>Justice Sharma</div>
        <div>Justice Verma</div>
      </div>

      <div className="matrix-row">
        <div>Outcome</div>
        <div className="success-tag">Allowed</div>
        <div className="success-tag">Allowed</div>
      </div>

      <div className="matrix-row">
        <div>Similarity</div>
        <div>Constitutional Matter</div>
        <div>Constitutional Matter</div>
      </div>

    </div>
  );
}