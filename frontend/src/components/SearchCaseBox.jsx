export default function SearchCaseBox() {
  return (
    <div className="search-section">

      <input type="text" placeholder="Search Case A (e.g. Property Dispute)" />

      <span className="vs">VS</span>

      <input type="text" placeholder="Search Case B (e.g. Criminal Appeal)" />

      <button className="compare-btn">
        Compare Cases
      </button>

    </div>
  );
}